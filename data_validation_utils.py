"""
Data Validation Utilities for Commission App
Handles empty data states and provides consistent validation across all pages
"""

import streamlit as st
import pandas as pd
from typing import Optional, List, Tuple

def check_data_availability(df: pd.DataFrame, 
                          required_columns: Optional[List[str]] = None,
                          page_name: str = "This page") -> Tuple[bool, str]:
    """
    Check if dataframe has data and required columns.
    
    Args:
        df: DataFrame to check
        required_columns: List of column names that must exist
        page_name: Name of the page for error messages
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if dataframe is empty
    if df is None or df.empty:
        return False, f"No data found. Please add some policies first to use {page_name}."
    
    # Check for required columns if specified
    if required_columns:
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return False, f"Missing required columns: {', '.join(missing_columns)}. Please check your data import."
    
    return True, ""

def show_empty_state(page_title: str, 
                    primary_action: str = "Add New Policy Transaction",
                    secondary_action: Optional[str] = "Import CSV Data",
                    custom_message: Optional[str] = None):
    """
    Display a consistent empty state UI when no data is available.
    
    Args:
        page_title: Title of the current page
        primary_action: Main action user should take
        secondary_action: Alternative action
        custom_message: Optional custom message to display
    """
    # Display empty state container
    st.markdown(f"""
    <div style='text-align: center; padding: 50px; background-color: #f8f9fa; border-radius: 10px; margin: 20px 0;'>
        <h2 style='color: #6c757d; margin-bottom: 20px;'>📊 No Data Available</h2>
        <p style='color: #6c757d; font-size: 18px; margin-bottom: 30px;'>
            {custom_message or f"Start tracking your commissions by adding your first policy."}
        </p>
        <div style='margin-top: 30px;'>
            <p style='color: #28a745; font-size: 16px; font-weight: bold;'>Getting Started:</p>
            <ol style='text-align: left; display: inline-block; color: #6c757d;'>
                <li>Click <strong>>></strong> to open the menu</li>
                <li>Navigate to <strong>{primary_action}</strong></li>
                <li>Enter your policy details</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if secondary_action:
        st.info(f"💡 **Tip**: You can also go to **{secondary_action}** to import existing data in bulk.")

def validate_required_fields(data: dict, required_fields: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate that all required fields are present and not empty.
    
    Args:
        data: Dictionary of field values
        required_fields: List of required field names
        
    Returns:
        Tuple of (is_valid, list_of_missing_fields)
    """
    missing_fields = []
    
    for field in required_fields:
        value = data.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing_fields.append(field)
    
    return len(missing_fields) == 0, missing_fields

def safe_column_access(df: pd.DataFrame, column: str, default_value=None):
    """
    Safely access a column in a dataframe, returning default if column doesn't exist.
    
    Args:
        df: DataFrame to access
        column: Column name
        default_value: Value to return if column doesn't exist
        
    Returns:
        Series or default value
    """
    if df is None or df.empty:
        return pd.Series(dtype=object)
    if column in df.columns:
        return df[column]
    else:
        return pd.Series([default_value] * len(df), index=df.index)

def safe_filter_contains(df: pd.DataFrame, column: str, search_term: str, case=False, na=False):
    """
    Safely filter dataframe rows containing search term in specified column.
    
    Args:
        df: DataFrame to filter
        column: Column name to search in
        search_term: String to search for
        case: Case sensitive search
        na: Include NA values
        
    Returns:
        Filtered DataFrame or empty DataFrame if error
    """
    if df is None or df.empty or column not in df.columns:
        return pd.DataFrame()
    
    try:
        return df[df[column].str.contains(search_term, case=case, na=na)]
    except Exception:
        return pd.DataFrame()

def safe_groupby(df: pd.DataFrame, by_columns: List[str], agg_func: str = 'sum'):
    """
    Safely perform groupby operation, returning empty result if columns missing.
    
    Args:
        df: DataFrame to group
        by_columns: Columns to group by
        agg_func: Aggregation function
        
    Returns:
        Grouped DataFrame or empty DataFrame
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    missing_cols = [col for col in by_columns if col not in df.columns]
    if missing_cols:
        return pd.DataFrame()
    
    try:
        return df.groupby(by_columns).agg(agg_func)
    except Exception:
        return pd.DataFrame()

def validate_commission_data(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate commission data has minimum required columns.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Define minimum required columns for commission tracking
    required_columns = [
        'Transaction ID',
        'Customer',
        'Policy Number',
        'Transaction Type',
        'Effective Date'
    ]
    
    return check_data_availability(df, required_columns, "commission tracking")

def handle_empty_data(page_name: str, 
                     show_alternate_content: bool = True,
                     custom_empty_message: Optional[str] = None):
    """
    Decorator to handle empty data states consistently across pages.
    
    Usage:
        @handle_empty_data("Reports")
        def show_reports_page(data):
            # Your page logic here
    """
    def decorator(func):
        def wrapper(data, *args, **kwargs):
            is_valid, error_msg = validate_commission_data(data)
            
            if not is_valid:
                if show_alternate_content:
                    show_empty_state(
                        page_name,
                        custom_message=custom_empty_message or error_msg
                    )
                else:
                    st.warning(error_msg)
                return None
            
            return func(data, *args, **kwargs)
        
        return wrapper
    
    return decorator