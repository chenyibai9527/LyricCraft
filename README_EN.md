# AI Creation Assistant | AI 创作助手 | AI創作アシスタント

[English](README_EN.md) | [中文](README.md) | [日本語](README_JA.md)

An intelligent creation assistant based on Qwen 2.5, supporting intelligent dialogue and lyrics creation.

## Features

### 1. Intelligent Dialogue
- Streaming response with real-time output
- Smart input prediction
- Context awareness
- Automatic follow-up question suggestions

### 2. Lyrics Creation
- Customizable theme, style, and length
- Real-time streaming generation
- Professional lyrics structure (Verse, Chorus, etc.)
- Automatic rhythm and rhyme optimization

## Tech Stack

- Backend: FastAPI + Python 3.x
- Frontend: Vanilla JavaScript + TailwindCSS
- AI Model: Tongyi Qianwen 2.5
- Development Tools: uvicorn, openai, pydantic

## Project Highlights
- Uses DashScope's Tongyi Qianwen 2.5 model
- Built with FastAPI for RESTful API
- Frontend interface built with TailwindCSS
- Uses uvicorn as ASGI server
- Data validation with pydantic
- Can be used both as an API service and web interface

## Quick Start

1. Clone the project and install dependencies:
```bash
git clone [repository-url]
cd ai-creation-assistant
python -m venv venv
source venv/bin/activate # Linux/Mac
```
or
```bash
.\venv\Scripts\activate # Windows
```

Install dependencies:
```bash
pip install -r requirements.txt
```


2. Configure environment variables:
Create a `.env` file and add the following configuration:
```bash
DASHSCOPE_API_KEY=your_api_key
BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen2.5-3b-instruct
```

3. Start the service:
```bash
uvicorn main:app --reload
```


4. Access the service:
- API documentation: http://localhost:8000/docs
- Web interface: http://localhost:8000/

## API Endpoints

### Chat Interface
- POST `/api/v1/chat/stream` - Streaming conversation
- POST `/api/v1/chat/predict` - Input prediction

### Lyrics Interface
- POST `/api/v2/lyrics` - Simple lyrics generation
- POST `/api/v1/lyrics/generate/stream` - Streaming lyrics generation

## Deployment Instructions

This project supports multiple deployment methods:

1. Direct deployment:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. Using Supervisor to manage:
```bash
ini
[program:ai-assistant]
command=/path/to/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
directory=/path/to/project
user=www-data
autostart=true
autorestart=true
```

3. Using Nginx as a reverse proxy:
```bash
nginx
server {
listen 80;
server_name your_domain.com;
location / {
proxy_pass http://127.0.0.1:8000;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
}
}
```

## Development Notes

Project structure:
- app/
  - api/
    - endpoints/ # API routes
  - core/ # Core configuration 
  - models/ # Data models
  - services/ # Business logic


## License

MIT License

## Contribution Guide

Welcome to submit Issues and Pull Requests!
