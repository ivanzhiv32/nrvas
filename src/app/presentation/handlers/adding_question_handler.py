from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app.domain.question import Question
from app.presentation.handlers.base import IHandler


class AddingQuestionHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.from_user.id,
            'Спасибо за вопрос, он добавлен в базу. '
            'В скором времени на него ответят и Вам придет уведомление.'
        )
        question_id = self._add_question(message.from_user.id, message.text)
        bot.send_message(
            self.ioc.id_admin,
            f'Пользователь @{message.from_user.username} задал вопрос: '
            f'<b>{message.text}</b>',
            reply_markup=self._add_keyboard(question_id),
            parse_mode='HTML'
        )

    def _add_keyboard(self, question_id: int) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        return markup.add(
            InlineKeyboardButton(
                text='Ответить',
                callback_data=f'{{"method": "answer", '
                              f'"index": {question_id}}}',
            ),
            InlineKeyboardButton(
                text='Отложить ответ',
                callback_data='unseen',
            )
        )

    def _add_question(self, user_id: int, question: str) -> int:
        question = Question(
            user_id=str(user_id),
            question=question,
        )
        usecase = self.ioc.question_usecase()
        question_id = usecase.add_question(question)
        return question_id
