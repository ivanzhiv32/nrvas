from telebot import TeleBot, StateMemoryStorage

from app.adapter.persistence.db import create_session_maker
from app.config import load_config
from app.constants import BASE_DIR
from app.ioc import IoC
from app.presentation.callbacks import (
    RecruitmentCallback,
    NationalityCallback,
    UniversityCallback,
    UnseenCallback,
    FAQCallback,
    QuestionCallback,
    AnswerFAQCallback,
)
from app.presentation.handlers import (
    StartHandler,
    TypeRecruitmentHandler,
    TelegramChannelHandler,
    IncomingQuestionHandler,
    QuestionHandler,
    FAQHandler,
    DocumentHandler,
    IDHandler,
    AboutHandler,
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
        FAQCallback(ioc),
        func=lambda call: 'faq' in call.data,
        pass_bot=True,
    )
    bot.register_callback_query_handler(
        AnswerFAQCallback(ioc),
        func=lambda call: 'answerFAQ' in call.data,
        pass_bot=True,
    )
    bot.register_callback_query_handler(
        QuestionCallback(ioc),
        func=lambda call: 'question' in call.data,
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
        FAQHandler(ioc),
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
    bot.register_message_handler(
        AboutHandler(ioc),
        content_types=['text'],
        func=lambda message: message.text == '#О_нас',
        pass_bot=True,
    )


def main():
    bot_config = load_config()
    state_storage = StateMemoryStorage()
    bot = TeleBot(
        token=bot_config.token,
        state_storage=state_storage,
        use_class_middlewares=True,
    )
    ioc = IoC(
        path=BASE_DIR,
        id_admin=bot_config.id_admin,
        db_url=bot_config.database,
    )

    register_callbacks(bot, ioc)
    register_handlers(bot, ioc)

    bot.polling()


if __name__ == "__main__":
    main()
