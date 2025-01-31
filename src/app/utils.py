from pathlib import Path

import pandas as pd
from openpyxl import load_workbook


def excel_to_2d_array(path: Path) -> pd.DataFrame:
    wb = load_workbook(path)
    sheet = wb.active
    wb.close()
    return pd.DataFrame(sheet.values)
