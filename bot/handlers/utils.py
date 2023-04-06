"""
Модуль содержит всомогательные функции для обработчиков команд.
"""
import logging

from telebot.types import InlineKeyboardMarkup, Message, ReplyKeyboardMarkup

from spawn import bot


def log_message(message: Message) -> None:
    """
    Записывает в лог сообщение, с указанием username и id отправителя.
    :param message: сообщение от пользователя
    """
    logging.info(
        "@{username} (ID:{user_id}) - {message}".format(
            username=message.from_user.username,
            user_id=message.from_user.id,
            message=message.text,
        )
    )


def send_message(
    chat_id: int | str,
    text: str,
    reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
) -> None:
    """
    Отправляет текстовое сообщение. Функция нужна для сокращения кода, чтобы не повторять везде одни
    и те же параметры: разметка - HTML, без звука, без превью ссылок.
    :param chat_id: id чата, куда отправляется сообщение
    :param text: текст сообщения
    :param reply_markup: клавиатура под сообщением
    """
    bot.send_message(
        chat_id=str(chat_id),
        text=text,
        parse_mode="HTML",
        disable_notification=True,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
    )
