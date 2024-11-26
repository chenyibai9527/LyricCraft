from app.services.lyrics import LyricGenerator
from app.services.chat import ChatService

def get_lyrics_generator() -> LyricGenerator:
    return LyricGenerator()

def get_chat_service() -> ChatService:
    return ChatService()