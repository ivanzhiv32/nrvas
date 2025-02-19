from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
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
    promo = KeyboardButton('Промо')

    if is_admin:
        return markup.row(
            faq,
            telegram_channel,
            about,
        ).add(promo).add(documents).add(question)
    return markup.add(registration).row(
        faq,
        telegram_channel,
        about,
    ).add(promo).add(documents).add(ask_question)
