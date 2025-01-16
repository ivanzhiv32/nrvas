from telebot import TeleBot, StateMemoryStorage

from app.config import load_bot_secret
from app.constants import BASE_DIR
from app.ioc import IoC
from app.presentation.callbacks import (
    RecruitmentCallback,
    NationalityCallback,
    UniversityCallback,
    UnseenCallback,
    PaginateCallback,
    QuestionCallback,
)
from app.presentation.handlers import (
    StartHandler,
    TypeRecruitmentHandler,
    TelegramChannelHandler,
    IncomingQuestionHandler,
    QuestionHandler,
    FaqHandler,
    DocumentHandler,
    IDHandler,
)


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
    bot.register_callback_query_handler(
        UnseenCallback(ioc),
        func=lambda call: call.data == 'unseen',
        pass_bot=True,
    )
    bot.register_callback_query_handler(
        PaginateCallback(ioc),
        func=lambda call: call.data == 'pagination',
        pass_bot=True,
    )
    bot.register_callback_query_handler(
        QuestionCallback(ioc),
        func=lambda call: call.data == 'question',
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
        TypeRecruitmentHandler(ioc),
        content_types=['text'],
        func=lambda message: message.text == 'Зарегистрироваться',
        pass_bot=True,
    )
    bot.register_message_handler(
        TelegramChannelHandler(ioc),
        content_types=['text'],
        func=lambda message: message.text == 'Telegram-канал',
        pass_bot=True,
    )
    bot.register_message_handler(
        IncomingQuestionHandler(ioc),
        content_types=['text'],
        func=lambda message: message.text == 'Входящие вопросы',
        pass_bot=True,
    )
    bot.register_message_handler(
        QuestionHandler(ioc),
        content_types=['text'],
        func=lambda message: message.text == 'Задать вопрос',
        pass_bot=True,
    )
    bot.register_message_handler(
        FaqHandler(ioc),
        content_types=['text'],
        func=lambda message: message.text == 'FAQ',
        pass_bot=True,
    )
    bot.register_message_handler(
        DocumentHandler(ioc),
        content_types=['text'],
        func=lambda message: message.text == 'Руководящие документы',
        pass_bot=True,
    )
    bot.register_message_handler(
        IDHandler(ioc),
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
