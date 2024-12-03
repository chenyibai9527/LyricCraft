# AI Creation Assistant | AI 创作助手 | AI創作アシスタント

[English](README_EN.md) | [中文](README.md) | [日本語](README_JA.md)

通義千問2.5をベースにした、インテリジェントな対話と作詞をサポートするAI創作アシスタントです。

## 機能

### 1. インテリジェント対話
- リアルタイム出力によるストリーミングレスポンス
- スマートな入力予測
- コンテキスト認識
- 自動フォローアップ質問の提案

### 2. 作詞機能
- テーマ、スタイル、長さのカスタマイズ可能
- リアルタイムストリーミング生成
- プロフェッショナルな歌詞構造（バース、コーラスなど）
- リズムと韻の自動最適化

## 技術スタック

- バックエンド: FastAPI + Python 3.x
- フロントエンド: Vanilla JavaScript + TailwindCSS
- AIモデル: 通義千問2.5
- 開発ツール: uvicorn, openai, pydantic

## プロジェクトの特徴
- DashScopeの通義千問2.5モデルを使用
- FastAPIによるRESTful API構築
- TailwindCSSによるフロントエンドインターフェース
- uvicornをASGIサーバーとして使用
- pydanticによるデータ検証
- APIサービスとWebインターフェースの両方として使用可能

## クイックスタート

1. プロジェクトをクローンし、依存関係をインストール：
```bash
git clone [repository-url]
cd ai-creation-assistant
python -m venv venv
source venv/bin/activate # Linux/Mac
```
または
```bash
.\venv\Scripts\activate # Windows
```

依存関係をインストール：
```bash
pip install -r requirements.txt
```


2. 環境変数を設定：
`.env`ファイルを作成し、以下の設定を追加：
```bash
DASHSCOPE_API_KEY=your_api_key
BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen2.5-3b-instruct
```

3. サービスを起動：
```bash
uvicorn main:app --reload
```


4. サービスにアクセス：
- APIドキュメント: http://localhost:8000/docs
- Webインターフェース: http://localhost:8000/

## API Endpoints

### Chat Interface
- POST `/api/v1/chat/stream` - ストリーミング会話
- POST `/api/v1/chat/predict` - 入力予測

### Lyrics Interface
- POST `/api/v2/lyrics` - シンプルな歌詞生成
- POST `/api/v1/lyrics/generate/stream` - ストリーミング歌詞生成

## デプロイ方法

This project supports multiple deployment methods:

1. 直接デプロイ：
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. Supervisorで管理：
```bash
ini
[program:ai-assistant]
command=/path/to/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
directory=/path/to/project
user=www-data
autostart=true
autorestart=true
```

3. Nginxをリバースプロキシとして使用：
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

## 開発ノート

プロジェクト構造：
- app/
  - api/
    - endpoints/ # APIルート
  - core/ # コア設定 
  - models/ # データモデル
  - services/ # ビジネスロジック


## ライセンス

MIT License

## 貢献ガイド

IssuesとPull Requestsを歓迎します！
