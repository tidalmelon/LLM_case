import logging
from typing import Any, List, Mapping, Optional, Iterator

import requests
import json

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from langchain.schema.output import GenerationChunk

logger = logging.getLogger(__name__)


class ChatGLM(LLM):
    """ChatGLM LLM service.

    Example:
        .. code-block:: python

            from langchain.llms import ChatGLM
            endpoint_url = (
                "http://127.0.0.1:8000"
            )
            ChatGLM_llm = ChatGLM(
                endpoint_url=endpoint_url
            )
    """

    endpoint_url: str = "http://127.0.0.1:4001"
    """Endpoint URL to use."""
    model_kwargs: Optional[dict] = None
    """Keyword arguments to pass to the model."""
    max_token: int = 20000
    """Max token allowed to pass to the model."""
    temperature: float = 0.1
    """LLM model temperature from 0 to 10."""
    history: List[List] = []
    """History of the conversation"""
    top_p: float = 0.7
    """Top P for nucleus sampling from 0 to 1"""
    with_history: bool = False
    """Whether to use history or not"""

    @property
    def _llm_type(self) -> str:
        return "chat_glm"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        _model_kwargs = self.model_kwargs or {}
        return {
            **{"endpoint_url": self.endpoint_url},
            **{"model_kwargs": _model_kwargs},
        }

    #def _stream(
    #    self,
    #    prompt: str,
    #    stop: Optional[List[str]] = None,
    #    run_manager: Optional[CallbackManagerForLLMRun] = None,
    #    **kwargs: Any,
    #) -> Iterator[GenerationChunk]:
    #    params = {**self._invocation_params, **kwargs, "stream": True}
    #    self.get_sub_prompts(params, [prompt], stop)  # this mutates params
    #    for stream_resp in completion_with_retry(
    #        self, prompt=prompt, run_manager=run_manager, **params
    #    ):
    #        if not isinstance(stream_resp, dict):
    #            stream_resp = stream_resp.dict()
    #        chunk = _stream_response_to_generation_chunk(stream_resp)
    #        yield chunk
    #        if run_manager:
    #            run_manager.on_llm_new_token(
    #                chunk.text,
    #                chunk=chunk,
    #                verbose=self.verbose,
    #                logprobs=chunk.generation_info["logprobs"]
    #                if chunk.generation_info
    #                else None,
    #            )

    # reference
    # https://www.yangyanxing.com/article/use-langchain-custom-stream.html

    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:

        _model_kwargs = self.model_kwargs or {}

        # HTTP headers for authorization
        headers = {"Content-Type": "application/json"}

        payload = {
            "prompt": prompt,
            "temperature": self.temperature,
            "history": self.history,
            "max_length": self.max_token,
            "top_p": self.top_p,
        }
        payload.update(_model_kwargs)
        payload.update(kwargs)

        logger.debug(f"ChatGLM payload: {payload}")

        response = requests.post(self.endpoint_url+"/stream", stream=True, headers=headers, json=payload)

        if response.status_code == 200:
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    if line.startswith('data'):
                        line = line[6:]
                        dic = json.loads(line)
                        if 'prompt' not in dic:
                            #text = dic['response']
                            text = dic['delta']
                            chunk = GenerationChunk(text=text)
                            yield chunk

                            if run_manager:
                                run_manager.on_llm_new_token(
                                    chunk.text,
                                    chunk=chunk,
                                    verbose=self.verbose,
                                    logprobs=chunk.generation_info["logprobs"]
                                    if chunk.generation_info
                                    else None,
                                )
        else:
            chunk = GenerationChunk(text=f"响应失败,失败信息为: {response.message}")
            yield chunk
            # 这里可能是错误的, 还没弄明白这个接口
            if run_manager:
                run_manager.on_llm_new_token(
                    chunk.text,
                    chunk=chunk,
                    verbose=self.verbose,
                    logprobs=chunk.generation_info["logprobs"]
                    if chunk.generation_info
                    else None,
                )



    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call out to a ChatGLM LLM inference endpoint.

        Args:
            prompt: The prompt to pass into the model.
            stop: Optional list of stop words to use when generating.

        Returns:
            The string generated by the model.

        Example:
            .. code-block:: python

                response = chatglm_llm("Who are you?")
        """

        _model_kwargs = self.model_kwargs or {}

        # HTTP headers for authorization
        headers = {"Content-Type": "application/json"}

        payload = {
            "prompt": prompt,
            "temperature": self.temperature,
            "history": self.history,
            "max_length": self.max_token,
            "top_p": self.top_p,
        }
        payload.update(_model_kwargs)
        payload.update(kwargs)

        logger.debug(f"ChatGLM payload: {payload}")

        # call api
        try:
            response = requests.post(self.endpoint_url+'/chat', headers=headers, json=payload)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error raised by inference endpoint: {e}")

        logger.debug(f"ChatGLM response: {response}")

        if response.status_code != 200:
            raise ValueError(f"Failed with response: {response}")

        try:
            parsed_response = response.json()

            # Check if response content does exists
            if isinstance(parsed_response, dict):
                content_keys = "response"
                if content_keys in parsed_response:
                    text = parsed_response[content_keys]
                else:
                    raise ValueError(f"No content in response : {parsed_response}")
            else:
                raise ValueError(f"Unexpected response type: {parsed_response}")

        except requests.exceptions.JSONDecodeError as e:
            raise ValueError(
                f"Error raised during decoding response from inference endpoint: {e}."
                f"\nResponse: {response.text}"
            )

        if stop is not None:
            text = enforce_stop_tokens(text, stop)
        if self.with_history:
            self.history = self.history + [[None, parsed_response["response"]]]
        return text
