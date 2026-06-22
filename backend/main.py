import os
import shutil

from fastapi import FastAPI
from fastapi import UploadFile, File

from backend.ingest import ingest_csv_data
from backend.schemas import QueryRequest, ExecuteRequest
from backend.sql_generator import generate_sql
from backend.validator import validate_sql
from backend.explainer import explain_sql
from backend.query_executor import query_execution

app = FastAPI(title= "Explainable SQL Copilot")

@app.get("/")
def root():
    return {"message": "Explainable SQL Copilot API"}

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):

    if not file.filename.endswith(".csv"):
        return {
            "success": False,
            "error": "Only CSV files are allowed."
        }

    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = ingest_csv_data(
        csv_path=file_path,
        file_name=file.filename
    )

    return {
        "success": True,
        **result
    }

@app.post("/generate-query")
def generate_query(request: QueryRequest):
    try:
        raw_sql = generate_sql(request.question)
        sql_validation = validate_sql(raw_sql)
        explanation = explain_sql(sql_validation)

        return {
            "success": True,
            "sql": sql_validation,
            "explanation": explanation
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/execute-query")
def execute_query(request: ExecuteRequest):
    result = query_execution(request.sql)
    return result