import logging

from telegram import Update
from telegram.ext import ContextTypes

from bot import URL_PATTERN

from openai_client import ask_chatgpt
from yandex_client import get_playlist

logger = logging.getLogger(__name__)

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    match = URL_PATTERN.match(text)
    if not match:
        await update.message.reply_text(
            "❌ Неверная ссылка. Отправьте в формате:\n" +
            "https://music.yandex.com/users/USERNAME/playlists/ID"
        )
        return
    username = match.group("username")
    playlist_id = match.group("playlist_id")
    await update.message.reply_text(
        f"🔄 Обработка плейлиста пользователя <b>{username}</b>, ID <b>{playlist_id}</b>...",
        parse_mode="HTML"
    )
    # Дальнейшая логика: context.user_data или return
    context.user_data['username'] = username
    context.user_data['playlist_id'] = playlist_id
    # Можно вернуть кортеж для дальнейшей цепочки
    return username, playlist_id

async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем и разбираем ссылку
    username, playlist_id = await handle_link(update, context)
    if not username or not playlist_id:
        return

    # Получаем текст плейлиста
    playlist_text = get_playlist(username, playlist_id)
    if not playlist_text:
        await update.message.reply_text("📭 Плейлист пуст или не найден.")
        return

    # Отправляем текст в ChatGPT и ждем ответ
    await update.message.reply_text("🤖 Отправка данных в ChatGPT...")
    result = await ask_chatgpt(playlist_text)

    # Выводим результат пользователю
    await update.message.reply_text(result)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Отправьте ссылку на ваши любимые песни в Яндекс.Музыке.\n"
    )