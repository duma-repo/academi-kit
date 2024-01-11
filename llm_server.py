from llms.llm import LLM
from llms.chatgpt import ChatGPT
import config

model: LLM = ChatGPT(config.model_name)


def request_llm(sys_prompt: str, user_prompt: list, stream=False):
    return model.request(sys_prompt, user_prompt, stream)
