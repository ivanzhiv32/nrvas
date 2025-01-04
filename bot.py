import telebot.types
import datetime

from telebot import types
from openpyxl import load_workbook
from time import sleep

TOKEN = '7541371307:AAHfbOo47fs-eSGfVN63CeCg_bUvMKRaIRI'
bot = telebot.TeleBot(TOKEN)

time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
print(f"{time}\nProcessing...")

@bot.message_handler(commands=["start"])
def start(message):
    sticker = open('stickers/welcome_bender.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    welcome_name = f'{message.from_user.first_name} {message.from_user.last_name}'
    welcome_msg = f'Здравствуйте, {welcome_name}\n Я - SciComBot, и я провожу отбор кандидатов в научную роту.\nВыберете интересующий Вас раздел 👇'
    go_to_main_menu(message, welcome_msg)

