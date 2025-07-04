import logging
import os
import re

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

import handlers

URL_PATTERN = re.compile(
    r"^https://music\.yandex\.ru/users/(?P<username>[A-Za-z0-9_-]+)/playlists/(?P<playlist_id>\d+)(?:\?.*)?$"
)

def main() -> None:
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        raise RuntimeError('BOT_TOKEN not set')
    logging.basicConfig(level=logging.INFO)

    app = Application.builder().token(bot_token).build()
    app.add_handler(CommandHandler('start', handlers.start))
    app.add_handler(
        MessageHandler(
            filters.Regex(URL_PATTERN) & ~filters.COMMAND,
            handlers.process_message
        )
    )
    app.run_polling()


if __name__ == '__main__':
    main()
