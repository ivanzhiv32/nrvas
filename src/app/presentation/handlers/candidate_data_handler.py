import datetime
import datetime as dt
from abc import ABC, abstractmethod
from collections.abc import Callable

from telebot import TeleBot
from telebot.types import Message

from app.constants import MAX_AGE, MIN_AGE, FORMAT_BIRTHDATE
from app.exceptions import ScoreException
from app.presentation.buttons import get_phone_keyboard
from app.presentation.interactor import InteractorFactory
from app.state import StateRecruitment


class BirthdateHandler:
    def __init__(self, ioc: InteractorFactory) -> None:
        self.ioc = ioc

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
            bot.send_message(
                message.chat.id,
                'Напишите Вашу фамилию'
            )
            bot.register_next_step_handler(
                message,
                SurnameCandidateHandler(self.ioc),
                bot=bot
            )
            bot.delete_message(chat_id=chat_id, message_id=message.id - 1)
            self._set_state(message, bot)
        except ValueError:
            self._invalid_birthdate(message, bot)

    def _set_state(self, message: Message, bot: TeleBot) -> None:
        user_id = message.from_user.id
        bot.set_state(user_id, StateRecruitment.birthdate)
        with bot.retrieve_data(user_id) as data:
            data['birthdate'] = message.text

    def _invalid_age(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.chat.id,
            (
                'В Соответствии с положениями п.п."а", пункта 1, статьи 22 \"Граждане, подлежащие призыву на военную службу\"'
                '\nФедерального закона от 28.03.1998 N 53-ФЗ (ред. от 02.10.2024) \"О воинской обязанности и военной службе\",'
                'призыву  на  военную службу подлежат граждане мужского пола в возрасте от 18 до 30 лет, состоящие на воинском учете '
                'или не состоящие, но обязанные состоять на воинском учете и не пребывающие в запасе '
            ),
        )
        bot.delete_state(user_id=message.from_user.id)

    def _invalid_birthdate(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.chat.id,
            'Введена некорректная дата, попробуйте снова'
        )
        bot.register_next_step_handler(
            message,
            BirthdateHandler(self.ioc),
            bot=bot
        )

    def _calculate_age(self, born: datetime.datetime) -> int:
        today = dt.date.today()
        return today.year - born.year - (
                (today.month, today.day) < (born.month, born.day)
        )


class BaseCandidateHandler(ABC):
    def __init__(self, ioc: InteractorFactory) -> None:
        self.ioc = ioc

    def get_methods(self) -> list[Callable[[Message, TeleBot], None]]:
        return [
            self._set_state,
            self._send_message,
            self._next_handler
        ]

    def __call__(self, message: Message, bot: TeleBot) -> None:
        for func in self.get_methods():
            func(message, bot)

    @abstractmethod
    def _next_handler(self, message: Message, bot: TeleBot) -> None: ...

    @abstractmethod
    def _send_message(self, message: Message, bot: TeleBot) -> None: ...

    @abstractmethod
    def _set_state(self, message: Message, bot: TeleBot) -> None: ...


class SurnameCandidateHandler(BaseCandidateHandler):
    def _send_message(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(message.from_user.id, 'Напишите Ваше имя')

    def _next_handler(self, message: Message, bot: TeleBot) -> None:
        bot.register_next_step_handler(
            message,
            NameCandidateHandler(self.ioc),
            bot=bot
        )
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)

    def _set_state(self, message: Message, bot: TeleBot) -> None:
        user_id = message.from_user.id
        bot.set_state(user_id, StateRecruitment.surname)
        with bot.retrieve_data(user_id) as data:
            data['surname'] = message.text


class NameCandidateHandler(BaseCandidateHandler):
    def _set_state(self, message: Message, bot: TeleBot) -> None:
        user_id = message.from_user.id
        bot.set_state(user_id, StateRecruitment.name)
        with bot.retrieve_data(user_id) as data:
            data['name'] = message.text

    def _next_handler(self, message: Message, bot: TeleBot) -> None:
        bot.register_next_step_handler(
            message,
            PatronymicCandidateHandler(self.ioc),
            bot=bot
        )
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)

    def _send_message(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(message.from_user.id, 'Напишите Ваше отчество')


class PatronymicCandidateHandler(BaseCandidateHandler):
    def _set_state(self, message: Message, bot: TeleBot) -> None:
        bot.set_state(message.chat.id, StateRecruitment.patronymic)
        with bot.retrieve_data(message.from_user.id) as data:
            data['patronymic'] = message.text

    def _next_handler(self, message: Message, bot: TeleBot) -> None:
        bot.register_next_step_handler(
            message,
            MilitaryStationCandidateHandler(self.ioc),
            bot=bot
        )
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)

    def _send_message(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.from_user.id,
            'Напишите название своего военного комиссариата'
        )


