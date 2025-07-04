"""
Helper functions for Commission Management Application
Contains utility functions used across multiple pages.
"""

import pandas as pd
import string
import random
import datetime
from column_mapping_config import (
    get_mapped_column, get_ui_field_name, 
    is_calculated_field, safe_column_reference
)


def format_currency(val):
    """Format the value as currency for display."""
    if pd.isna(val) or val is None:
        return ""
    try:
        return f"${val:,.2f}"
    except Exception:
        return val


def format_dates_mmddyyyy(df):
    """Format date columns to MM/DD/YYYY format."""
    if df.empty:
        return df
    
    date_columns = ["Effective Date"]
    for col in date_columns:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%m/%d/%Y')
            except Exception:
                pass
    return df


def format_currency_columns(df):
    """Apply currency formatting to specified columns."""
    if df.empty:
        return df
    
    currency_columns = [
        "Commission Paid", "Agency Commission Received", "Premium",
        "Balance Due", "Commission_Paid", "Agency_Commission_Received"
    ]
    
    for col in currency_columns:
        if col in df.columns:
            try:
                df[col] = df[col].apply(format_currency)
            except Exception:
                pass
    return df


def generate_client_id(length=6):
    """Generate a random client ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_transaction_id(length=7):
    """Generate a random transaction ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def calculate_commission(row):
    """Calculate commission based on premium and rate."""
    try:
        premium = float(row.get('Premium', 0))
        rate = float(row.get('Commission_Rate', 0))
        return premium * (rate / 100)
    except (ValueError, TypeError):
        return 0.0


def get_pending_renewals(df):
    """Identify policies that need renewal based on effective dates."""
    if df.empty:
        return pd.DataFrame()
    
    try:
        # Convert effective date to datetime
        df_copy = df.copy()
        df_copy['Effective_Date'] = pd.to_datetime(df_copy['Effective_Date'], errors='coerce')
        
        # Calculate days until renewal (assuming 1 year policy term)
        today = pd.Timestamp.now()
        df_copy['Days_Until_Renewal'] = (df_copy['Effective_Date'] + pd.DateOffset(years=1) - today).dt.days
        
        # Return policies due for renewal in the next 30 days
        pending = df_copy[(df_copy['Days_Until_Renewal'] <= 30) & (df_copy['Days_Until_Renewal'] >= -30)]
        return pending.sort_values('Days_Until_Renewal')
        
    except Exception as e:
        print(f"Error in get_pending_renewals: {e}")
        return pd.DataFrame()


def duplicate_for_renewal(df):
    """Create renewal records from existing policies."""
    if df.empty:
        return pd.DataFrame()
    
    try:
        renewed_df = df.copy()
        
        # Update transaction IDs for renewals
        renewed_df['Transaction_ID'] = [generate_transaction_id() for _ in range(len(renewed_df))]
        
        # Update effective dates to next year
        renewed_df['Effective_Date'] = pd.to_datetime(renewed_df['Effective_Date'], errors='coerce')
        renewed_df['Effective_Date'] = (renewed_df['Effective_Date'] + pd.DateOffset(years=1)).dt.strftime('%m/%d/%Y')
        
        # Mark as renewal transaction
        renewed_df[get_mapped_column("Transaction Type")] = "RWL"
        
        return renewed_df
        
    except Exception as e:
        print(f"Error in duplicate_for_renewal: {e}")
        return pd.DataFrame()


def safe_page_execution(page_func, page_name="Unknown Page"):
    """Safely execute a page function with error handling."""
    try:
        return page_func()
    except Exception as e:
        import streamlit as st
        import traceback
        
        st.error(f"⚠️ Error loading {page_name}")
        st.error(f"Error details: {str(e)}")
        
        # Show detailed error in expander for debugging
        with st.expander("🔧 Technical Details (for developers)"):
            st.code(traceback.format_exc())
        
        # Suggest recovery actions
        st.info("💡 **Suggested actions:**")
        st.write("1. Try refreshing the page")
        st.write("2. Check if all required data is available")
        st.write("3. Contact your system administrator if the problem persists")
        
        return None