from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest, ChatStreamResponse, PredictRequest, PredictResponse, ChatMessage
from app.services.chat import ChatService
from app.api.deps import get_chat_service
from app.core.config import settings
import json
from pydantic import BaseModel
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["对话"])

@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    流式对话API端点
    """
    async def event_generator():
        async for chunk in chat_service.chat_stream(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        ):
            yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
    )

@router.post("/predict", response_model=PredictResponse)
async def predict_completion(
    request: PredictRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """预测用户输入的完整内容"""
    try:
        if not request.input or len(request.input.strip()) < 2:
            return PredictResponse(prediction=None)

        messages = [
            ChatMessage(
                role="system",
                content="""你的任务是预测用户想要输入的完整句子。
                要求：
                1. 基于当前输入预测用户的完整意图
                2. 不要重复用户已输入的内容
                3. 只输出后续可能的内容
                4. 保持自然的语言流畅性
                例如：
                输入：'写一首日文'
                预测：'歌词'
                输入：'我想问一下关于'
                预测：'项目开发的问题'"""
            ),
            ChatMessage(
                role="user",
                content=f"用户当前输入：{request.input}\n预测后续内容："
            )
        ]

        # 添加部分历史消息作为上下文
        if request.messages:
            context_messages = request.messages[-2:]
            messages = [*context_messages, *messages]

        response = chat_service.client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[{"role": msg.role, "content": msg.content} for msg in messages],
            max_tokens=50,
            temperature=0.3,
            stream=False
        )
        
        prediction = response.choices[0].message.content.strip()
        
        # 确保预测以用户输入开头
        full_prediction = request.input + prediction
            
        logger.info(f"Input: {request.input} -> Prediction: {full_prediction}")
        return PredictResponse(prediction=full_prediction)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"预测过程发生错误: {str(e)}"
        )