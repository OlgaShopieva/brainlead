import pandas as pd
from sqlalchemy import text
from src.database import engine


def collect_tables():
    query = text("""
        SELECT
            TABLE_NAME,
            TABLE_TYPE,
            ENGINE,
            TABLE_ROWS,
            DATA_LENGTH,
            INDEX_LENGTH,
            CREATE_TIME,
            UPDATE_TIME,
            TABLE_COMMENT
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = DATABASE()
        ORDER BY TABLE_NAME
    """)

    with engine.connect() as conn:
        return pd.read_sql(query, conn)


def collect_columns():
    query = text("""
        SELECT
            TABLE_NAME,
            COLUMN_NAME,
            ORDINAL_POSITION,
            COLUMN_TYPE,
            IS_NULLABLE,
            COLUMN_DEFAULT,
            COLUMN_KEY,
            EXTRA,
            COLUMN_COMMENT
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        ORDER BY TABLE_NAME, ORDINAL_POSITION
    """)

    with engine.connect() as conn:
        return pd.read_sql(query, conn)