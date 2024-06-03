from langchain_groq import ChatGroq
import solventgpt.config as cfg
from solventgpt.models.basemodel import BaseLLMModel


class GroqModel(BaseLLMModel):
    def __init__(self, modelname, *args, **kwargs):
        super().__init__(modelname, *args, **kwargs)
        self.llm = ChatGroq(model_name=modelname, groq_api_key=cfg.GROQ_API_KEY, temperature=cfg.MODEL_TEMPERATURE)
