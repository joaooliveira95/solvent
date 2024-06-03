from typing import Optional
import markdown
from bs4 import BeautifulSoup


def strip_markdown(md: str) -> Optional[str]:
    html = markdown.markdown(md)
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text()
