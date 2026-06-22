from google import genai

from backend.config import API_KEY
from backend.schema_inspector import get_schema


client = genai.Client(api_key= API_KEY)


def generate_sql(question: str):

    schema = get_schema()

    prompt = f"""
                You are a PostgreSQL SQL expert.

                Database Schema:
                {schema}

                Rules:
                1. Generate only valid PostgreSQL SELECT queries.
                2. Use only tables and columns that exist in the schema.
                3. If the user asks for a table or column that does not exist, return exactly: COLUMN_NOT_FOUND
                4. Do not use NULL as a replacement for missing columns.
                5. Return only SQL. Do not include explanations or markdown.
                6. For aggregated columns, always use clear aliases.
                Examples:
                SUM(revenue) AS total_revenue
                AVG(revenue) AS average_revenue
                MAX(revenue) AS max_revenue
                MIN(revenue) AS min_revenue
                COUNT(*) AS total_count
                7. Never generate DELETE, UPDATE, DROP, ALTER, INSERT, CREATE, or TRUNCATE.

                User Question:
                {question}
            """

    response = client.models.generate_content(
        model= "gemini-2.5-flash",
        contents= prompt
    )
    
    return response.text.strip()