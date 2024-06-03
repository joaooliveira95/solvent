import os
import uuid
from datetime import datetime, date, timezone, timedelta
from typing import Optional
from pydantic import BaseModel
from supabase.client import create_client
import solventgpt.config as cfg
from solventgpt.utils import get_plan_limit


# FIXME temporary
class Credentials(BaseModel):
    username: str
    password: str


class User(BaseModel):
    user_id: str
    email: Optional[str] = ""
    plan_type: str
    plan_limit: int
    plan_usage: Optional[int] = 0
    renew_at: Optional[datetime] = None


class ConversationMessage(BaseModel):
    role: str
    content: str


class ConversationHeader(BaseModel):
    conversation_id: str
    user_id: str
    created: str
    title: Optional[str] = ""


class Conversation(ConversationHeader):
    messages: list[ConversationMessage]


class ConversationInput(BaseModel):
    conversation_id: str
    user_id: str
    messages: list[ConversationMessage]
    temperature: Optional[float] = 0.2


class ConversationList(BaseModel):
    conversations: list[ConversationHeader]


class ConversationResponse(BaseModel):
    conversation_id: str
    user_id: str
    created: str
    message: ConversationMessage


def supa_client():
    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_TOKEN"])


def db_user_plan(user_id):
    supa = supa_client()
    res = supa.table("userdata").select("*").eq("user_id", user_id).execute()
    if res and res.data:
        user = User(**res.data[0])
    else:
        user = User(user_id=user_id, plan_type="free", plan_limit=cfg.PLAN_FREE_LIMIT)
    res = supa.table("message").select("*").eq("user_id", user_id).eq("date", date.today()).eq("role", "user").execute()
    if res and res.data:
        user.plan_usage = len(res.data)
    else:
        user.plan_usage = 0
    today = datetime.now(timezone.utc).date()
    user.renew_at = datetime(today.year, today.month, today.day, 0, 0, 0, tzinfo=timezone.utc) + timedelta(1)
    return user


def db_user_create(user):
    supa = supa_client()
    payload = {"user_id": user.user_id, "email": user.email, "plan_type": user.plan_type, "plan_limit": user.plan_limit}
    res = supa.table("userdata").insert(payload).execute()
    return res.data


def db_user_plan_change(user_id, plan_type):
    supa = supa_client()
    res = supa.table("userdata").select("*").eq("user_id", user_id).execute()
    if res and len(res.data) > 0:
        res = (
            supa.table("userdata")
            .update({"plan_type": plan_type, "plan_limit": get_plan_limit(plan_type)})
            .eq("user_id", user_id)
            .execute()
        )
        return res.data
    else:
        payload = {"user_id": user_id, "plan_type": plan_type, "plan_limit": get_plan_limit(plan_type)}
        res = supa.table("userdata").insert(payload).execute()
        return res.data


def db_user_payment(user_id, email, plan_type, amount_total, stripe_id):
    """save a payment in the database"""
    supa = supa_client()
    payload = {
        "user_id": user_id,
        "email": email,
        "plan_type": plan_type,
        "amount_total": amount_total,
        "stripe_id": stripe_id,
        "created": str(datetime.now(timezone.utc)),
    }
    res = supa.table("payment").insert(payload).execute()
    return res.data


def db_user_conversations(user_id):
    supa = supa_client()
    res = supa.table("conversation").select("*").eq("user_id", user_id).eq("active", 1).execute()
    if res:
        convs = [ConversationHeader(**itm) for itm in res.data]
    else:
        convs = []
    return ConversationList(conversations=convs)


def db_conversation(conversation_id):
    supa = supa_client()
    res = supa.table("conversation").select("*").eq("conversation_id", conversation_id).eq("active", 1).execute()
    if res:
        resmsg = supa.table("message").select("*").eq("conversation_id", conversation_id).execute()
        msg = resmsg.data if resmsg else []
        msg = [ConversationMessage(role=itm["role"], content=itm["content"]) for itm in msg]
        convdic = res.data[0]
        convdic["messages"] = msg
        return Conversation(**convdic)
    return None


def db_message(message_id):
    supa = supa_client()
    res = supa.table("message").select("*").eq("message_id", message_id).execute()
    if res:
        return res.data[0]
    return None


def db_conversation_delete(conversation_id):
    supa = supa_client()
    supa.table("conversation").update({"active": 0}).eq("conversation_id", conversation_id).execute()


def db_create_conversation(user_id):
    supa = supa_client()
    payload = {
        "conversation_id": str(uuid.uuid4()),
        "user_id": user_id,
        "created": str(datetime.now(timezone.utc)),
        "active": 1,
    }
    supa.table("conversation").insert(payload).execute()
    payload["messages"] = []
    return Conversation(**payload)


def db_update_conversation(conversation_id, title):
    supa = supa_client()
    supa.table("conversation").update({"title": title}).eq("conversation_id", conversation_id).execute()
    return db_conversation(conversation_id)


def db_message_feedback(message_id, user_id, feedback):
    supa = supa_client()
    payload = {
        "message_id": message_id,
        "user_id": user_id,
        "created_at": str(datetime.now(timezone.utc)),
        "feedback": feedback,
    }
    supa.table("messagefeedback").insert(payload).execute()


def db_create_message(conversation_id, user_id, role, content):
    supa = supa_client()
    payload = {
        "conversation_id": conversation_id,
        "user_id": user_id,
        "role": role,
        "content": content,
        "created": str(datetime.now(timezone.utc)),
        "date": str(datetime.now(timezone.utc).date()),
    }
    supa.table("message").insert(payload).execute()
