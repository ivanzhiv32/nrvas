from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app.application.usecase.faq import FAQList
from app.presentation.handlers.base import IHandler

LIMIT = 4


class FAQHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        usecase = self.ioc.faq_usecase()
        model = usecase.get_faq_list(LIMIT, 0)
        try:
            bot.send_message(
                message.chat.id,
                text='<b>Выберите интересующий вас вопрос</b>',
                parse_mode='HTML',
                reply_markup=self._get_keyboard(model)
            )
        except ValueError:
            bot.send_message(
                message.chat.id,
                text='<b>Скоро будут опубликованы часто задаваемые вопросы</b>',
                parse_mode='HTML',
            )

    def _get_keyboard(
            self,
            model: FAQList,
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
        total_page = (model.total // LIMIT
                      if model.total % LIMIT == 0
                      else model.total // LIMIT + 1)
        if model.total < LIMIT:
            return markup.add(
                InlineKeyboardButton(
                    text=f'{model.offset + 1}/{total_page}',
                    callback_data='  '
                )
            ).add(
                InlineKeyboardButton(
                    text='Скрыть',
                    callback_data='unseen',
                ),
            )
        offset = model.offset + 1
        return markup.add(
            InlineKeyboardButton(
                text=f'{offset}/{total_page}',
                callback_data='  '
            ),
            InlineKeyboardButton(
                text='➡️',
                callback_data=f'{{"method": "faq", '
                              f'"NumberPage": {offset}}}'
            )
        ).add(
            InlineKeyboardButton(
                text='Скрыть',
                callback_data='unseen',
            ),
        )
