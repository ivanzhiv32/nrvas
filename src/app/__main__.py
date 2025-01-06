from telebot import TeleBot

from app.config import BotConfig, load_bot_secret
from app.constants import BASE_DIR
from app.handlers.documents_handler import documents_handler
from app.handlers.faq_handler import faq_handler
from app.handlers.id_handler import id_handler
from app.handlers.question_handler import incoming_question_handler, question_handler
from app.handlers.recruitment_handler import type_recruitment_handler
from app.handlers.start_handler import StartHandler
from app.handlers.telegram_handler import telegram_channel_handler


def register_handlers(bot: TeleBot, config: BotConfig) -> None:
    bot.register_message_handler(
        StartHandler(
            dir_sticker=BASE_DIR / 'stickers/welcome_bender.tgs',
            id_admin=config.id_admin,
        ),
        commands=['start'],
        pass_bot=True,
    )
    bot.register_message_handler(
        type_recruitment_handler,
        content_types=['text'],
        func=lambda message: message.text == 'Зарегистрироваться',
        pass_bot=True,
    )
    bot.register_message_handler(
        telegram_channel_handler,
        content_types=['text'],
        func=lambda message: message.text == 'Telegram-канал',
        pass_bot=True,
    )
    bot.register_message_handler(
        incoming_question_handler,
        content_types=['text'],
        func=lambda message: message.text == 'Входящие вопросы',
        pass_bot=True,
    )
    bot.register_message_handler(
        question_handler,
        content_types=['text'],
        func=lambda message: message.text == 'Задать вопрос',
        pass_bot=True,
    )
    bot.register_message_handler(
        faq_handler,
        content_types=['text'],
        func=lambda message: message.text == 'FAQ',
        pass_bot=True,
    )
    bot.register_message_handler(
        documents_handler,
        content_types=['text'],
        func=lambda message: message.text == 'Руководящие документы',
        pass_bot=True,
    )
    bot.register_message_handler(
        id_handler,
        content_types=['text'],
        func=lambda message: message.text == 'id',
        pass_bot=True,
    )


def main():
    bot_config = load_bot_secret()
    bot = TeleBot(
        token=bot_config.token,
    )
    register_handlers(bot, bot_config)

    bot.polling()


if __name__ == "__main__":
    main()
