from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool


class YahooStockInfoInput(BaseModel):
    """Input for the YahooStockInfo tool."""

    query: str = Field(description="company ticker query to look up")


class YahooStockInfoTool(BaseTool):
    """Tool that gets latest stock values from Yahoo Finance."""

    name: str = "yahoo_stock_info"
    description: str = (
        "Useful to get latest trading information about a "
        "public company stock. "
        "Input should be a company ticker. "
        "For example, AAPL for Apple, MSFT for Microsoft."
    )

    args_schema: Type[BaseModel] = YahooStockInfoInput

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Yahoo finance stock info tool."""
        try:
            import yfinance
        except ImportError:
            raise ImportError(
                "Could not import yfinance python package. " "Please install it with `pip install yfinance`."
            )

        stock_symbol = query
        stock = yfinance.Ticker(stock_symbol)

        stock_name = stock.info.get("longName", stock_symbol)
        pe_ratio = stock.info.get("trailingPE", "P/E ratio not available")
        data = stock.history(period="1d")
        current_price = data["Close"].iloc[-1] if not data.empty else "No data available"

        description = (
            f"The current stock price of {stock_name} ({stock_symbol}) is {current_price}. "
            f"The overall earnings ratio, commonly referred to as the Price-to-Earnings (P/E) ratio, "
            f"for {stock_name} ({stock_symbol}) is currently {pe_ratio}. This ratio indicates "
            f"how much investors are willing to pay for one dollar of earnings and is a commonly used "
            f"metric to gauge a company's valuation.\n\n"
        )

        return description
