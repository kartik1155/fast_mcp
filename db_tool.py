# db_tool.py

import os
import psycopg2
from fastmcp import FastMCP

# Environment variables (Render injects them automatically)
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

mcp = FastMCP("PostgreSQL Query Tool 🐘")


@mcp.tool()
def run_query(sql: str) -> list:
    """Run a SQL query on the PostgreSQL database. Use for read-only queries."""
    try:
        with psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                if cur.description:
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
                else:
                    return [{"message": "Query executed successfully, no results."}]
    except Exception as e:
        return [{"error": str(e)}]

# For Render or Uvicorn
app = mcp.app
