import requests
import json

headers={
    'Authorization': '',
    'Content-Type': 'application/json'
}

history = []

payload = {
    "prompt": "你好",
    "temperature": 0.7,
    "history": history,
    "max_length": 10000,
    "top_p": 0.4,
}


print('打印机模式')

url = 'http://127.0.0.1:4001/stream'
response = requests.post(url, stream=True, headers=headers, json=payload)
if response.status_code == 200:
    for line in response.iter_lines(decode_unicode=True):
        if line:
            if line.startswith("data"):
                line = line[6:]
                dic = json.loads(line)
                if 'prompt' not in dic:
                    print(dic['delta'], end="", flush=True)
                else:
                    print()

print("堵塞模式")
url = 'http://127.0.0.1:4001/chat'
response = requests.post(url, headers=headers, json=payload)
if response.status_code == 200:
    print(response.json()['response'])


print('Langchain pattern')

from chatglm_e import ChatGLM

llm = ChatGLM()

for chunk in llm.stream("你好"):
    print(chunk, end="", flush=True)
print()

