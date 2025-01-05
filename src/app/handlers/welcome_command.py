from typing import Any

from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app.buttons import type_recruitment
from app.utils import excel_to_2d_array


class WelcomeCommand:
    def __init__(self, bot: TeleBot, ) -> None:
        self.bot = bot

    def __call__(self, message: Message) -> None:
        try:
            self._get_text_command(message)[message.text]
        except KeyError:
            pass

    def _get_text_command(self, message: Message) -> dict[str, Any]:
        return {
            'Зарегистрироваться': self._get_register_text(message),
            'Telegram-канал': self._get_telegram_channel_text(message),
            'Входящие вопросы': self._get_incoming_question_text(message),
            'FAQ': self._get_faq_text(message),
            'Руководящие документы': self._get_documents_text(message),
            'Задать вопрос': ...,
            'id': ...
        }

    def _get_register_text(self, message: Message) -> None:
        self.bot.send_message(
            message.chat.id,
            'На какой призыв Вы хотите оставить заявку?',
            reply_markup=type_recruitment()
        )

    def _get_telegram_channel_text(self, message: Message) -> None:
        self.bot.send_message(
            message.chat.id,
            'https://t.me/+ntFED2PMwUo2MDZi',
        )

    def _get_incoming_question_text(self, message: Message) -> None:
        df = excel_to_2d_array('questions.xlsx')
        page = 1
        count = len(df) - 1

        markup = InlineKeyboardMarkup()

        markup.add(
            InlineKeyboardButton(
                text='Ответить',
                callback_data=f'{{"method":"answer", '
                              f'"NumberPage:{page}}}',
            )
        )
        markup.add(
            InlineKeyboardButton(
                text=f'{page}/{count}',
                callback_data='  '
            ),
            InlineKeyboardButton(
                text='Вперёд --->',
                callback_data=f'{{"method":"questions", '
                              f'"NumberPage":{page + 1}, '
                              f'"CountPage"{count}}}'
            )
        )

        self.bot.send_message(
            message.from_user.id,
            f'<b>{df[3][page]}</b>\n\n',
            parse_mode='HTML',
            reply_markup=markup,
        )

    def _get_faq_text(self, message: Message) -> None:
        df = excel_to_2d_array('faq.xlsx')
        page = 1

        count = (len(df) - 1) // 4
        if (len(df) - 1) % 4 != 0:
            count += 1

        markup = InlineKeyboardMarkup()
        i = 1
        while i <= 4:
            question = df[1][i]
            answer = df[2][i]
            markup.add(
                InlineKeyboardButton(
                    text=question,
                    callback_data=f'{{"method":"question", "index": {i}}}',
                )
            )
            i += 1
        markup.add(
            InlineKeyboardButton(
                text='Скрыть',
                callback_data='unseen'
            )
        )
        markup.add(
            InlineKeyboardButton(
                text=f'{page}/{count}',
                callback_data=' '
            ),
            InlineKeyboardButton(
                text='Вперёд --->',
                callback_data=f'{{"method": "question", '
                              f'"NumberPage": {page + 1}, '
                              f'"IndexQuestion": {i}}}'
            )
        )
        self.bot.send_message(
            message.chat.id,
            text=f'<b>Выберите интересующий вас вопрос</b>', parse_mode="HTML",
            reply_markup=markup
        )

    def _get_documents_text(self, message: Message) -> None:
        markup = InlineKeyboardMarkup()

        markup.add(
            InlineKeyboardButton(
                'Ссылка',
                url='https://www.consultant.ru/document/cons_doc_LAW_18260/'
            )
        )

        self.bot.send_message(
            message.chat.id,
            text='ФЗ № 53 «О воинской обязанности и военной службе» от 28.03.1998 (ред. 02.10.2024)',
            reply_markup=markup
        )

    def _get_question_text(self, message: Message) -> None:
        self.bot.send_message(
            message.from_user.id,
            'Отправьте интересующий вас вопрос',
        )
        # TODO: функционал для задать вопрос
        self.bot.register_next_step_handler(
            message,

        )
