import pandas as pd
from src.config.config import file1, file3


def load_ghg_totals_by_country():
    excel1 = pd.ExcelFile(file1)
    return pd.read_excel(excel1, sheet_name="GHG_totals_by_country")

def load_wb_income_data():
    excel3 = pd.ExcelFile(file3)
    return pd.read_excel(excel3, sheet_name="List of economies")