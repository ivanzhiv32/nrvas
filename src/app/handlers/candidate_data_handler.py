import datetime as dt

from telebot import TeleBot
from telebot.types import Message

from app.constants import MILITARY_SERVICE
from app.state import StateRecruitment

FORMAT_BIRTHDATE = '%d.%m.%Y'


def birthdate_handler(message: Message, bot: TeleBot) -> None:
    # TODO: нужен рефакторинг ручки
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        birthdate = dt.datetime.strptime(message.text or '', "%d.%m.%Y")
        age = dt.datetime.now().year - birthdate.year - (
                (dt.datetime.now().month, dt.datetime.now().day) < (birthdate.month, birthdate.day)
        )
        if age < 18 or age > 30:
            bot.send_message(
                chat_id,
                MILITARY_SERVICE,
            )
            return
        bot.send_message(
            chat_id,
            'Напишите Вашу фамилию'
        )
        bot.register_next_step_handler(message, candidate_surname_handler, bot=bot)
        bot.delete_message(chat_id=chat_id, message_id=message.id - 1)
        bot.set_state(user_id, StateRecruitment.birthdate)
        with bot.retrieve_data(user_id) as data:
            data['birthdate'] = message.text
    except ValueError:
        bot.send_message(chat_id,
                         'Введена некорректная дата, попробуйте снова')
        bot.register_next_step_handler(message, birthdate_handler, bot=bot)


def candidate_surname_handler(message: Message, bot: TeleBot) -> None:
    surname = message.text
    user_id = message.from_user.id
    bot.send_message(user_id, 'Напишите ваше имя')
    bot.set_state(user_id, StateRecruitment.birthdate)
    with bot.retrieve_data(user_id) as data:
        data['surname'] = surname
    bot.register_next_step_handler(message, candidate_name_handler, bot=bot)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)


def candidate_name_handler(message: Message, bot: TeleBot) -> None:
    name = message.text
    user_id = message.from_user.id
    bot.send_message(user_id, 'Напишите ваше отчество')
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)