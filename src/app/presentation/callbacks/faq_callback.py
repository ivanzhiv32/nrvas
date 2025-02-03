import json
from typing import Any

from telebot import TeleBot
from telebot.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.application.usecase.faq import FAQList
from app.presentation.callbacks.base import ICallback

LIMIT = 4


class FAQCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        data = json.loads(call.data)
        usecase = self.ioc.faq_usecase()
        offset = data['NumberPage']
        model = usecase.get_faq_list(LIMIT, offset)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            text='<b>Выберите интересующий Вас вопрос:</b>',
            parse_mode='HTML',
            reply_markup=self._add_keyboard(model, data),
            message_id=call.message.message_id,
        )

    def _add_keyboard(
            self,
            model: FAQList,
            data: dict[str, Any],
    ) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        for _, value in enumerate(model.faq):
            markup.add(
                InlineKeyboardButton(
                    text=value.question,
                    callback_data=f'{{"method": "answerFAQ", '
                                  f'"index": {value.id}}}',
                )
            )
        offset = data['NumberPage']
        if len(model.faq) < model.limit or model.faq == 0:
            return markup.add(
                InlineKeyboardButton(
                    text='<--- Назад',
                    callback_data=f'{{"method": "faq", '
                                  f'"NumberPage": {offset - 1}}}'
                ),
                InlineKeyboardButton(
                    text='Скрыть',
                    callback_data='unseen',
                )
            )
        elif offset > 0:
            return markup.add(
                InlineKeyboardButton(
                    text='<--- Назад',
                    callback_data=f'{{"method": "faq", '
                                  f'"NumberPage": {offset - 1}}}'
                ),
                InlineKeyboardButton(
                    text='Скрыть',
                    callback_data='unseen',
                ),
                InlineKeyboardButton(
                    text='Вперёд --->',
                    callback_data=f'{{"method": "faq", '
                                  f'"NumberPage": {offset + 1}}}'
                )
            )
        return markup.add(
            InlineKeyboardButton(
                text='Скрыть',
                callback_data='unseen',
            ),
            InlineKeyboardButton(
                text='Вперёд --->',
                callback_data=f'{{"method": "faq", '
                              f'"NumberPage": {offset + 1}}}'
            )
        )


class AnswerFAQCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        usecase = self.ioc.faq_usecase()
        data = json.loads(call.data)
        model = usecase.get_faq(data['index'])
        bot.send_message(
            chat_id=call.message.chat.id,
            text=model.answer,
        )
