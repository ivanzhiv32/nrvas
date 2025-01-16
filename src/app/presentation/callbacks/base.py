from abc import ABC, abstractmethod

from telebot import TeleBot
from telebot.types import CallbackQuery

from app.presentation.interactor import InteractorFactory


class ICallback(ABC):
    def __init__(self, ioc: InteractorFactory) -> None:
        self.ioc = ioc

    @abstractmethod
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None: ...
