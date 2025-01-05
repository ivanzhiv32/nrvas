from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)


def type_recruitment() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    winter = InlineKeyboardButton('Зимний', callback_data='winter')
    summer = InlineKeyboardButton('Летний', callback_data='summer')
    markup.add(winter, summer)
    return markup


def get_keyboard(is_admin: bool) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    about = KeyboardButton('#О_нас')
    faq = KeyboardButton('FAQ')
    telegram_channel = KeyboardButton('Telegram-канал')
    ask_question = KeyboardButton('Задать вопрос')
    registration = KeyboardButton('Зарегистрироваться')
    documents = KeyboardButton('Руководящие документы')
    question = KeyboardButton('Входящие вопросы')

    if is_admin:
        markup.add(registration).row(
            faq,
            telegram_channel,
            about,
        ).add(documents).add(question)
        return markup
    return markup.add(registration).row(
        faq,
        telegram_channel,
        about,
    ).add(documents).add(ask_question)
