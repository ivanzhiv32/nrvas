from telebot import TeleBot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from app.presentation.interactor import InteractorFactory


class PromoHandler:
    def __init__(self, ioc: InteractorFactory) -> None:
        self.ioc = ioc

    def __call__(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.chat.id,
            text='Выберите интересующие Вас промо материалы:',
            reply_markup=self._get_keyboard()
        )

    def _get_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                'Брошюра',
                callback_data='promo_brochure'
            )
        ).add(
            InlineKeyboardButton(
                'Стенд',
                callback_data='promo_stand'
            )
        ).add(
            InlineKeyboardButton(
                'Визитка',
                callback_data='promo_card'
            )
        )
        # ).add(
        #     InlineKeyboardButton(
        #         'Видео',
        #         callback_data='promo_video'
        #     )
        # )