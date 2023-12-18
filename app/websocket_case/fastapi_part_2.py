import time
import jwt

from typing import List

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient


ZHIPUAI_API_KEY = ""


app = FastAPI()
# 允许所有跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def generate_token(apikey: str, exp_seconds: int):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)

    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),
    }

    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )



async def request(val: List[dict[str, str]], streaming=False):

    model = "chatglm_turbo"

    invoke_method = "sse-invoke" if streaming else "invoke"

    url = f"https://open.bigmodel.cn/api/paas/v3/model-api/{model}/{invoke_method}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": generate_token(ZHIPUAI_API_KEY, 60) # 60s
    }
    params = {
        "model": "gpt-3.5-turbo",
        "prompt": val,
        "temperature": 0.8,
        "incremental": streaming
    }


    async with AsyncClient() as client:
        if streaming:
            async with client.stream("POST", url, headers=headers, json=params, timeout=60) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data:"):
                        #print(line[5:], flush=True, end='')
                        yield line[5:]
                #print()
        else:
            response = await client.post(url, headers=headers, json=params, timeout=60)
            #print(response.text)
            yield response.text

@app.websocket("/chat") 
async def chat(websocket: WebSocket):

    await websocket.accept()

    while True:
        data = await websocket.receive_text()

        print("beigin============")
        print(data)
        print("end============")
        print()
        print()


        if data == 'quit':
            await websocket.close()
            break

        prompt = [{"role": "user", "content": data}]
        async for i in request(prompt, True):
            await websocket.send_text(i)

    # 还需要收集history_message, 这里就不写了


if __name__ == '__main__':

    import uvicorn
    uvicorn.run("fastapi_part_2:app", host="0.0.0.0", port=10000, reload=True)
