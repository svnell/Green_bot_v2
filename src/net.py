import re
import httpx
from httpx_ntlm import HttpNtlmAuth
from telegram.ext import Application
from src.settings import DOMAIN, USERNAME, PASSWORD

_pattern = re.compile(r'<img[^>]*style="[^"]*border:\s*#66FF66[^"]*"[^>]*>', re.IGNORECASE)


async def ensure_client(app: Application) -> httpx.AsyncClient:
    st = app.bot_data.setdefault("state", None)
    if st is None:
        raise RuntimeError("state not initialized")
    if st.client is None:
        st.client = httpx.AsyncClient(
            verify=False,  # лучше указать CA
            auth=HttpNtlmAuth(f"{DOMAIN}\\{USERNAME}", PASSWORD),
            timeout=15.0,
        )
    return st.client


async def check_page(app: Application, url: str) -> bool:
    client = await ensure_client(app)
    resp = await client.get(url)
    resp.raise_for_status()
    return bool(_pattern.search(resp.text))
