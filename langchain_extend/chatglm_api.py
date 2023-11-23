
import os
import sys
import json
import torch
import uvicorn
import logging
import argparse
from fastapi import FastAPI
from transformers import AutoTokenizer, AutoModel
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import ServerSentEvent, EventSourceResponse


def getLogger(name, file_name, use_formatter=True):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s    %(message)s')
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    if file_name:
        handler = logging.FileHandler(file_name, encoding='utf8')
        handler.setLevel(logging.INFO)
        if use_formatter:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
            handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = getLogger('ChatGLM', 'chatlog.log')

MAX_HISTORY = 3


class ChatGLM():
    def __init__(self) -> None:
        logger.info("Start initialize model...")
        #path = "THUDM/chatglm2-6b-32k"
        path = "/root/.cache/huggingface/hub/THUDM/chatglm2-6b-32k"
        self.tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(path, trust_remote_code=True).quantize(8).half().cuda()
        self.model.eval()
        logger.info("Model initialization finished.")

    def clear(self) -> None:
        if torch.cuda.is_available():
            with torch.cuda.device(f"cuda:{args.device}"):
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()

    def answer(self, prompt, history=[], max_length=2048, temperature=0.7, top_p=0.4):
        response, history = self.model.chat(self.tokenizer, 
                                            prompt, 
                                            history=history, 
                                            max_length=max_length, 
                                            temperature=temperature, 
                                            top_p=top_p)
        history = [list(h) for h in history]
        self.clear()
        return response, history

    def stream(self, prompt, history=[], max_length=2048, temperature=0.7, top_p=0.4):
        if prompt is None or history is None:
            yield {"prompt": "", "response": "", "history": [], "finished": True}
        size = 0
        response = ""
        for response, history in self.model.stream_chat(self.tokenizer, 
                                                        prompt, 
                                                        history=history,
                                                        max_length=max_length, 
                                                        temperature=temperature, 
                                                        top_p=top_p):
            this_response = response[size:]
            history = [list(h) for h in history]
            size = len(response)
            yield {"delta": this_response, "response": response, "finished": False}
        logger.info("Answer - {}".format(response))
        self.clear()
        yield {"prompt": prompt, "delta": "[EOS]", "response": response, "history": history, "finished": True}



def start_server(http_address: str, port: int, gpu_id: str):
    os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_id

    bot = ChatGLM()

    app = FastAPI()
    app.add_middleware(CORSMiddleware,
                       allow_origins=["*"],
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"]
                       )

    @app.get("/")
    def index():
        return {'message': 'started', 'success': True}

    @app.post("/chat")
    async def answer_question(arg_dict: dict):
        result = {"prompt": "", "response": "", "success": False}
        try:
            text = arg_dict.pop("prompt")
            ori_history = arg_dict.pop("history")
            logger.info("Prompt - {}".format(text))
            if len(ori_history) > 0:
                logger.info("History - {}".format(ori_history))

            history = ori_history[-MAX_HISTORY:]
            history = [tuple(h) for h in history]
            response, history = bot.answer(text, history, **arg_dict)
            logger.info("Answer - {}".format(response))
            ori_history.append((text, response))
            result = {"prompt": text, "response": response,
                      "history": ori_history, "success": True}
        except Exception as e:
            logger.error(f"error: {e}")
        return result

    @app.post("/stream")
    def answer_question_stream(arg_dict: dict):
        def decorate(generator):
            for item in generator:
                yield ServerSentEvent(json.dumps(item, ensure_ascii=False), event='delta')

        try:
            text = arg_dict.pop("prompt")
            ori_history = arg_dict.pop("history")
            logger.info("Prompt - {}".format(text))
            if len(ori_history) > 0:
                logger.info("History - {}".format(ori_history))
            history = ori_history[-MAX_HISTORY:]
            history = [tuple(h) for h in history]
            return EventSourceResponse(decorate(bot.stream(text, history, **arg_dict)))
        except Exception as e:
            logger.error(f"error: {e}")
            return EventSourceResponse(decorate(bot.stream(None, None)))


    @app.get("/free_gc")
    def free_gpu_cache():
        try:
            bot.clear()
            return {"success": True}
        except Exception as e:
            logger.error(f"error: {e}")
            return {"success": False}

    logger.info("starting server...")
    uvicorn.run(app=app, host=http_address, port=port, workers=1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stream API Service for ChatGLM2-6B')
    parser.add_argument('--device', '-d', help='device，-1 means cpu, other means gpu ids', default='0')
    parser.add_argument('--host', '-H', help='host to listen', default='0.0.0.0')
    parser.add_argument('--port', '-P', help='port of this service', default=4001)
    args = parser.parse_args()
    start_server(args.host, int(args.port), args.device)















