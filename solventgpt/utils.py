from pathlib import Path
import solventgpt.config as cfg


def get_asset(filename):
    pathname = get_asset_path(filename)
    if pathname.exists():
        with open(pathname, encoding="utf8") as file:
            return file.read()
    return ""


def get_asset_path(filename):
    return Path(__file__).parent.parent / "web_assets" / filename


def get_allowed_paths():
    return [str(Path(__file__).parent.parent / "web_assets")]


def api2gr(history):
    """Convert message history api input into gradio format"""
    if len(history) > 0 and history[0].role == "system":
        history = history[1:]
    hist = []
    for idx in range(0, len(history), 2):
        usr, assist = history[idx : idx + 2]
        hist.append((usr.content, assist.content))
    return hist


def get_plan_limit(plan_type):
    if plan_type == "free":
        return cfg.PLAN_FREE_LIMIT
    elif plan_type == "pro":
        return cfg.PLAN_PRO_LIMIT
    elif plan_type in ("premium", "lifetime"):
        return cfg.PLAN_NO_LIMIT
    return 0
