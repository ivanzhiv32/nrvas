from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton,
)


def get_main_keyboard(is_admin: bool) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=3,
        one_time_keyboard=False,
    )

    about = KeyboardButton('#О_нас')
    faq = KeyboardButton('FAQ')
    telegram_channel = KeyboardButton('Telegram-канал')
    ask_question = KeyboardButton('Задать вопрос')
    registration = KeyboardButton('Зарегистрироваться')
    documents = KeyboardButton('Руководящие документы')
    question = KeyboardButton('Входящие вопросы')

    if is_admin:
        return markup.add(registration).row(
            faq,
            telegram_channel,
            about,
        ).add(documents).add(question)
    return markup.add(registration).row(
        faq,
        telegram_channel,
        about,
    ).add(documents).add(ask_question)


def get_nationality_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(
            'Да',
            callback_data='yes_russian'
        ),
        InlineKeyboardButton(
            'Нет',
            callback_data='no_russian'
        )
    )


def get_university_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(
            'Да',
            callback_data='yes_university'
        ),
        InlineKeyboardButton(
            'Нет',
            callback_data='no_university'
        )
    )
