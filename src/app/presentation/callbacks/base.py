from abc import ABC, abstractmethod

from telebot import TeleBot
from telebot.types import CallbackQuery, Message

from app.presentation.handlers.base import IHandler
from app.presentation.interactor import InteractorFactory


class ICallback(ABC):
    def __init__(self, ioc: InteractorFactory) -> None:
        self.ioc = ioc

    @abstractmethod
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None: ...

    def next_handler(
            self,
            message: Message,
            bot: TeleBot,
            handler: 'IHandler'
    ) -> None:
        bot.register_next_step_handler(
            message,
            handler,
            bot=bot,
        )