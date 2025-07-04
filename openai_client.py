import asyncio
import os

import httpx
import openai
from dotenv import load_dotenv

SYSTEM_PROMPT = (
    "Ты музыкальный критик. Проанализируй список треков и опиши музыкальные вкусы пользователя: "
    "предпочитаемые жанры, основные мотивы, характерные исполнители, общее настроение. Скажи, что вообще думаешь об этом списке музыки."
    "Ответь на русском простыми абзацами без кавычек, без маркдауна, без списков и заголовков."
)

load_dotenv()

# Prepare OpenAI client with proxy
api_key = os.getenv("OPENAI_API_KEY")
proxy_url = "http://JuTqmCNApNGz7n:dzera.nat.i@216.107.136.148:42204"

# Собираем URL прокси

transport = httpx.HTTPTransport(proxy=proxy_url)          # ← ключевой параметр
client     = httpx.Client(transport=transport, trust_env=False)

# ----- асинхронный клиент -----
# transport = httpx.AsyncHTTPTransport(proxy=proxy_url)
# client    = httpx.AsyncClient(transport=transport, trust_env=False)


openai_client = openai.OpenAI(api_key=api_key, http_client=client)


# --- OpenAI query ---
async def ask_chatgpt(tracks_text: str) -> str:
    response = await asyncio.to_thread(
        openai_client.chat.completions.create,
        model="gpt-4o-mini",          # или другой поддерживаемый text-model
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": tracks_text}
        ],
        max_tokens=1000,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()