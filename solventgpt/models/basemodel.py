from typing import TypedDict, Annotated, Sequence
import operator
import json
from datetime import datetime
from langchain_core.messages import BaseMessage, FunctionMessage
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_core.utils.function_calling import convert_to_openai_function
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from langgraph.graph import StateGraph, END
from langfuse.callback import CallbackHandler
from langchain_community.chat_models.perplexity import ChatPerplexity

# from solventgpt.tools.yahoo_finance_news import YahooFinanceNewsTool
from solventgpt.tools.stock_chart import StockChartTool, remove_chart_html

from solventgpt.tools.yahoo_stock_info import YahooStockInfoTool
from solventgpt.tools.yf_stock_tools import StockPriceTool, StockPercentageChangeTool, StockGetBestPerformingTool
from solventgpt.tools.financialjuice import FinancialJuiceNewsTool

# from solventgpt.tools.ddg_search import DuckDuckGoSearchRun
from solventgpt.tools.perplexity import PerplexityQueryTool
from solventgpt.prompts import SYSTEM_PROMPT
import solventgpt.config as cfg


def get_model_names():
    return list(sorted(cfg.LLM_MODEL_MAP.keys()))


def get_llm(modelname):
    model_platform = cfg.LLM_MODEL_MAP[modelname]
    if model_platform == "openai":
        from solventgpt.models import OpenAIModel

        llm = OpenAIModel(modelname)
    elif model_platform == "perplexity":
        from solventgpt.models import PerplexityModel

        llm = PerplexityModel(modelname)
    elif model_platform == "groq":
        from solventgpt.models import GroqModel

        llm = GroqModel(modelname)
    else:
        raise ValueError(f"Unsupported model platform {model_platform}")
    return llm


def conv_to_lc(message, history, system=""):
    """convert conversation history to LangChain format"""
    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))
    if system and history_langchain_format and not isinstance(history_langchain_format[0], SystemMessage):
        system += f" Today is {str(datetime.now())}."
        history_langchain_format = [SystemMessage(content=system)] + history_langchain_format
    return history_langchain_format


def should_continue(state):
    last_message = state["messages"][-1]
    if "function_call" not in last_message.additional_kwargs:
        return "end"
    return "continue"


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


# TODO rework if perplexity experiment works ok
class BaseLLMModel:
    def __init__(self, modelname, system_prompt=SYSTEM_PROMPT):
        self.llm = None
        self.modelname = modelname
        self.system_prompt = system_prompt
        self.llm_pplx = ChatPerplexity(
            model=cfg.PPLX_ONLINE_MODEL,
            pplx_api_key=cfg.PPLX_API_KEY,
            temperature=cfg.MODEL_TEMPERATURE,
        )

    def init_agent(self):
        self.tools = [
            # DuckDuckGoSearchRun(),
            PerplexityQueryTool(),
            # YahooFinanceNewsTool(),
            StockChartTool(),
            StockPriceTool(),
            StockPercentageChangeTool(),
            StockGetBestPerformingTool(),
            FinancialJuiceNewsTool(),
        ]
        self.tool_executor = ToolExecutor(self.tools)
        functions = [convert_to_openai_function(t) for t in self.tools]
        self.llm = self.llm.bind_functions(functions)

    def predict(self, message, history):
        """runs the LLM for a conversation"""
        history_lc = conv_to_lc(message, history)
        response = self.llm(history_lc)
        return response.content

    def agent_predict(self, message, history, user_id=None, callback=None):
        """run agent flow for a conversation"""

        def call_model(state):
            messages = state["messages"]
            response = self.llm.invoke(messages)
            return {"messages": [response]}

        def call_tool(state):
            last_message = state["messages"][-1]
            action = ToolInvocation(
                tool=last_message.additional_kwargs["function_call"]["name"],
                tool_input=json.loads(last_message.additional_kwargs["function_call"]["arguments"]),
            )
            response = self.tool_executor.invoke(action)
            function_message = FunctionMessage(content=str(response), name=action.tool)
            return {"messages": [function_message]}

        workflow = StateGraph(AgentState)
        workflow.add_node("agent", call_model)
        workflow.add_node("action", call_tool)
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges("agent", should_continue, {"continue": "action", "end": END})
        workflow.add_edge("action", "agent")
        app = workflow.compile()

        inputs = inputs = {"messages": conv_to_lc(message, history, system=self.system_prompt)}

        lf_handler = CallbackHandler(
            public_key=cfg.FUSE_PUBKEY, secret_key=cfg.FUSE_SECKEY, host=cfg.FUSE_HOST, user_id=user_id
        )

        response = app.invoke(inputs, config={"callbacks": [lf_handler]})
        self.postprocess_perplexity(response)
        self.postprocess_chart(response)
        return response["messages"][-1].content

    def postprocess_chart(self, response):
        # take the last human message
        charts = [msg for msg in response["messages"] if isinstance(msg, FunctionMessage) and msg.name == "stock_chart"]
        if len(charts) > 0:
            # first remove the iframe from the last reply (if present)
            reply = response["messages"][-1].content
            reply = remove_chart_html(reply)
            # add the last chart to the final response
            response["messages"][-1].content = reply + charts[-1].content

    def _cut_conversation(self, messages):
        """cut the conversation in the last user message"""
        idx_msgs = [(idx, msg) for idx, msg in enumerate(messages)]
        user_msgs = [itm for itm in idx_msgs if isinstance(itm[1], HumanMessage)]
        if len(user_msgs) > 0:
            last_user_idx = user_msgs[-1][0]
            return messages[: (last_user_idx + 1)], messages[(last_user_idx + 1) :]
        return [], messages

    def postprocess_perplexity(self, response):
        """replace the final answer with perplexity if it was not a function call"""
        _, after_user = self._cut_conversation(response["messages"])
        func_calls = [msg for msg in after_user if isinstance(msg, FunctionMessage)]
        if len(func_calls) == 0:
            # if no tools where used, run perplexity
            # take out the last message from main LLM abd all function messages
            messages = [msg for msg in response["messages"] if not isinstance(msg, FunctionMessage)]
            messages, _ = self._cut_conversation(messages)
            if len(messages) > 0:
                res = self.llm_pplx.invoke(messages)
                response["messages"][-1].content = res.content
