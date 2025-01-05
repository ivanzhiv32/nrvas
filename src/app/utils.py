import pandas as pd
from openpyxl import load_workbook
from telebot.types import Message

from app.constants import BASE_DIR


def check_is_admin(message: Message, id_admin: int) -> bool:
    return message.from_user.id == id_admin


def excel_to_2d_array(name: str) -> pd.DataFrame:
    wb = load_workbook(BASE_DIR / f'documents/{name}')
    sheet = wb.active
    return pd.DataFrame(sheet.values)
