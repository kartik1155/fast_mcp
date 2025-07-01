
from fastmcp import FastMCP
import psycopg2
from psycopg2.extras import RealDictCursor
import os

mcp = FastMCP("Database MCP 🎯")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", "5432")
}

@mcp.tool()
def run_query(query: str) -> list:
    """Execute a SELECT query from the database"""
    if not query.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries allowed.")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

# ✅ Correct way to expose FastAPI app for Render
app = mcp.build()
