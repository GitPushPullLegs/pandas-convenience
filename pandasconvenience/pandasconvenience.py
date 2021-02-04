import pandas as pd
import pyodbc as dbc

def read_sql(query: str, driver: str, server: str, database: str) -> pd.DataFrame:
    """Returns a dataframe from a sql query"""
    conn = dbc.connect(f"Driver={driver};Server={server};Database={database};Trusted_Connection=yes;")
    return pd.read_sql(query, conn)

