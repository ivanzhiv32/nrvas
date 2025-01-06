import pandas as pd
from openpyxl import load_workbook

from app.constants import BASE_DIR


def excel_to_2d_array(name: str) -> pd.DataFrame:
    wb = load_workbook(BASE_DIR / f'documents/{name}')
    sheet = wb.active
    return pd.DataFrame(sheet.values)
