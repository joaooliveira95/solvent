import logging
from pathlib import Path
from datetime import datetime
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import gradio as gr
from typing import Optional
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
from supabase import create_client
import stripe

from solventgpt.protoui import demo
from solventgpt.models import get_llm
from solventgpt import config as cfg
from solventgpt.utils import api2gr
from solventgpt.auth import get_current_user, supa_login
from solventgpt.database import (
    User,
    Credentials,
    ConversationMessage,
    ConversationHeader,
    Conversation,
    ConversationInput,
    ConversationList,
    ConversationResponse,
    db_user_plan,
    db_user_create,
    db_user_conversations,
    db_conversation,
    db_conversation_delete,
    db_create_conversation,
    db_update_conversation,
    db_message_feedback,
    db_create_message,
    db_user_payment,
    db_user_plan_change,
)

CUSTOM_PATH = "/protoui"

supa_client = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stripe.api_key = cfg.INSTANCE[cfg.APP_ENV]["stripe_key"]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """life span events"""
    try:
        global super_client
        super_client = create_client(cfg.SUPABASE_URL, cfg.SUPABASE_TOKEN)
        yield
    finally:
        logging.info("lifespan shutdown")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_main():
    return RedirectResponse(url="/protoui/?__theme=dark")


# FIXME temporary
@app.post("/test/login")
async def test_login(credentials: Credentials):
    data = supa_login(credentials.username, credentials.password)
    return {"token": data.session.access_token}


@app.get("/v1/user/plan")
async def user_plan(user: dict = Depends(get_current_user)) -> User:
    return db_user_plan(user["sub"])


@app.post("/v1/user/plan")
async def user_plan_create(user: dict = Depends(get_current_user)) -> User:
    user = User(user_id=user["sub"], plan_limit=cfg.PLAN_FREE_LIMIT, plan_type="free")
    db_user_create(user)
    return user


@app.get("/v1/checkout-session")
async def create_checkout_session(user: dict = Depends(get_current_user)):
    app_env = cfg.APP_ENV
    base_url = cfg.INSTANCE[app_env]["url"]
    user_id = user["sub"]
    urls = {}
    prices = cfg.INSTANCE[app_env]["prices"]
    for product, price_id in prices.items():
        mode = "payment" if product == "lifetime" else "subscription"
        chk_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode=mode,
            success_url=base_url + "/test/plan-upgrade/completed?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=base_url + "/test/plan-upgrade/cancelled",
            metadata={"user_id": user_id, "product": product},
        )
        urls[product] = chk_session["url"]
    return urls


# temporary endpoints for testing
# @app.get("/test/plan-upgrade", response_class=HTMLResponse, include_in_schema=False)
# async def tmp_plan_upgrade(current_user: dict = Depends(get_current_user)):
#    links = "".join([f'<li><a href="https://buy.stripe.com/{paylink}">Buy {product}</a></li>'
#            for product, url in urls.items()])
#    return f"<html><body><ul>{links}</ul></body></html>"


@app.get("/test/plan-upgrade/completed")
async def payment_success():
    return HTMLResponse("<html><body><h1>Plan upgrade successful!</h1></body></html>")


@app.get("/test/plan-upgrade/cancelled")
async def payment_cancel():
    return HTMLResponse("<html><body><h1>Plan upgrade cancelled</h1></body></html>")


@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    endpoint_secret = "whsec_539mr9MmbCF9AP8AdRVoILa9vLcUpVSP"

    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": "Invalid payload"})
    except stripe.error.SignatureVerificationError as e:
        return JSONResponse(status_code=400, content={"message": "Invalid signature"})

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print("checkout.session.completed webhook")
        print(session)
        db_user_payment(
            user_id=session["metadata"]["user_id"],
            email=session.get("customer_details", {}).get("email", ""),
            plan_type=session["metadata"]["product"],
            amount_total=session["amount_total"],
            stripe_id=session["id"],
        )
        db_user_plan_change(session["metadata"]["user_id"], session["metadata"]["product"])
    return JSONResponse(status_code=200, content={"message": "Received"})


@app.get("/webasset/{webasset_name}", include_in_schema=False)
async def get_webasset(webasset_name: str):
    pathname = Path(__file__).parent.parent / "web_assets" / webasset_name
    media_type = ""
    if webasset_name.endswith("png"):
        media_type = "image/png"
    return FileResponse(pathname, media_type=media_type)  # Change the media_type according to the image type


@app.post("/v1/agent/completion")
async def agent_completion(inp: ConversationInput, user: dict = Depends(get_current_user)) -> ConversationResponse:
    userplan = db_user_plan(user["sub"])
    if userplan.plan_usage >= userplan.plan_limit:
        raise HTTPException(status_code=403, detail="Quota exceeded. No more calls are allowed before limit reset")

    model = get_llm(cfg.DEFAULT_MODEL)

    # last message is the user query
    assert inp.messages[-1].role == "user"
    user_query = inp.messages[-1].content
    history = api2gr(inp.messages[:-1])
    response = model.agent_predict(user_query, history, user_id=inp.user_id)

    msg = ConversationMessage(role="assistant", content=response)
    conv_response = ConversationResponse(
        conversation_id=inp.conversation_id, user_id=inp.user_id, created=str(datetime.now()), message=msg
    )
    db_create_message(conversation_id=inp.conversation_id, user_id=inp.user_id, role="user", content=user_query)
    db_create_message(conversation_id=inp.conversation_id, user_id=inp.user_id, role="assistant", content=response)
    return conv_response


@app.get("/v1/conversations/user")
async def get_user_conversations(user: dict = Depends(get_current_user)) -> ConversationList:
    return db_user_conversations(user["sub"])


@app.get("/v1/conversation")
async def get_conversation(conversation_id: str, user: dict = Depends(get_current_user)) -> Optional[Conversation]:
    return db_conversation(conversation_id)


@app.delete("/v1/conversation")
async def delete_conversation(conversation_id: str, user: dict = Depends(get_current_user)):
    db_conversation_delete(conversation_id)


@app.post("/v1/conversation")
async def add_conversation(user: dict = Depends(get_current_user)) -> Conversation:
    return db_create_conversation(user["sub"])


@app.put("/v1/conversation/title")
async def update_conversation_title(
    conversation_id: str, title: str, user: dict = Depends(get_current_user)
) -> Conversation:
    return db_update_conversation(conversation_id, title)


@app.post("/v1/message/feedback")
async def message_feedback(message_id: int, feedback: int, user: dict = Depends(get_current_user)):
    db_message_feedback(message_id, user["sub"], feedback)


app = gr.mount_gradio_app(app, demo, auth=supa_login, path=CUSTOM_PATH)
