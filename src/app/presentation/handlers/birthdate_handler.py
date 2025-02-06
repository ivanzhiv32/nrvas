import datetime as dt

from telebot import TeleBot
from telebot.types import Message

from app.constants import MAX_AGE, MIN_AGE, FORMAT_BIRTHDATE
from app.presentation.buttons import get_main_keyboard
from app.presentation.handlers.base import IHandler
from app.presentation.handlers.surname_handler import SurnameHandler
from app.state import StateRecruitment


class BirthdateHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        chat_id = message.chat.id
        try:
            birthdate = dt.datetime.strptime(
                message.text or '',
                FORMAT_BIRTHDATE
            )
            age = self._calculate_age(birthdate)
            if MIN_AGE > age or MAX_AGE < age:
                self._invalid_age(message, bot)
                return
            self.set_state(
                message,
                bot,
                'birthdate',
                message.text,
                StateRecruitment.birthdate,
            )
            bot.send_message(
                message.chat.id,
                'Напишите Вашу фамилию'
            )
            self.next_handler(message, bot, SurnameHandler(self.ioc))
            bot.delete_message(chat_id=chat_id, message_id=message.id - 1)
        except ValueError:
            self._invalid_birthdate(message, bot)

    def _invalid_age(self, message: Message, bot: TeleBot) -> None:
        user_id = message.from_user.id
        start_command = self.ioc.start_usecase()
        bot.send_message(
            message.chat.id,
            (
                'В Соответствии с положениями п.п."а", пункта 1, статьи 22 '
                '\"Граждане, подлежащие призыву на военную службу\"'
                '\nФедерального закона от 28.03.1998 N 53-ФЗ (ред. от 02.10.2024) '
                '\"О воинской обязанности и военной службе\",'
                'призыву  на  военную службу подлежат граждане мужского пола в '
                'возрасте от 18 до 30 лет, состоящие на воинском учете '
                'или не состоящие, но обязанные состоять на воинском учете и не '
                'пребывающие в запасе '
            ),
            reply_markup=get_main_keyboard(user_id == start_command.id_admin),
        )
        bot.delete_state(user_id=message.from_user.id)

    def _invalid_birthdate(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.chat.id,
            'Введена некорректная дата, попробуйте снова'
        )
        self.next_handler(message, bot, BirthdateHandler(self.ioc))

    def _calculate_age(self, born: dt.datetime) -> int:
        today = dt.date.today()
        return today.year - born.year - (
                (today.month, today.day) < (born.month, born.day)
        )