class MilitaryStationCandidateHandler(BaseCandidateHandler):
    def _set_state(self, message: Message, bot: TeleBot) -> None:
        bot.set_state(message.chat.id, StateRecruitment.military_station)
        with bot.retrieve_data(message.from_user.id) as data:
            data['military_station'] = message.text

    def _next_handler(self, message: Message, bot: TeleBot) -> None:
        bot.register_next_step_handler(
            message,
            UniversityCandidateHandler(self.ioc),
            bot=bot
        )
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)

    def _send_message(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(message.from_user.id, 'Напишите название своего ВУЗа')


class UniversityCandidateHandler(BaseCandidateHandler):
    def _set_state(self, message: Message, bot: TeleBot) -> None:
        bot.set_state(message.chat.id, StateRecruitment.university)
        with bot.retrieve_data(message.from_user.id) as data:
            data['university'] = message.text

    def _send_message(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.from_user.id,
            'Напишите направление подготовки в ВУЗе'
        )

    def _next_handler(self, message: Message, bot: TeleBot) -> None:
        bot.register_next_step_handler(
            message,
            FieldStudyCandidateHandler(self.ioc),
            bot=bot
        )
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)


class FieldStudyCandidateHandler(BaseCandidateHandler):
    def _next_handler(self, message: Message, bot: TeleBot) -> None:
        bot.register_next_step_handler(
            message,
            AverageScoreCandidateHandler(self.ioc),
            bot=bot
        )
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)

    def _set_state(self, message: Message, bot: TeleBot) -> None:
        bot.set_state(message.chat.id, StateRecruitment.field_study)
        with bot.retrieve_data(message.from_user.id) as data:
            data['field_study'] = message.text

    def _send_message(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.from_user.id,
            'Напишите средний балл по диплому (х.х)'
        )


class AverageScoreCandidateHandler:
    def __init__(self, ioc: InteractorFactory) -> None:
        self.ioc = ioc

    def __call__(self, message: Message, bot: TeleBot) -> None:
        try:
            score = float(message.text.replace(',', '.'))
            user_id = message.from_user.id
            if score < 4:
                bot.send_message(
                    user_id,
                    'Ваш средний балл не соответствует требованиям.\n'
                    'В научную роту рассматриваются кандидаты со средним баллом не менее 4.0'
                )
                raise ScoreException()
            elif score > 5:
                bot.send_message(
                    user_id,
                    'Введен некорректный балл, попробуйте снова'
                )
                bot.register_next_step_handler(
                    message,
                    AverageScoreCandidateHandler(self.ioc),
                    bot=bot
                )
            self._set_state(message, bot)
            self._set_message(message, bot)
            self._next_handler(message, bot)
        except ValueError:
            self._invalid_score_message(message, bot)
        except ScoreException:
            pass

    def _set_message(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(message.from_user.id, 'Откуда Вы узнали о нас?')

    def _set_state(self, message: Message, bot: TeleBot) -> None:
        bot.set_state(message.chat.id, StateRecruitment.average_score)
        with bot.retrieve_data(message.from_user.id) as data:
            data['average_score'] = message.text

    def _invalid_score_message(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.from_user.id,
            'Введен некорректный балл, попробуйте снова'
        )
        bot.register_next_step_handler(
            message,
            AverageScoreCandidateHandler(self.ioc),
            bot=bot
        )

    def _next_handler(self, message: Message, bot: TeleBot) -> None:
        bot.register_next_step_handler(
            message,
            PhoneCandidateHandler(self.ioc),
            bot=bot
        )
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)


class PhoneCandidateHandler(BaseCandidateHandler):
    def _send_message(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.chat.id,
            parse_mode='HTML',
            text='Для связи с вами, нам необходимо получить ваш номер телефона. '
                 'Нажмите кнопку в меню или напишите его в чат',
            reply_markup=get_phone_keyboard()
        )

    def _next_handler(self, message: Message, bot: TeleBot) -> None:
        bot.register_next_step_handler(
            message,
            SendingDocHandler(self.ioc),
            bot=bot
        )
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)

    def _set_state(self, message: Message, bot: TeleBot) -> None:
        bot.set_state(message.chat.id, StateRecruitment.find_out)
        with bot.retrieve_data(message.from_user.id) as data:
            data['phone'] = message.text


class SendingDocHandler:
    def __init__(self, ioc: InteractorFactory) -> None:
        self.ioc = ioc

    def __call__(self, message: Message, bot: TeleBot) -> None:
        phone = message.contact.phone_number
        self._send_message(message, bot)
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
        self._send_documents(message, bot)

    def _send_message(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.from_user.id,
            'Поздравляем, ваша кандидатура будет рассмотрена для поступления '
            'в научную роту Военной академеии связи им С.М. Буденного'
        )

    def _send_documents(self, message: Message, bot: TeleBot) -> None:
        chat_id = message.chat.id
        path = self.ioc.path
        with open(path / r'documents/Лист собеседования.docx', 'rb') as file:
            bot.send_document(chat_id, path)

        with open(path / r'documents/Согласие.docx', 'rb') as file:
            bot.send_document(chat_id, path)
