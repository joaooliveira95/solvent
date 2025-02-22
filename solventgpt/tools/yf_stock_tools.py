from typing import Optional, Type, List
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from solventgpt.tools.yf_util import get_date_stock_price, get_price_change_percent, get_best_performing


class StockPriceCheckInput(BaseModel):
    """Input for Stock price check."""

    stockticker: str = Field(description="Ticker symbol for stock or index")
    date: Optional[str] = Field(description="Date for the stock information date in iso format YYYY-MM-DD")


class StockPriceTool(BaseTool):
    name = "get_stock_ticker_price"
    description = (
        "Useful for when you need to find out the price of stock. "
        "You should input the stock ticker used on the yfinance API"
    )

    def _run(self, stockticker: str, date: str = None):
        price_response = get_date_stock_price(stockticker, date)
        return price_response

    def _arun(self, stockticker: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = StockPriceCheckInput


class StockChangePercentageCheckInput(BaseModel):
    """Input for Stock ticker check. for percentage check"""

    stockticker: str = Field(description="Ticker symbol for stock or index")
    days_ago: int = Field(description="Int number of days to look back")


class StockPercentageChangeTool(BaseTool):
    name = "get_price_change_percent"
    description = (
        "Useful for when you need to find out the percentage change "
        "in a stock's value. "
        "You should input the stock ticker used on the yfinance API "
        "and also input the "
        "number of days to check the change over"
    )

    def _run(self, stockticker: str, days_ago: int):
        price_change_response = get_price_change_percent(stockticker, days_ago)

        return price_change_response

    def _arun(self, stockticker: str, days_ago: int):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = StockChangePercentageCheckInput


class StockBestPerformingInput(BaseModel):
    """Input for Stock ticker check. for percentage check"""

    stocktickers: List[str] = Field(description="Ticker symbols for stocks or indices")
    days_ago: int = Field(description="Int number of days to look back")


class StockGetBestPerformingTool(BaseTool):
    name = "get_best_performing"
    description = (
        "Useful for when you need to the performance of multiple "
        "stocks over a period. "
        "You should input a list of stock "
        "tickers used on the yfinance API "
        "and also input the number of days to check the change over"
    )

    def _run(self, stocktickers: List[str], days_ago: int):
        price_change_response = get_best_performing(stocktickers, days_ago)

        return price_change_response

    def _arun(self, stockticker: List[str], days_ago: int):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = StockBestPerformingInput
