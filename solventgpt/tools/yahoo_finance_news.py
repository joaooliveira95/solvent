from typing import Iterable, Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.documents import Document
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool
from requests.exceptions import HTTPError, ReadTimeout
from urllib3.exceptions import ConnectionError

from langchain_community.document_loaders.web_base import WebBaseLoader


class YahooFinanceNewsInput(BaseModel):
    """Input for the YahooFinanceNews tool."""

    query: str = Field(description="company ticker query to look up")


class YahooFinanceNewsTool(BaseTool):
    """Tool that searches financial news on Yahoo Finance."""

    name: str = "yahoo_finance_news"
    description: str = (
        "Useful for when you need to find financial news "
        "about a public company. "
        "Input should be a company ticker. "
        "For example, AAPL for Apple, MSFT for Microsoft."
    )
    top_k: int = 10
    """The number of results to return."""

    args_schema: Type[BaseModel] = YahooFinanceNewsInput

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Yahoo Finance News tool."""
        try:
            import yfinance
        except ImportError:
            raise ImportError(
                "Could not import yfinance python package. " "Please install it with `pip install yfinance`."
            )

        company = yfinance.Ticker(query)
        try:
            if company.isin is None:
                return f"Company ticker {query} not found."
        except (HTTPError, ReadTimeout, ConnectionError, ConnectionRefusedError):
            return f"Company ticker {query} not found."

        links = []
        try:
            links = [n["link"] for n in company.news if n["type"] == "STORY"]
        except (HTTPError, ReadTimeout, ConnectionError, ConnectionRefusedError):
            if not links:
                return f"No news found for company that searched with {query} ticker."
        if not links:
            return f"No news found for company that searched with {query} ticker."
        loader = WebBaseLoader(web_paths=links)
        docs = loader.load()
        result = self._format_results(docs, query)
        if not result:
            return f"No news found for company that searched with {query} ticker."
        return result

    @staticmethod
    def _format_results(docs: Iterable[Document], query: str) -> str:
        # removed until there is a mapping with mapping tickers and company names
        # if query in doc.metadata["description"] or query in doc.metadata["title"]
        doc_strings = ["\n".join([doc.metadata.get("title", ""), doc.metadata.get("description", "")]) for doc in docs]

        return "\n\n".join(doc_strings)
