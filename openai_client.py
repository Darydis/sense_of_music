import asyncio
import os

import httpx
import openai
from dotenv import load_dotenv

load_dotenv()

# Prepare OpenAI client with proxy
api_key = os.getenv("OPENAI_API_KEY")
prompt = os.getenv("SYSTEM_PROMPT")
proxy_url = os.getenv("proxy_url")

# Собираем URL прокси

transport  = httpx.HTTPTransport(proxy=httpx.Proxy(proxy_url))
client     = httpx.Client(transport=transport, trust_env=False)

# ----- асинхронный клиент -----
# transport = httpx.AsyncHTTPTransport(proxy=proxy_url)
# client    = httpx.AsyncClient(transport=transport, trust_env=False)


openai_client = openai.OpenAI(api_key=api_key, http_client=client)


# --- OpenAI query ---
async def ask_chatgpt(tracks_text: str) -> str:
    response = await asyncio.to_thread(
        openai_client.chat.completions.create,
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user",   "content": tracks_text}
        ],
        max_tokens=1000,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()