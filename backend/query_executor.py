import pandas as pd

from sqlalchemy import text
from backend.database import SessionLocal

def query_execution(output: str):
    try:
        with SessionLocal() as session:
            df = pd.read_sql(text(output), session.bind)

        return {
            "success": True,
            "rows": df.to_dict(orient="records")
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    