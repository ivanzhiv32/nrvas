from telebot import TeleBot, StateMemoryStorage

from app.config import load_bot_secret
from app.constants import BASE_DIR
from app.ioc import IoC
from app.presentation.callbacks import (
    RecruitmentCallback,
    NationalityCallback,
    UniversityCallback,
)
from app.presentation.handlers.documents_handler import documents_handler
from app.presentation.handlers.faq_handler import faq_handler
from app.presentation.handlers.id_handler import id_handler
from app.presentation.handlers.question_handler import (
    incoming_question_handler,
    question_handler,
)
from app.presentation.handlers.recruitment_handler import (
    type_recruitment_handler
)
from app.presentation.handlers.start_handler import StartHandler
from app.presentation.handlers.telegram_handler import telegram_channel_handler


def register_callbacks(bot: TeleBot, ioc: IoC) -> None:
    bot.register_callback_query_handler(
        RecruitmentCallback(ioc),
        func=lambda call: call.data in ('winter', 'summer'),
        pass_bot=True,
    )
    bot.register_callback_query_handler(
        NationalityCallback(ioc),
        func=lambda call: call.data in ('yes_russian', 'no_russian'),
        pass_bot=True,
    )
    bot.register_callback_query_handler(
        UniversityCallback(ioc),
        func=lambda call: call.data in ('yes_university', 'no_university'),
        pass_bot=True,
    )


def register_handlers(
        bot: TeleBot,
        ioc: IoC,
) -> None:
    bot.register_message_handler(
        StartHandler(ioc=ioc),
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
    state_storage = StateMemoryStorage()
    bot = TeleBot(
        token=bot_config.token,
        state_storage=state_storage,
        use_class_middlewares=True,
    )
    ioc = IoC(path=BASE_DIR, id_admin=bot_config.id_admin)

    register_callbacks(bot, ioc)
    register_handlers(bot, ioc)

    bot.polling()


if __name__ == "__main__":
    main()
