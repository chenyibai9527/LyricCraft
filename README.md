# AI Creation Assistant | AI 创作助手 | AI創作アシスタント

[English](README_EN.md) | [中文](README.md) | [日本語](README_JA.md)

一个基于通义千问2.5的智能创作助手，支持智能对话和歌词创作功能。

## 功能特点
- 使用 DashScope 的通义千问2.5 模型
- 使用 FastAPI 构建 RESTful API
- 使用 TailwindCSS 构建前端界面
- 使用 uvicorn 作为 ASGI 服务器
- 使用 pydantic 进行数据验证
- 既可以作为 API 服务使用，也可以作为 Web 界面使用。

### 1. 智能对话
- 流式响应，实时输出
- 智能输入预测
- 上下文感知
- 自动提供后续问题建议

### 2. 歌词创作
- 支持主题、风格、长度自定义
- 流式生成，实时展示
- 专业歌词结构（Verse、Chorus等）
- 自动优化韵律和节奏

## 技术栈

- 后端：FastAPI + Python 3.x
- 前端：原生 JavaScript + TailwindCSS
- AI模型：通义千问2.5
- 开发工具：uvicorn, openai, pydantic


## 快速开始

1. 克隆项目并安装依赖：
```bash
git clone [repository-url]
cd ai-creation-assistant
python -m venv venv
source venv/bin/activate # Linux/Mac
```
或
```bash
.\venv\Scripts\activate # Windows
```
安装依赖：
```bash
pip install -r requirements.txt
```


2. 配置环境变量：
创建 `.env` 文件并添加以下配置：
```bash
DASHSCOPE_API_KEY=your_api_key
BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen2.5-3b-instruct
```

3. 启动服务：
```bash
uvicorn main:app --reload
```


4. 访问服务：
- API文档：http://localhost:8000/docs
- Web界面：http://localhost:8000/

## API 接口

### 对话接口
- POST `/api/v1/chat/stream` - 流式对话
- POST `/api/v1/chat/predict` - 输入预测

### 歌词接口
- POST `/api/v2/lyrics` - 简单歌词生成
- POST `/api/v1/lyrics/generate/stream` - 流式歌词生成

## 部署说明

本项目支持多种部署方式：

1. 直接部署：
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. 使用 Supervisor 管理：
```bash
ini
[program:ai-assistant]
command=/path/to/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
directory=/path/to/project
user=www-data
autostart=true
autorestart=true
```

3. 使用 Nginx 反向代理：
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

## 开发说明

项目结构：
- app/
  - api/
    - endpoints/ # API路由
  - core/ # 核心配置 
  - models/ # 数据模型
  - services/ # 业务逻辑


## 许可证

MIT License

## 贡献指南

欢迎提交 Issue 和 Pull Request！
