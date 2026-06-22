from backend.config import API_KEY
from google import genai

client = genai.Client(api_key= API_KEY)

def explain_sql(output: str):
    prompt = f"""You are an analytics assistant.

            Explain this SQL query in plain English.

            SQL_QUERY_START
            {output}
            SQL_QUERY_END

            Rules:
            1. Explain what the query does.
            2. Use simple language.
            3. Keep it under 80 words.
            4. Do not say the SQL query was not provided.
        """
    
    response = client.models.generate_content(
        model= "gemini-2.5-flash",
        contents= prompt
    )

    return response.text.strip()
    
