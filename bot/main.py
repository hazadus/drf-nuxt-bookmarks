"""
Telegram bot to add bookmarks via DRF API.
Run `python main.py` to start the bot.
"""
import logging
import sys

from handlers import common
from spawn import bot

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bkmrks-bot.log"),
        logging.StreamHandler(sys.stdout),  # output to file AND console
    ],
    format="%(asctime)s | %(levelname)s | %(module)s/%(funcName)s():%(lineno)d - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)


# Run the bot
bot.infinity_polling(logger_level=logging.INFO)
logging.info("Bot started.")
