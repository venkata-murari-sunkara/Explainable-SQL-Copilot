
FORBIDDEN_WORDS = [
    "DROP",
    "DELETE",
    "TRUNCATE",
    "ALTER",
    "CREATE",
    "INSERT",
    "UPDATE",
    "GRANT",
    "REVOKE"   
]


def clean_sql_output(output: str) -> str :
    output = output.strip()
    output = output.replace("```sql", "")
    output = output.replace("```", "")
    return output.strip()

def validate_sql(output: str) -> str:
    if not output:
        raise ValueError("No SQL query was generated.")

    output = clean_sql_output(output)

    upper_sql = output.upper()
    
    
    if "COLUMN_NOT_FOUND" in upper_sql.upper():
        raise ValueError("The requested column does not exist in the uploaded dataset.")

    if not upper_sql.startswith("SELECT"):
        raise ValueError("Only SELECT statements are allowed.")
    
    
    for keyword in FORBIDDEN_WORDS:
        if keyword in upper_sql:
            raise ValueError(f"Forbidden SQL keyword detected: {keyword}")
        
    
    return output