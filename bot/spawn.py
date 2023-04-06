"""
Инициализация telebot, Env для использования во всех модулях, где необходима.
"""
import telebot
from environs import Env

env = Env()
env.read_env()

bot = telebot.TeleBot(token=env.str("BOT_TOKEN"))
