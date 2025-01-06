from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app.constants import BASE_DIR
from main import excel_to_2d_array


def faq_handler(message: Message, bot: TeleBot) -> None:
    filename = 'faq.xlsx'
    df = excel_to_2d_array(BASE_DIR / filename)
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
    bot.send_message(
        message.chat.id,
        text=f'<b>Выберите интересующий вас вопрос</b>',
        parse_mode="HTML",
        reply_markup=markup
    )
