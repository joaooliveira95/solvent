from langchain_community.chat_models.perplexity import ChatPerplexity
from solventgpt.models.basemodel import BaseLLMModel
import solventgpt.config as cfg


class PerplexityModel(BaseLLMModel):
    def __init__(self, modelname, *args, **kwargs):
        super().__init__(modelname, *args, **kwargs)
        self.llm = ChatPerplexity(
            model=modelname,
            pplx_api_key=cfg.PPLX_API_KEY,
            temperature=cfg.MODEL_TEMPERATURE,
        )
        self.init_agent()
