from openpyxl.reader.excel import load_workbook
from telebot import TeleBot
from telebot.types import Message

from app.presentation.handlers.base import IHandler


class AddingQuestionHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        # TODO: добавить БД
        filename = 'documents/questions.xlsx'
        wb = load_workbook(self.ioc.path / filename)
        sheet = wb.active
        rows_count = sheet.max_row
        data = (rows_count, message.from_user.id, False, message.text)
        sheet.append(data)
        wb.save(self.ioc.path / filename)
