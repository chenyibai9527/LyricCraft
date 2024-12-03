from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Settings
from app.api.endpoints import lyrics, lyrics_v2, chat
import uvicorn
from fastapi.responses import FileResponse

def create_app() -> FastAPI:
    settings = Settings()
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION
    )
    
    # 添加静态文件支持
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # 添加 CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由
    app.include_router(lyrics.router, prefix="/api/v1")
    app.include_router(lyrics_v2.router, prefix="/api/v2")
    app.include_router(chat.router, prefix="/api/v1")
    
    return app

app = create_app()

# 添加根路由重定向到 index.html
@app.get("/")
async def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)