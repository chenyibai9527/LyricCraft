from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "歌词生成器"
    PROJECT_DESCRIPTION: str = "基于通义千问2.5的歌词生成服务"
    VERSION: str = "1.0.0"
    
    DASHSCOPE_API_KEY: str
    BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    MODEL_NAME: str = "qwen2.5-3b-instruct"
    
    class Config:
        env_file = ".env"

settings = Settings()