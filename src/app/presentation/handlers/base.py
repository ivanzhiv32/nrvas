from abc import ABC, abstractmethod
from typing import Any

from telebot import TeleBot, State
from telebot.types import Message

from app.presentation.interactor import InteractorFactory


class IHandler(ABC):
    def __init__(self, ioc: InteractorFactory) -> None:
        self.ioc = ioc

    @abstractmethod
    def __call__(
            self,
            message: Message,
            bot: TeleBot,
    ) -> None: ...

    def set_state(
            self,
            message: Message,
            bot: TeleBot,
            key: str,
            value: str | None,
            state: State,
    ) -> None:
        user_id = message.from_user.id
        bot.set_state(user_id, state)
        with bot.retrieve_data(user_id) as data:
            data[key] = value

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
