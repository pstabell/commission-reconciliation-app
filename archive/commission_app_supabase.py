import streamlit as st
st.set_page_config(layout="wide")
import traceback
import string
import random
import pandas as pd
import datetime
import io
import streamlit_sortables
import os
import json
import pdfplumber
import shutil
import uuid
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from column_mapping_config import (
    column_mapper, get_mapped_column, get_ui_field_name, 
    is_calculated_field, safe_column_reference
)
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
@st.cache_resource
def get_supabase_client():
    """Get cached Supabase client."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        st.error("Missing Supabase credentials. Please check your .env file.")
        st.stop()
    return create_client(url, key)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_policies_data():
    """Load policies data from Supabase with caching."""
    try:
        supabase = get_supabase_client()
        response = supabase.table('policies').select("*").execute()
        if response.data:
            df = pd.DataFrame(response.data)
            # Ensure numeric columns are properly typed
            if 'Agent Estimated Comm $' in df.columns:
                df['Agent Estimated Comm $'] = pd.to_numeric(df['Agent Estimated Comm $'], errors='coerce')
            if 'BALANCE DUE' in df.columns:
                df['BALANCE DUE'] = pd.to_numeric(df['BALANCE DUE'], errors='coerce')
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data from Supabase: {e}")
        return pd.DataFrame()

def save_policy_to_supabase(policy_data):
    """Save a new policy to Supabase."""
    try:
        supabase = get_supabase_client()
        # Remove any _id field if it exists (Supabase will auto-generate)
        if '_id' in policy_data:
            del policy_data['_id']
        response = supabase.table('policies').insert(policy_data).execute()
        return True, response.data
    except Exception as e:
        return False, str(e)

def update_policy_in_supabase(policy_id, updates):
    """Update a policy in Supabase."""
    try:
        supabase = get_supabase_client()
        # Remove _id from updates if present
        if '_id' in updates:
            del updates['_id']
        response = supabase.table('policies').update(updates).eq('_id', policy_id).execute()
        return True, response.data
    except Exception as e:
        return False, str(e)

def delete_policy_from_supabase(policy_id):
    """Delete a policy from Supabase."""
    try:
        supabase = get_supabase_client()
        response = supabase.table('policies').delete().eq('_id', policy_id).execute()
        return True, response.data
    except Exception as e:
        return False, str(e)

def load_manual_entries():
    """Load manual commission entries from Supabase."""
    try:
        supabase = get_supabase_client()
        response = supabase.table('manual_commission_entries').select("*").execute()
        if response.data:
            return pd.DataFrame(response.data)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading manual entries: {e}")
        return pd.DataFrame()

def save_manual_entry(entry_data):
    """Save manual commission entry to Supabase."""
    try:
        supabase = get_supabase_client()
        if 'id' in entry_data:
            del entry_data['id']
        response = supabase.table('manual_commission_entries').insert(entry_data).execute()
        return True, response.data
    except Exception as e:
        return False, str(e)

def load_commission_payments():
    """Load commission payments from Supabase."""
    try:
        supabase = get_supabase_client()
        response = supabase.table('commission_payments').select("*").execute()
        if response.data:
            return pd.DataFrame(response.data)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading commission payments: {e}")
        return pd.DataFrame()

def save_commission_payment(payment_data):
    """Save commission payment to Supabase."""
    try:
        supabase = get_supabase_client()
        if 'id' in payment_data:
            del payment_data['id']
        response = supabase.table('commission_payments').insert(payment_data).execute()
        return True, response.data
    except Exception as e:
        return False, str(e)

def load_renewal_history():
    """Load renewal history from Supabase."""
    try:
        supabase = get_supabase_client()
        response = supabase.table('renewal_history').select("*").execute()
        if response.data:
            return pd.DataFrame(response.data)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading renewal history: {e}")
        return pd.DataFrame()

def save_renewal_history(renewal_data):
    """Save renewal history to Supabase."""
    try:
        supabase = get_supabase_client()
        if 'id' in renewal_data:
            del renewal_data['id']
        response = supabase.table('renewal_history').insert(renewal_data).execute()
        return True, response.data
    except Exception as e:
        return False, str(e)

# Clear cache functions
def clear_policies_cache():
    """Clear the policies data cache."""
    load_policies_data.clear()

def clear_all_caches():
    """Clear all data caches."""
    load_policies_data.clear()
    st.cache_data.clear()

@st.cache_data
def get_custom_css():
    """Get cached CSS for better performance."""
    return """<style>        /* Remove default padding and maximize main block width */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            margin-left: 240px !important;
            width: calc(100vw - 240px) !important;
            max-width: calc(100vw - 240px) !important;
        }
        
        /* Ensure main content area starts after sidebar */
        .main {
            margin-left: 240px !important;
            width: calc(100vw - 240px) !important;
            max-width: calc(100vw - 240px) !important;
        }
        
        /* Additional targeting for content wrapper */
        [data-testid="stAppViewContainer"] > .main {
            margin-left: 240px !important;
            width: calc(100vw - 240px) !important;
        }
          /* Force all main content to respect sidebar space */
        section.main {
            margin-left: 240px !important;
            width: calc(100vw - 240px) !important;
        }
        
        /* Target the root app container - this is critical! */
        [data-testid="stAppViewContainer"] {
            margin-left: 240px !important;
            width: calc(100vw - 240px) !important;
            max-width: calc(100vw - 240px) !important;
        }
        
        /* Also target the main header area */
        [data-testid="stHeader"] {
            margin-left: 240px !important;
            width: calc(100vw - 240px) !important;
        }
        
        /* Force sidebar to be permanently visible and disable all collapse functionality */
        section[data-testid="stSidebar"] {
            min-width: 240px !important;
            max-width: 240px !important;
            width: 240px !important;
            display: block !important;
            visibility: visible !important;
            position: fixed !important;
            left: 0 !important;
            top: 0 !important;
            height: 100vh !important;
            z-index: 999 !important;
            background-color: #f5f5f5 !important;
            overflow-y: auto !important;
            transform: translateX(0) !important;
            transition: none !important;
        }
        
        /* Override any transform or transition that might hide the sidebar */
        section[data-testid="stSidebar"][data-sidebar="collapsed"] {
            transform: translateX(0) !important;
            min-width: 240px !important;
            width: 240px !important;
            display: block !important;
            visibility: visible !important;
        }
        
        /* Hide the sidebar toggle button */
        button[data-testid="collapsedControl"],
        [data-testid="stSidebarCollapse"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarCollapseControl"],
        .css-1cypcdb,  /* Class for collapse button */
        .e1fqkh3o4 {    /* Another class for collapse button */
            display: none !important;
            visibility: hidden !important;
        }
        
        /* Remove any negative margins or positioning that might hide content */
        section[data-testid="stSidebar"] * {
            margin-left: 0 !important;
        }
        
        /* Ensure sidebar content is always visible */
        section[data-testid="stSidebar"] > div {
            width: 240px !important;
            min-width: 240px !important;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        
        /* Override any media queries that might affect sidebar */
        @media (max-width: 768px) {
            section[data-testid="stSidebar"] {
                transform: translateX(0) !important;
                display: block !important;
                visibility: visible !important;
            }
        }
        
        /* Additional safeguards against any transformation */
        .st-emotion-cache-1eo1v4u {  /* Sidebar container class */
            transform: none !important;
            min-width: 240px !important;
        }
        
        /* Ensure sidebar is never translated off-screen */
        [data-testid="stSidebar"]:not([data-sidebar="expanded"]) {
            transform: translateX(0) !important;
        }
        
        /* Remove padding and margins that might push main content */
        .css-1y4p8pa {
            max-width: none !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        /* Adjust text input widths to be more reasonable */
        input[type="text"], 
        input[type="number"], 
        .stTextInput input, 
        .stNumberInput input {
            max-width: 300px !important;
        }
        
        /* Style scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        
        /* Make dataframes scrollable */
        .stDataFrame {
            max-width: 100%;
            overflow-x: auto;
        }
        
        /* Style the radio buttons */
        .stRadio > div {
            background-color: white;
            padding: 0.5rem;
            border-radius: 0.5rem;
        }
        
        /* Additional override for stale element reference issues */
        iframe {
            pointer-events: auto !important;
        }
        
        /* Force main content to have proper width */
        .main .block-container {
            max-width: none !important;
        }
        
        /* Make sure the header also respects the sidebar */
        header[data-testid="stHeader"] {
            margin-left: 240px !important;
        }
        
        /* Style headers */
        h1, h2, h3 {
            color: #1f2937;
        }
        
        /* Style metrics */
        [data-testid="metric-container"] {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        /* Style upload section */
        .uploadedFile {
            background-color: #f8f9fa;
            padding: 0.5rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        /* Ensure data editor takes full width */
        [data-testid="stDataFrameResizable"] {
            width: 100% !important;
        }
        
        /* Style data editor cells */
        .stDataFrameGlideDataEditor {
            min-height: 400px !important;
        }
    </style>"""

def apply_css():
    """Apply custom CSS to the app."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

def format_currency(value):
    """Format a value as currency."""
    try:
        if pd.isna(value) or value is None:
            return "$0.00"
        return f"${float(value):,.2f}"
    except:
        return "$0.00"

def generate_client_id():
    """Generate a unique client ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_transaction_id():
    """Generate a unique transaction ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

# Copy all other functions from the original file (safe_float, calculate_commission, etc.)
# These functions don't interact with the database directly, so they remain the same

def safe_float(value):
    """Safely convert a value to float, handling various formats."""
    if pd.isna(value) or value is None or value == '':
        return 0.0
    
    if isinstance(value, (int, float)):
        return float(value)
    
    # If it's a string, clean it up
    if isinstance(value, str):
        # Remove currency symbols and commas
        cleaned = value.replace('$', '').replace(',', '').strip()
        # Remove percentage signs
        cleaned = cleaned.replace('%', '').strip()
        
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    
    return 0.0

def calculate_commission(row):
    """Calculate commission for a given row."""
    premium = safe_float(row.get('Premium Sold', 0))
    comm_rate = safe_float(row.get('Policy Gross Comm %', 0))
    agent_rate = safe_float(row.get('Agent Comm (NEW 50% RWL 25%)', 0))
    
    # If commission rate is greater than 1, assume it's a percentage (e.g., 10 instead of 0.10)
    if comm_rate > 1:
        comm_rate = comm_rate / 100
    
    # If agent rate is greater than 1, assume it's a percentage
    if agent_rate > 1:
        agent_rate = agent_rate / 100
    
    # Calculate agency commission
    agency_comm = premium * comm_rate
    
    # Calculate agent commission
    agent_comm = agency_comm * agent_rate
    
    return agency_comm, agent_comm

def renew_selected_policies(selected_policies_df):
    """Generate renewal records for selected policies."""
    renewed_df = selected_policies_df.copy()
    
    # Generate new IDs
    renewed_df[get_mapped_column("Client ID")] = renewed_df[get_mapped_column("Client ID")].apply(lambda x: generate_client_id())
    renewed_df[get_mapped_column("Transaction ID")] = renewed_df[get_mapped_column("Transaction ID")].apply(lambda x: generate_transaction_id())
    
    # Update dates - add one year
    date_columns = ["Effective Date", "X-DATE"]
    for col in date_columns:
        mapped_col = get_mapped_column(col)
        if mapped_col in renewed_df.columns:
            renewed_df[mapped_col] = pd.to_datetime(renewed_df[mapped_col], format='%m/%d/%Y', errors='coerce')
            renewed_df[mapped_col] = renewed_df[mapped_col] + pd.DateOffset(years=1)
    
    # Create new effective and expiration dates
    renewed_df['new_effective_date'] = renewed_df[get_mapped_column("X-DATE")]
    renewed_df['new_expiration_date'] = renewed_df['new_effective_date'] + pd.DateOffset(years=1)
    
    # Update the actual columns
    renewed_df[get_mapped_column("Effective Date")] = renewed_df['new_effective_date'].dt.strftime('%m/%d/%Y')
    renewed_df[get_mapped_column("X-DATE")] = renewed_df['new_expiration_date'].dt.strftime('%m/%d/%Y')
    renewed_df[get_mapped_column("Transaction Type")] = "RWL"
    
    return renewed_df