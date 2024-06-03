from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

PREFIX = " Here is the interactive chart.\n"

CHART = """<iframe style="width: 100%; height: 425px" srcdoc='<!-- TradingView Widget BEGIN -->
<html style="width: 100%; height: 100%; overflow: hidden"><body style="width: 100%; height: 100%; margin: 0; overflow: hidden">
<style>.tradingview-widget-container .tradingview-widget-copyright {{display: none;}}</style>
<div class="tradingview-widget-container" style="height:100%;width:100%">
  <div class="tradingview-widget-container__widget" style="height:calc(100% - 10px);width:100%"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
  {{
  "autosize": true,
  "symbol": "{ticker}",
  "interval": "H",
  "timezone": "Etc/UTC",
  "theme": "dark",
  "style": "1",
  "locale": "en",
  "hide_top_toolbar": true,
  "enable_publishing": false,
  "allow_symbol_change": false,
  "save_image": false,
  "calendar": false,
  "studies": [
    "STD;DEMA",
    "STD;SMA"
  ],
  "hide_volume": true,
  "support_host": ""
}}
  </script>
</div>
</body></html>
<!-- TradingView Widget END -->'></iframe>"""


# fix some ticker exceptions
TICKER_MAP = {"^GSPC": "US500", "S&P 500": "US500"}


def remove_chart_html(content):
    """removes the chart html from the content (if present)"""
    startpos = content.find(CHART[:10])
    if startpos >= 0:
        endpos = content.find(CHART[-10:])
        if endpos >= 0 and endpos > startpos:
            content = content[:startpos].strip() + "\n" + content[endpos:].strip()
    # also remove prefix
    startpos = content.find(PREFIX)
    if startpos >= 0:
        content = content[:startpos] + content[(startpos + len(PREFIX)) :]
    return content


class StockChartInput(BaseModel):
    """Input for the StockChart tool."""

    query: str = Field(description="company ticker query to look up")


class StockChartTool(BaseTool):
    """Tool that generates a financial chart for stock ticker."""

    name: str = "stock_chart"
    description: str = (
        "Useful to generate a chart for a public company stock "
        "Input should be a company ticker. "
        "For example, AAPL for Apple, MSFT for Microsoft."
        "Only call this tool if the user asks explicitly for a chart or a plot."
    )

    args_schema: Type[BaseModel] = StockChartInput

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the stock chart tool."""

        # apply mapping for some mismatches between LLM and chart
        ticker = TICKER_MAP.get(query, query)

        return PREFIX + CHART.format(ticker=ticker)
