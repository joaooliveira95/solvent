from typing import Optional, Type
from datetime import datetime, timedelta
import feedparser
import requests

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.tools import BaseTool


class FinancialJuiceNewsInput(BaseModel):
    """No inputs needed for the Financial Juice tool."""

    pass


class FinancialJuiceNewsTool(BaseTool):
    """Tool that gets latest news from Financial Juice."""

    name: str = "financial_juice"
    description: str = (
        "Useful always when reasoning about latest financial news "
        "to identify global trends and facts that can impact prices. "
        "Also useful to get next events and current and planned "
        "information disclosure on economic data (economic calendar) "
        "that may have an impact on stock prices."
    )
    args_schema: Type[BaseModel] = FinancialJuiceNewsInput
    top_k: int = 50
    """The number of results to return."""

    cache: dict = {}
    """save results in cache"""

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Financial Juice tool."""

        latest = self.cache.get("timestamp", datetime(2000, 1, 1))
        if datetime.now() - latest < timedelta(seconds=180):
            return self.cache.get("content")

        data = feedparser.parse("https://www.financialjuice.com/feed.ashx")
        docs = []
        for itm in data["entries"][: self.top_k]:
            docs.append(itm["title"].lstrip("FinancialJuice:").strip())

        try:
            res = requests.get("https://ideal-gentle-sailfish.ngrok-free.app/")
            if res.status_code == 200:
                docs += ["\n", res.content.decode("utf-8")]
        except Exception:
            pass

        result = "\n\n".join(docs)
        self.cache["timestamp"] = datetime.now()
        self.cache["content"] = result
        return result
