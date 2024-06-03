import os
import string
import random
import gradio as gr
import postlang
from solventgpt.voicechatbot import VoiceChatInterface
from solventgpt.models import get_llm, get_model_names
from solventgpt import config as cfg
from solventgpt.utils import get_asset_path, get_allowed_paths

# product metris
postlang.api_key = cfg.POSTLANG_API_KEY
postlang.host = cfg.POSTLANG_HOST
# langsmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agent SL Project"
os.environ["LANGCHAIN_API_KEY"] = "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"

global_css = """
footer {visibility: hidden}
#solvent-logo {display: block}
#solvent-logo > button > div > img {width: 280px !important; height: 70px !important;}
#solvent-logoname {font-family: "League Spartan", sans-serif; font-size: 18pt;}
"""

js_func = """
function refresh() {
    const url = new URL(window.location);

    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""

SESSION_ID = None
USER_ID = None


def generate_session_id():
    return "".join([random.choice(string.ascii_letters) for _ in range(12)])


def generate_user_id():
    return "".join([random.choice(string.ascii_letters) for _ in range(8)])


def generate_chat(message, history, model, request: gr.Request):
    global USER_ID, SESSION_ID
    # start a new session ID for each conversation
    if len(history) == 0 or not SESSION_ID:
        SESSION_ID = generate_session_id()
    USER_ID = request.username or generate_user_id()

    response = model.agent_predict(message, history, user_id=USER_ID)

    postlang.task(
        USER_ID,
        input=message,
        output=response,
        session_id=SESSION_ID,
        properties={"llm_model": model.modelname},
    )
    return response


async def on_like(evdata: gr.LikeData):
    if evdata.liked:
        event = "llm-like"
    else:
        event = "llm-dislike"

    postlang.task(
        USER_ID,
        event=event,
        input="",
        output=evdata.value,
        session_id=SESSION_ID,
        properties={},
    )


def on_model_change(modelname):
    model = get_llm(modelname)
    return model


def on_load(modelname):
    model = get_llm(modelname)
    return model


with gr.Blocks(fill_height=True, css=global_css, js=js_func) as demo:
    model = gr.State()

    with gr.Row(elem_id="solvent-header"):
        logo = gr.Image(
            get_asset_path("logo_full.png"),
            elem_id="solvent-logo",
            height=65,
            width=65,
            container=False,
            label=False,
            show_download_button=False,
        )

    modelname = gr.Dropdown(choices=get_model_names(), value=cfg.DEFAULT_MODEL, label="GPT Model", visible=False)
    modelname.change(on_model_change, inputs=[modelname], outputs=[model])

    ci = VoiceChatInterface(generate_chat, additional_inputs=[model], fill_height=True, analytics_enabled=False)
    ci.chatbot.sanitize_html = False
    ci.chatbot.likeable = True
    ci.chatbot.like(on_like, None, None)
    gr.HTML("<br />")
    gr.Markdown("© 2024 Solvent.Life™ LTD, LLC. All rights reserved.")

    demo.load(on_load, inputs=[modelname], outputs=[model])

if __name__ == "__main__":
    demo.queue().launch(auth=cfg.AUTH, server_name="0.0.0.0", allowed_paths=get_allowed_paths())
