import pandas as pd
from pandas import ExcelWriter
import pyodbc as dbc

def read_sql(query: str, driver: str, server: str, database: str) -> pd.DataFrame:
    """Returns a dataframe from a sql query"""
    conn = dbc.connect(f"Driver={driver};Server={server};Database={database};Trusted_Connection=yes;")
    return pd.read_sql(query, conn)

def import_any(value: str, **kwargs) -> pd.DataFrame:
    """Creates a data frame from a csv file, excel file or sql query."""
    if value.endswith('.csv'):
        return pd.read_csv(value, **kwargs)
    elif value.endswith('.xls') or value.endswith('.xlsx'):
        return pd.read_excel(value, **kwargs)
    else:
        return read_sql(value, **kwargs)

def export_to_excel(data_frames: {pd.DataFrame}, path):
    """Exports multiple data frames into an excel workbook. The dict key is the sheet name."""
    with ExcelWriter(path) as writer:
        for key, data_frame in data_frames.items():
            data_frame.to_excel(writer, key, index=False)
        writer.save()