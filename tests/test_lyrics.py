import asyncio
import aiohttp
import json

async def test_stream():
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://localhost:8000/api/v1/lyrics/generate/stream',
            json={
                "theme": "思念",
                "style": "抒情",
                "length": "200"
            }
        ) as response:
            async for line in response.content:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = json.loads(line[6:])
                    print(data['content'], end='', flush=True)
                    if data.get('error'):
                        print(f"\n错误: {data['error']}")
                        break
                    if data['done']:
                        break

if __name__ == "__main__":
    asyncio.run(test_stream())