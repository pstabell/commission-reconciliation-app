"""
Database utilities for Commission Management Application
Handles database connections, caching, and common operations.
"""

import streamlit as st
import sqlalchemy
import pandas as pd
import traceback


@st.cache_resource
def get_database_engine():
    """Get cached database engine for better performance."""
    return sqlalchemy.create_engine(
        'sqlite:///commissions.db',
        pool_pre_ping=True,
        pool_recycle=3600
    )


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_policies_data():
    """Load policies data with caching for better performance."""
    try:
        engine = get_database_engine()
        return pd.read_sql('SELECT * FROM policies', engine)
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return pd.DataFrame()


def execute_query(query, params=None, fetch=False):
    """Execute a database query with error handling."""
    try:
        engine = get_database_engine()
        with engine.begin() as conn:
            if fetch:
                if params:
                    result = conn.execute(sqlalchemy.text(query), params)
                else:
                    result = conn.execute(sqlalchemy.text(query))
                return result.fetchall()
            else:
                if params:
                    conn.execute(sqlalchemy.text(query), params)
                else:
                    conn.execute(sqlalchemy.text(query))
                return True
    except Exception as e:
        st.error(f"Database error: {e}")
        return False


def ensure_table_exists(table_name, create_sql):
    """Ensure a table exists, create if it doesn't."""
    try:
        engine = get_database_engine()
        with engine.begin() as conn:
            conn.execute(sqlalchemy.text(create_sql))
        return True
    except Exception as e:
        st.error(f"Error creating table {table_name}: {e}")
        return False


def safe_database_operation(operation_func, error_message="Database operation failed"):
    """Safely execute database operations with error handling."""
    try:
        return operation_func()
    except Exception as e:
        st.error(f"{error_message}: {str(e)}")
        # Log the full traceback for debugging
        if st.session_state.get('debug_mode', False):
            st.text(traceback.format_exc())
        return None