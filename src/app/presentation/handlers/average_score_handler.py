from telebot import TeleBot
from telebot.types import Message

from app.exceptions import ScoreException
from app.presentation.handlers.base import IHandler
from app.presentation.handlers.find_out_handler import FindOutHandler
from app.state import StateRecruitment


class AverageScoreHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        try:
            score = float(message.text.replace(',', '.'))
            user_id = message.from_user.id
            if score < 4:
                bot.send_message(
                    user_id,
                    'Ваш средний балл не соответствует требованиям.\n'
                    'В научную роту рассматриваются кандидаты со средним баллом не менее 4.0'
                )
                raise ScoreException()
            elif score > 5:
                bot.send_message(
                    user_id,
                    'Введен некорректный балл, попробуйте снова'
                )
                self.next_handler(message, bot, AverageScoreHandler(self.ioc))
            self.set_state(
                message,
                bot,
                'average_score',
                message.text,
                StateRecruitment.average_score
            )
            bot.send_message(message.from_user.id, 'Откуда Вы узнали о нас?')
            self.next_handler(message, bot, FindOutHandler(self.ioc))
            bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.id - 1
            )
        except ValueError:
            self._invalid_score_message(message, bot)
        except ScoreException:
            pass

    def _invalid_score_message(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.from_user.id,
            'Введен некорректный балл, попробуйте снова'
        )
        self.next_handler(message, bot, AverageScoreHandler(self.ioc))
