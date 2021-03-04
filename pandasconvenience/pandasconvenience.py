import pandas as pd
import pyodbc as dbc
from pandas import ExcelWriter
import keyring


def read_sql(query: str,
             driver: str = keyring.get_password('sql_server', 'driver'),
             server: str = keyring.get_password('sql_server', 'server'),
             database: str = keyring.get_password('sql_server', 'database')) -> pd.DataFrame:
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

_HEADER_FORMAT = dict(bold=True, text_wrap=True, fg_color='#365f92', font_color='#FFFFFF', border=1)

def export_to_excel(data_frames: {pd.DataFrame}, output_path: str,
                    header_formatting: bool = True, auto_column_width: bool = True,
                    datetime_format: str = 'mm/dd/yyyy', date_format: str = 'mm/dd/yyyy'):
    """
    Combines multiple data frames into multiple tabs in one excel document.
    Args:
        data_frames: The data frames to be output. The key will be used as the tab name.
        output_path: Where the excel file should be created.
        header_formatting: Default true. Whether the headers should be formatted with a blue theme.
        auto_column_width: Default true. Sets the width to that of the longest value in each column.
        datetime_format: Default mm/dd/yyyy. Sets the format for the datetime cells.
        date_format:  Default mm/dd/yyy. Sets the format for the date cells.
    """
    with ExcelWriter(output_path,
                     engine='xlsxwriter',
                     datetime_format=datetime_format,
                     date_format=date_format) as writer:
        for key, data_frame in data_frames.items():
            data_frame.to_excel(writer, sheet_name=key, startrow=1, header=False, index=False)
            workbook = writer.book
            worksheet = writer.sheets[key]
            if header_formatting:
                header_format = workbook.add_format(_HEADER_FORMAT)
                for col_num, value in enumerate(data_frame.columns.values):
                    worksheet.write(0, col_num, value, header_format)

            if auto_column_width:
                for idx, col in enumerate(data_frame):
                    series = data_frame[col]
                    max_len = max((
                        series.astype(str).map(len).max(),
                        len(str(series.name))
                    )) + 1
                    worksheet.set_column(idx, idx, max_len)
        writer.save()


def split(data_frame: pd.DataFrame, columns: [str]) -> {pd.DataFrame}:
    """Splits a data frame into multiple by the columns."""
    return dict(tuple(data_frame.groupby(columns)))
