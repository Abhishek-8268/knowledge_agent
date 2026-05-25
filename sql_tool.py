import sqlite3
import re
import os
from dotenv import load_dotenv
from groq import Groq

# Ensure env variables are loaded
load_dotenv()
client = Groq()

DB_NAME = "ecommerce.db"

def get_schema() -> str:
    """Reads the schema definition from SCHEMA.md to feed to the LLM."""
    try:
        with open("SCHEMA.md", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "Schema file not found. Ensure SCHEMA.md exists."

def is_safe_sql(sql_query: str) -> bool:
    """
    Strict SQL safety validation.
    Only allow a single SELECT statement.
    """

    query_upper = sql_query.upper().strip()

    forbidden_keywords = [
        "INSERT", "UPDATE", "DELETE",
        "DROP", "ALTER", "CREATE",
        "TRUNCATE", "REPLACE",
        "GRANT", "REVOKE",
        "ATTACH", "DETACH", "PRAGMA"
    ]

    # Reject dangerous keywords
    for keyword in forbidden_keywords:
        if re.search(rf'\b{keyword}\b', query_upper):
            return False

    # Only allow SELECT
    if not query_upper.startswith("SELECT"):
        return False

    # Reject multiple statements
    if ";" in query_upper[:-1]:
        return False

    return True

def generate_sql(question: str) -> str:
    """Uses Groq to translate a natural language question into a SQL query."""
    schema = get_schema()
    
    system_prompt = f"""
    You are an expert SQLite developer. 
    Your job is to translate the user's question into a valid, read-only SQLite query.
    
    Here is the database schema:
    {schema}
    
    Rules:
    - Only return the raw SQL query.
    - Do NOT include markdown formatting like ```sql or ```.
    - Do NOT explain the query.
    - NEVER write queries that modify the database (no INSERT, UPDATE, DELETE).
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0, # Temperature 0 makes the model more deterministic and logical
        )
        
        raw_response = chat_completion.choices[0].message.content.strip()
        
        # Clean up any residual markdown if the model disobeys instructions
        clean_sql = raw_response.replace("```sql", "").replace("```", "").strip()
        return clean_sql
        
    except Exception as e:
        return f"Error generating SQL: {str(e)}"

def query_database(question: str) -> str:
    """
    The main tool function: Translates, validates, and executes the SQL.
    Returns the results as a string.
    """
    print(f"\n[Tool Execution] Translating to SQL...")
    sql_query = generate_sql(question)
    print(f"[Tool Execution] Generated SQL: {sql_query}")
    
    if not is_safe_sql(sql_query):
        return f"Security Error: The generated SQL was rejected by the guardrail. Query: {sql_query}"
        
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        # Get column names for better readability
        columns = [description[0] for description in cursor.description]
        conn.close()
        
        if not results:
            return "Query executed successfully, but returned no results."
            
        # Format the results into a readable string
        formatted_results = f"Columns: {', '.join(columns)}\nData:\n"
        for row in results:
            row_data = ", ".join(
                f"{col}: {val}"
                for col, val in zip(columns, row)
            )
            formatted_results += f"- {row_data}\n"
            
        return formatted_results

    except sqlite3.Error as e:
        return f"Database Execution Error: {str(e)}"

if __name__ == "__main__":
    # Let's test the pipeline
    test_question = "Which products were most ordered last month?"
    print(f"User Question: {test_question}")
    result = query_database(test_question)
    print("\n[Tool Output]")
    print(result)
    
    print("\n--- Testing Guardrail ---")
    malicious_query = "Drop the customers table."
    print(f"User Question: {malicious_query}")
    malicious_result = query_database(malicious_query)
    print("\n[Tool Output]")
    print(malicious_result)