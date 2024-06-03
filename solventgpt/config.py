import os

OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

PPLX_API_KEY = os.environ.get("PPLX_API_KEY")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

MODEL_TEMPERATURE = 0.2

# internal tool for product metrics
POSTLANG_API_KEY = "phc_hVraRHsv46wuAz4lIrrN3O7GtfYndA2Aa7eWQMLqrxA"
POSTLANG_HOST = "https://dash.minuva.com"

FUSE_PUBKEY = "pk-lf-48bdc6e8-31f6-4bdd-9bde-01cfcef41ee1"
FUSE_SECKEY = "sk-lf-7de233a2-e803-442f-b0e9-12ac23d164bb"
FUSE_HOST = "https://langfuse.cognitiva.com"

# Old auth (to be removed)
AUTH = [
    ("pedro", "98CmQ8mX5S"),
    ("antonio", "TgUS7svziN"),
    ("user01", "pLJsVDAqY6"),
    ("user02", "98CmQ8mX5S"),
    ("user03", "LtI1vegGPv"),
    ("user04", "1ZxsW8c9u6"),
    ("user05", "TgUS7svziN"),
    ("user06", "1W9ujo1dXD"),
    ("user07", "nzGD8L7Y9d"),
    ("user08", "8jTfKVw3jV"),
    ("user09", "L5GcuNLvFW"),
    ("user10", "hkLYXHDHdR"),
    ("user11", "R5aa81PuqS"),
    ("user12", "S0lC3H46xk"),
    ("user13", "fh9GviqRRr"),
    ("user14", "YNC1zmIODO"),
    ("user15", "SRaMqqjTfZ"),
    ("user16", "6KtKCAus8N"),
    ("user17", "kAwia8q0v6"),
    ("user18", "Lbwq8jW4QC"),
    ("user19", "w7WHyOGRnh"),
    ("user20", "dslaxLSl49"),
]

DEFAULT_MODEL = "gpt-3.5-turbo"

PPLX_ONLINE_MODEL = "llama-3-sonar-large-32k-online"

LLM_MODEL_MAP = {
    "gpt-4": "openai",
    "gpt-4-turbo": "openai",
    "gpt-3.5-turbo": "openai",
    "llama3-8b-8192": "groq",
    "llama3-70b-8192": "groq",
    "mixtral-8x7b-32768": "groq",
    "llama-3-sonar-large-32k-online": "perplexity",  # this is perplexity using OpenAI compatible API
}

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

SQUID_PROXY = f"http://pedro:{os.environ.get('SQUID_PASS')}@159.69.61.40:3128"

SUPABASE_URL = "https://fjvbgsnhdgmkycibwcpj.supabase.co"
SUPABASE_TOKEN = os.environ.get("SUPABASE_TOKEN")

JWT_SECRET = os.environ.get("JWT_SECRET")

PLAN_FREE_LIMIT = 5
PLAN_PRO_LIMIT = 50
PLAN_NO_LIMIT = 9999999

APP_ENV = os.environ["APP_ENV"]
assert APP_ENV in ["dev", "staging", "production"]

INSTANCE = {
    "dev": {
        "url": "https://destined-teal-refined.ngrok-free.app",
        "prices": {
            "pro": "price_1PIbo7KMjAsX28XXV1yqW1f3",
            "premium": "price_1PIe7YKMjAsX28XXievK3K84",
            "lifetime": "price_1PIe9SKMjAsX28XXziZhwTLf",
        },
        "stripe_key": os.environ["STRIPE_KEY"],
    },
    "staging": {
        "url": "https://solventgpt-staging-r5i554wrlq-uc.a.run.app",
        "prices": {
            "pro": "price_1PIbo7KMjAsX28XXV1yqW1f3",
            "premium": "price_1PIe7YKMjAsX28XXievK3K84",
            "lifetime": "price_1PIe9SKMjAsX28XXziZhwTLf",
        },
        "stripe_key": os.environ["STRIPE_KEY"],
    }
}
