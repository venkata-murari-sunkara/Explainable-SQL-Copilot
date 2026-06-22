import re
import pandas as pd

from backend.database import engine

def clean_column_name(column_name: str) -> str :
    column_name = column_name.strip().lower()
    column_name = re.sub(r"[^a-zA-Z0-9_]+", "_", column_name)
    column_name = re.sub(r"_+", "_", column_name)
    return column_name.strip("_")

def clean_table_name(table_name: str) -> str :
    table_name = table_name.strip().lower()
    table_name = re.sub(r"[^a-zA-Z0-9_]+", "_", table_name)
    table_name = re.sub(r"_+", "_", table_name)
    return table_name.strip("_")


def ingest_csv_data(csv_path: str, file_name: str):
    df = pd.read_csv(csv_path)

    df.columns = [clean_column_name(col) for col in df.columns]

    table_name = clean_table_name(file_name)

    df.to_sql(
        name= table_name,
        con= engine,
        if_exists= "replace",
        index= False
    )

    return {
        "message": "CSV ingested successfully",
        "table_name": table_name,
        "rows": len(df),
        "columns": list(df.columns)
    }