from backend.sql_generator import generate_sql
from backend.validator import validate_sql
from backend.query_executor import query_execution
from backend.explainer import explain_sql

question = "What is the highest revenue product?"

sql = generate_sql(question)
sql_validation = validate_sql(sql)
sql_explainer = explain_sql(sql_validation)
result = query_execution(sql_validation)


print("\nSQL Query:\n", sql_validation)
print("\nExplanation of the SQL Query:\n", sql_explainer)
print("\nResult:\n",result) 
