from langchain_openai import ChatOpenAI
from solventgpt.models.basemodel import BaseLLMModel
import solventgpt.config as cfg


class OpenAIModel(BaseLLMModel):
    def __init__(self, modelname, *args, **kwargs):
        super().__init__(modelname, *args, **kwargs)
        self.llm = ChatOpenAI(
            openai_api_key=cfg.OPENAI_API_KEY,
            temperature=cfg.MODEL_TEMPERATURE,
            model_name=modelname,
            openai_api_base=cfg.OPENAI_API_BASE,
        )
        self.init_agent()
