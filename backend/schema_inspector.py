import pandas as pd

from sqlalchemy import text
from backend.database import SessionLocal

def get_schema():
    query = """
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
            """

    with SessionLocal() as session:
        df = pd.read_sql(text(query), session.bind)

    schema = {}

    for table_name, group in df.groupby("table_name"):
        schema[table_name] = (
            group[["column_name", "data_type"]].rename(
                columns={
                    "column_name": "column",
                    "data_type": "type"
                }
            ).to_dict(orient= "records")
        )

    return schema
            
