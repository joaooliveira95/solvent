"""Tool for the Perplexity model."""

from typing import Optional, Type

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from langchain.schema import HumanMessage
from langchain_community.chat_models.perplexity import ChatPerplexity
import solventgpt.config as cfg


class PerplexityQueryInput(BaseModel):
    """Input for the Perplexity tool."""

    query: str = Field(description="query text to the model")


class PerplexityQueryTool(BaseTool):
    """Tool that queries Perplexity model."""

    name: str = "perplexity"
    description: str = (
        "A wrapper around Perplexity online models. "
        "Useful for when you need to answer queries related, "
        "to very recent data, either financial data, trends or news "
        "Input should be the query to the model."
    )
    args_schema: Type[BaseModel] = PerplexityQueryInput

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Perplexity tool."""

        llm = ChatPerplexity(
            model=cfg.PPLX_ONLINE_MODEL,
            pplx_api_key=cfg.PPLX_API_KEY,
            temperature=cfg.MODEL_TEMPERATURE,
        )

        inputs = [HumanMessage(content=query)]
        response = llm(inputs)
        return response.content
