"""
Модуль содержит обработчики основных команд бота.
"""
from telebot.types import Message

from spawn import bot

from .api import create_bookmark
from .utils import log_message, send_message


@bot.message_handler(
    content_types=["text"],
    func=lambda msg: msg.text.lower().lstrip().startswith("http://")
    or msg.text.lower().lstrip().startswith("https://"),
)
def message_url(message: Message) -> None:
    """
    Post link received from user to API to create new bookmark.
    """
    log_message(message=message)
    result = create_bookmark(telegram_id=str(message.chat.id), url=message.text)

    if result:
        reply = "Added link: {url}".format(
            url=result.get("url"),
        )
    else:
        reply = (
            "Something went wrong! It seems that link wasn't added to your bookmarks. "
            "Check your link and try again."
        )

    send_message(message.chat.id, reply)


@bot.message_handler(content_types=["text"])
def message_any(message: Message) -> None:
    """
    В ответ на все остальные сообщения пользователя, не содержащие команды, подсказывает команду помощи.
    :param message: сообщение от пользователя
    """
    log_message(message=message)
    send_message(
        message.chat.id,
        "Send me a link to create new bookmark.\n\nYour Telegram user ID is: {id}\n\n"
        "Set your ID in your user's profile to add links sent to me to your bookmarks.".format(
            id=message.chat.id,
        ),
    )
