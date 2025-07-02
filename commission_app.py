import streamlit as st
st.set_page_config(layout="wide")
import traceback
import string
import random
import pandas as pd
import sqlalchemy
import datetime
import io
import streamlit_sortables as sortables
import os
import json
import pdfplumber
import logging
import hashlib
import shutil
import uuid
import re
from pathlib import Path
from column_mapping_config import (
    column_mapper, get_mapped_column, get_ui_field_name, 
    is_calculated_field, safe_column_reference
)

def load_help_content(file_name):
    """Load markdown content from the help_content directory."""
    try:
        with open(os.path.join("help_content", file_name), "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: {file_name} not found."

# Configure logging for database protection system
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('commission_app.log'),
        logging.StreamHandler()
    ]
)

st.write(':green[App started - debug message]')

def apply_css():
    """Apply custom CSS styling to the Streamlit app."""
    with st.container():
        st.markdown(
            """
            <style>        /* Remove default padding and maximize main block width */
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
        
        /* Make tables and editors use reasonable width */
        .stDataFrame, .stDataEditor {
        }/* Force sidebar to be permanently visible and disable all collapse functionality */
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
            z-index: 999999 !important;
            background-color: #f0f2f6 !important;
        }
        
        /* Override any attempts to hide the sidebar */
        [data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(0px) !important;
            visibility: visible !important;
        }
        
        /* Remove collapse button completely */
        button[kind="header"][aria-label="Show navigation"] {
            display: none !important;
        }
        
        /* Make tables and editors use reasonable width */
        .stDataFrame, .stDataEditor {
        }/* Highlight all interactive input fields in Add New Policy Transaction form and Admin Panel rename headers */
        .stForm input:not([disabled]), .stForm select:not([disabled]), .stForm textarea:not([disabled]),
        .stTextInput > div > input:not([disabled]), .stNumberInput > div > input:not([disabled]), .stDateInput > div > input:not([disabled]) {
            background-color: #fff3b0 !important; /* Darker yellow */
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Make selectboxes match other fields and remove focus ring */
        .stSelectbox > div[data-baseweb="select"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        .stSelectbox > div[data-baseweb="select"]:focus,
        .stSelectbox > div[data-baseweb="select"]:active,
        .stSelectbox > div[data-baseweb="select"]:focus-visible {
            border: 2px solid #e6a800 !important;
            box-shadow: none !important;
            outline: none !important;
        }
        /* Add yellow border to the client name search input at the top of Add New Policy Transaction */
        input[type="text"][aria-label="Type client name to search:"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Add yellow border to Premium Sold Calculator inputs */
        input[type="number"][aria-label="Existing Premium"],
        input[type="number"][aria-label="New/Revised Premium"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Add yellow border to Enter Premium Sold and see Agency Revenue input */
        input[type="number"][aria-label="Premium Sold"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Custom fatter scrollbars for all tables and editors */
        .stDataFrame ::-webkit-scrollbar, .stDataEditor ::-webkit-scrollbar {
            height: 18px;
            width: 18px;
        }
        .stDataFrame ::-webkit-scrollbar-track, .stDataEditor ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 8px;
        }
        .stDataFrame ::-webkit-scrollbar-thumb, .stDataEditor ::-webkit-scrollbar-thumb {
            background: #888888;
            border-radius: 8px;
        }
        .stDataFrame ::-webkit-scrollbar-thumb:hover, .stDataEditor ::-webkit-scrollbar-thumb:hover {
            background: #b0b0b0;
            border-radius: 8px;
        }
        /* For Firefox */
        .stDataFrame, .stDataEditor {
            scrollbar-width: thick;
            scrollbar-color: #888888 #b0b0b0;
        }
            </style>
            """,
            unsafe_allow_html=True
        )

def format_currency(val):
    try:
        val = float(val)
        return f"${val:,.2f}"
    except (ValueError, TypeError):
        return val

def format_dates_mmddyyyy(df):
    """Format all date columns as MM/DD/YYYY for display."""
    date_cols = [col for col in df.columns if "date" in col.lower() or col.lower() in ["x-date", "xdate"]]
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%m/%d/%Y")
        except Exception:
            pass
    return df

CURRENCY_COLUMNS = [
    "Premium Sold",
    "Agency Commission Received $",
    "Gross Premium Paid",
    "Agency Gross Comm",
    "Paid Amount",
    "Estimated Agent Comm",
    "Estimated Agent Comm (New 50% Renewal 25%)",
    "BALANCE DUE",
    "Balance Due"
]

def format_currency_columns(df):
    for col in CURRENCY_COLUMNS:
        if col in df.columns:
            df[col] = df[col].apply(format_currency)
    return df

def generate_client_id(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def generate_transaction_id(length=7):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def calculate_commission(row):
    try:
        revenue = float(row["Agency Revenue"])
    except (ValueError, TypeError):
        revenue = 0.0
    if row["NEW/RWL"] in ["NEW", "NBS", "STL", "BoR"]:
        return revenue * 0.50
    elif row["NEW/RWL"] in ["END", "PCH"]:
        return revenue * 0.50 if row["Policy Origination Date"] == row["Effective Date"] else revenue * 0.25
    elif row["NEW/RWL"] in ["RWL", "REWRITE"]:
        return revenue * 0.25
    elif row["NEW/RWL"] in ["CAN", "XCL"]:
        return 0
    else:
        return revenue * 0.25

def main():
    # --- DEBUG: Surface any top-level exceptions ---
    
    # Apply CSS styling
    apply_css()
    
    # --- Page Selection ---
    page = st.sidebar.radio(
        "Navigation", [
            "Dashboard",
            "Reports",
            "All Policies in Database",
            "Edit Policies in Database",
            "Add New Policy Transaction",
            "Search & Filter",
            "Admin Panel",
            "Accounting",
            "Help",
            "Policy Revenue Ledger",
            "Policy Revenue Ledger Reports",
            "Pending Policy Renewals"
        ]
    )
    
    # --- Database connection ---
    engine = sqlalchemy.create_engine('sqlite:///commissions.db')

    # --- Ensure 'policies' table exists ---
    with engine.begin() as conn:
        conn.execute(sqlalchemy.text("""
            CREATE TABLE IF NOT EXISTS policies (
                "Customer" TEXT,
                "Policy Type" TEXT,
                "Carrier Name" TEXT,
                "Policy Number" TEXT,
                "NEW/RWL" TEXT,
                "Agency Revenue" REAL,
                "Policy Origination Date" TEXT,
                "Effective Date" TEXT,
                "Paid" TEXT,
                "Calculated Commission" REAL,
                "Client ID" TEXT,
                "Transaction ID" TEXT
            )
        """))

    all_data = pd.read_sql('SELECT * FROM policies', engine)

    # --- Robust column renaming to match app expectations ---
    rename_dict = {
        "Policy type": "Policy Type",
        "Carrier": "Carrier Name",
        "Policy #": "Policy Number",
        "Estimated Agent Comm - New 50% Renewal 25%": "Estimated Agent Comm (New 50% Renewal 25%)",
        "Customer Name": "Customer",
        "Producer Name": "Producer",
        "Lead source": "Lead Source",
        "Premium Sold": "Premium Sold",
        "Agency Gross Paid": "Agency Gross Paid",
        "Gross Agency Comm %": "Gross Agency Comm %",
        "NEW BIZ CHECKLIST COMPLETE": "NEW BIZ CHECKLIST COMPLETE",
        "X-DATE": "X-DATE",
        "STMT DATE": "STMT DATE",
        "Agency Gross Comm": "Agency Gross Comm",
        "Paid Amount": "Paid Amount",
        "PAST DUE": "PAST DUE",
        "FULL OR MONTHLY PMTS": "FULL OR MONTHLY PMTS",
        "NOTES": "NOTES"
    }
    all_data.rename(columns=rename_dict, inplace=True)

    st.title("Sales Commission Tracker")
    
    # Initialize session state variables
    if "assigned_client_id" not in st.session_state:
        st.session_state["assigned_client_id"] = None
    if "assigned_client_name" not in st.session_state:
        st.session_state["assigned_client_name"] = None
    if "premium_sold_input_live" not in st.session_state:
        st.session_state["premium_sold_input_live"] = 0.0
    if "premium_sold_input" not in st.session_state:
        st.session_state["premium_sold_input"] = 0.0
    if "pending_add_col" not in st.session_state:
        st.session_state["pending_add_col"] = ""
    if "delete_confirmed" not in st.session_state:
        st.session_state["delete_confirmed"] = False
    if "pending_delete_col" not in st.session_state:
        st.session_state["pending_delete_col"] = ""

    # --- Sidebar Navigation ---
    show_debug = st.sidebar.checkbox("Show Debug Info", value=False)
    
    if show_debug:
        st.write("DEBUG: all_data shape:", all_data.shape)
        st.write("DEBUG: all_data columns:", all_data.columns.tolist())
        st.write("DEBUG: page selected:", page)
        st.dataframe(format_currency_columns(all_data))

    # Navigation Logic: Top Level ---
    
    # --- Dashboard (Home Page) ---
    if page == "Dashboard":
        st.markdown("""
        <style>
        /* Remove extra margin from header/title */
        .main .block-container h1 {
            margin-bottom: 0.5rem;
        }
        /* Highlight all interactive input fields in Add New Policy Transaction form and Admin Panel rename headers */
        .stForm input:not([disabled]), .stForm select:not([disabled]), .stForm textarea:not([disabled]),
        .stTextInput > div > input:not([disabled]), .stNumberInput > div > input:not([disabled]), .stDateInput > div > input:not([disabled]) {
            background-color: #fff3b0 !important; /* Darker yellow */
            border: 2px solid #e6a800 !important; /* Darker yellow border */
            border-radius: 6px !important;
        }
        /* Make selectboxes match other fields and remove focus ring */
        .stSelectbox > div[data-baseweb="select"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        .stSelectbox > div[data-baseweb="select"]:focus,
        .stSelectbox > div[data-baseweb="select"]:active,
        .stSelectbox > div[data-baseweb="select"]:focus-visible {
            border: 2px solid #e6a800 !important;
            box-shadow: none !important;
            outline: none !important;
        }
        /* Add yellow border to the client name search input at the top of Add New Policy Transaction */
        input[type="text"][aria-label="Type client name to search:"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Add yellow border to Premium Sold Calculator inputs */
        input[type="number"][aria-label="Existing Premium"],
        input[type="number"][aria-label="New/Revised Premium"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Add yellow border to Enter Premium Sold and see Agency Revenue input */
        input[type="number"][aria-label="Premium Sold"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Custom fatter scrollbars for all tables and editors */
        .stDataFrame ::-webkit-scrollbar, .stDataEditor ::-webkit-scrollbar {
            height: 18px;
            width: 18px;
        }
        .stDataFrame ::-webkit-scrollbar-thumb, .stDataEditor ::-webkit-scrollbar-thumb {
            background: #888888;
            border-radius: 8px;
            border: 3px solid #b0b0b0;
        }
        .stDataFrame ::-webkit-scrollbar-track, .stDataEditor ::-webkit-scrollbar-track {
            background: #b0b0b0;
            border-radius: 8px;
        }
        /* For Firefox */
        .stDataFrame, .stDataEditor {
            scrollbar-width: thick;
            scrollbar-color: #888888 #b0b0b0;
        }
        /* Highlight all interactive input fields in Add New Policy Transaction form and Admin Panel rename headers */
        .stForm input:not([disabled]), .stForm select:not([disabled]), .stForm textarea:not([disabled]),
        .stTextInput > div > input:not([disabled]), .stNumberInput > div > input:not([disabled]), .stDateInput > div > input:not([disabled]) {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Make selectboxes match other fields and remove focus ring */
        .stSelectbox > div[data-baseweb="select"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        .stSelectbox > div[data-baseweb="select"]:focus,
        .stSelectbox > div[data-baseweb="select"]:active,
        .stSelectbox > div[data-baseweb="select"]:focus-visible {
            border: 2px solid #e6a800 !important;
            box-shadow: none !important;
            outline: none !important;
        }
        /* Add yellow border to the client name search input at the top of Add New Policy Transaction */
        input[type="text"][aria-label="Type client name to search:"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Add yellow border to Premium Sold Calculator inputs */
        input[type="number"][aria-label="Existing Premium"],
        input[type="number"][aria-label="New/Revised Premium"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Add yellow border to Enter Premium Sold and see Agency Revenue input */
        input[type="number"][aria-label="Premium Sold"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Highlight selectboxes in Admin Panel reorder columns section */
        [id^="reorder_col_"] > div[data-baseweb="select"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        [id^="reorder_col_"] > div[data-baseweb="select"]:focus,
        [id^="reorder_col_"] > div[data-baseweb="select"]:active,
        [id^="reorder_col_"] > div[data-baseweb="select"]:focus-visible {
            border: 2px solid #e6a800 !important;
            box-shadow: none !important;
            outline: none !important;
        }
        /* Highlight selectboxes in Admin Panel reorder columns section (force all backgrounds) */
        [data-testid^="stSelectbox"][id^="reorder_col_"] > div[data-baseweb="select"],
        [id^="reorder_col_"] [data-baseweb="select"],
        [id^="reorder_col_"] [class*="css-1wa3eu0-placeholder"],
        [id^="reorder_col_"] [class*="css-1uccc91-singleValue"],
        [id^="reorder_col_"] [class*="css-1okebmr-indicatorSeparator"],
        [id^="reorder_col_"] [class*="css-1pahdxg-control"],
        [id^="reorder_col_"] [class*="css-1s2u09g-control"],
        [id^="reorder_col_"] [class*="css-1n7v3ny-option"],
        [id^="reorder_col_"] [class*="css-9gakcf-option"],
        [id^="reorder_col_"] [class*="css-1n6sfyn-MenuList"],
        [id^="reorder_col_"] [class*="css-1n6sfyn-MenuList"] * {
            background-color: #fff3b0 !important;
            border-color: #e6a800 !important;
            color: #222 !important;
        }
        [id^="reorder_col_"] > div[data-baseweb="select"] {
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        [id^="reorder_col_"] > div[data-baseweb="select"]:focus,
        [id^="reorder_col_"] > div[data-baseweb="select"]:active,
        [id^="reorder_col_"] > div[data-baseweb="select"]:focus-visible {
            border: 2px solid #e6a800 !important;
            box-shadow: none !important;
            outline: none !important;
        }
        /* Add yellow border to the client name search input at the top of Add New Policy Transaction */
        input[type="text"][aria-label="Type client name to search:"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Add yellow border to Premium Sold Calculator inputs */
        input[type="number"][aria-label="Existing Premium"],
        input[type="number"][aria-label="New/Revised Premium"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Add yellow border to Enter Premium Sold and see Agency Revenue input */
        input[type="number"][aria-label="Premium Sold"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Force highlight for all selectboxes labeled 'NEW/RWL' everywhere */
        label:has(> div[data-baseweb="select"]) {
            background-color: #fff3b0 !important;
            border-radius: 6px !important;
            padding: 2px 4px !important;
        }
        /* Also target selectbox input and dropdown for 'NEW/RWL' */
        [aria-label="NEW/RWL"] > div[data-baseweb="select"],
        [aria-label="NEW/RWL"] [data-baseweb="select"],
        [aria-label="NEW/RWL"] [class*="css-1wa3eu0-placeholder"],
        [aria-label="NEW/RWL"] [class*="css-1uccc91-singleValue"],
        [aria-label="NEW/RWL"] [class*="css-1okebmr-indicatorSeparator"],
        [aria-label="NEW/RWL"] [class*="css-1pahdxg-control"],
        [aria-label="NEW/RWL"] [class*="css-1s2u09g-control"],
        [aria-label="NEW/RWL"] [class*="css-1n7v3ny-option"],
        [aria-label="NEW/RWL"] [class*="css-9gakcf-option"],
        [aria-label="NEW/RWL"] [class*="css-1n6sfyn-MenuList"],
        [aria-label="NEW/RWL"] [class*="css-1n6sfyn-MenuList"] * {
            background-color: #fff3b0 !important;
            border-color: #e6a800 !important;
            color: #222 !important;
        }
        [aria-label="NEW/RWL"] > div[data-baseweb="select"] {
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        [aria-label="NEW/RWL"] > div[data-baseweb="select"]:focus,
        [aria-label="NEW/RWL"] > div[data-baseweb="select"]:active,
        [aria-label="NEW/RWL"] > div[data-baseweb="select"]:focus-visible {
            border: 2px solid #e6a800 !important;
            box-shadow: none !important;
            outline: none !important;
        }
        /* Add yellow border to the client name search input at the top of Add New Policy Transaction */
        input[type="text"][aria-label="Type client name to search:"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Add yellow border to Premium Sold Calculator inputs */
        input[type="number"][aria-label="Existing Premium"],
        input[type="number"][aria-label="New/Revised Premium"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Add yellow border to Enter Premium Sold and see Agency Revenue input */
        input[type="number"][aria-label="Premium Sold"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Highlight selectboxes in Admin Panel reorder columns section */
        [id^="reorder_col_"] > div[data-baseweb="select"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        [id^="reorder_col_"] > div[data-baseweb="select"]:focus,
        [id^="reorder_col_"] > div[data-baseweb="select"]:active,
        [id^="reorder_col_"] > div[data-baseweb="select"]:focus-visible {
            border: 2px solid #e6a800 !important;
            box-shadow: none !important;
            outline: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # --- Dashboard (Home Page) ---
    st.subheader("Dashboard")
    st.metric("Total Transactions", len(all_data))
    if "Calculated Commission" in all_data.columns:
        st.metric("Total Commissions", f"${all_data['Calculated Commission'].sum():,.2f}")
    st.write("Welcome! Use the sidebar to navigate.")
    
    # --- Client Search & Edit (clean selectbox style) ---
    st.markdown("### Search and Edit a Client")
    customer_col = get_mapped_column("Customer")
    if customer_col and customer_col in all_data.columns:
        customers = ["Select a client..."] + sorted(all_data[customer_col].dropna().unique().tolist())
        selected_client = st.selectbox("Filter by Customer:", customers)
    else:
        selected_client = None
    
    if selected_client and selected_client != "Select a client...":
        client_df = all_data[all_data[customer_col].str.strip().str.lower() == selected_client.strip().lower()].reset_index(drop=True)
        st.write(f"Showing policies for **{selected_client}**:")
        
        # --- Show metrics side by side, spaced in 6 columns, shifted left ---
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        # Move metrics to col2 and col3, leaving col6 open for future data
        with col2:
            agent_paid_col = get_mapped_column("Agent Paid Amount (STMT)")
            if agent_paid_col and agent_paid_col in client_df.columns:
                paid_amounts = pd.to_numeric(client_df[agent_paid_col], errors="coerce")
                total_paid = paid_amounts.sum()
                st.metric(label="Total Paid Amount", value=f"${total_paid:,.2f}")
            else:
                st.warning(f"No '{get_ui_field_name('Agent Paid Amount (STMT)')}' column found for this client.")
        
        with col3:
            # Calculate total estimated commissions for this client
            agent_comm_col = get_mapped_column("Agent Estimated Comm $")
            if agent_comm_col and agent_comm_col in client_df.columns:
                total_estimated_comm = pd.to_numeric(client_df[agent_comm_col], errors="coerce").fillna(0).sum()
                st.metric(label="Total Est. Commission", value=f"${total_estimated_comm:,.2f}")
            else:
                st.metric(label="Total Est. Commission", value="$0.00")

        # --- Pagination controls ---
        page_size = 10
        total_policies = len(client_df)
        total_pages = (total_policies - 1) // page_size + 1 if total_policies > 0 else 1
        page_num = st.number_input(
            f"Page (showing {page_size} at a time):",
            min_value=1, max_value=total_pages, value=1, step=1
        )

        start_idx = (page_num - 1) * page_size
        end_idx = start_idx + page_size
        page_df = client_df.iloc[start_idx:end_idx]

        # --- Add a blank row for new entry ---
        blank_row = {col: "" for col in client_df.columns}
        page_df_with_blank = pd.concat([page_df, pd.DataFrame([blank_row])], ignore_index=True)

        # --- Editable table for current page (with blank row) ---
        edited_page_df = st.data_editor(
            page_df_with_blank,
            use_container_width=True,
            height=200,
            key=f"edit_client_{page_num}"
        )

        # --- Save edits for all pages ---
        if st.button("Update This Client's Data", key="update_client_dashboard"):
            # Remove any completely blank rows except the new one (in case user didn't fill it)
            edited_page_df = edited_page_df.dropna(how="all").reset_index(drop=True)
            # Update the edited rows in the full client_df
            client_df.update(edited_page_df.iloc[:-1])  # update existing rows
            # If the last row (the blank) was filled, append it
            new_row = edited_page_df.iloc[-1]
            if new_row.notna().any() and any(str(val).strip() for val in new_row):
                client_df = pd.concat([client_df, pd.DataFrame([new_row])], ignore_index=True)
            # Replace all records for this client in the database
            remaining_df = all_data[all_data[customer_col].str.strip().str.lower() != selected_client.strip().lower()]
            updated_df = pd.concat([remaining_df, client_df], ignore_index=True)
            updated_df.to_sql('policies', engine, if_exists='replace', index=False)
            st.success("Client data updated!")
    else:
        # Show overall summary when no client is selected
        st.info("👆 Select a client above to view and edit their policies.")
        
        # --- Overall Database Summary ---
        st.markdown("### 📊 Database Overview")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if customer_col and customer_col in all_data.columns:
                unique_clients = all_data[customer_col].nunique()
                st.metric("Total Clients", unique_clients)
            else:
                st.metric("Total Clients", "N/A")
        
        with col2:
            total_policies = len(all_data)
            st.metric("Total Policies", f"{total_policies:,}")
        
        with col3:
            if "Calculated Commission" in all_data.columns:
                total_commissions = all_data["Calculated Commission"].sum()
                st.metric("Total Commissions", f"${total_commissions:,.2f}")
            else:
                st.metric("Total Commissions", "N/A")
        
        # --- Quick Actions ---
        st.markdown("### 🚀 Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📝 Add New Policy", use_container_width=True):
                st.session_state.page = "Add New Policy Transaction"
                st.rerun()
        
        with col2:
            if st.button("📊 View Reports", use_container_width=True):
                st.session_state.page = "Reports"
                st.rerun()
        
        with col3:
            if st.button("⚙️ Admin Panel", use_container_width=True):
                st.session_state.page = "Admin Panel"
                st.rerun()

# --- Navigation Logic: Top Level ---
# --- Reports ---
    if page == "Reports":
        st.subheader("Customizable Report")
    
        # --- Column selection ---
        st.markdown("**Select columns to include in your report:**")
        columns = all_data.columns.tolist()
        selected_columns = st.multiselect("Columns", columns, default=columns)
    
        # --- Date range filter (user can pick which date column) ---
        date_columns = [col for col in ["Effective Date", "Policy Origination Date", "Due Date", "X-Date", "X-DATE"] if col in all_data.columns]
        date_col = None
        if date_columns:
            date_col = st.selectbox("Select date column to filter by:", date_columns)
        if date_col:
            min_date = pd.to_datetime(all_data[date_col], errors="coerce").min()
            max_date = pd.to_datetime(all_data[date_col], errors="coerce").max()
            start_date, end_date = st.date_input(
                "Date range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                format="MM/DD/YYYY"
            )
            mask = (pd.to_datetime(all_data[date_col], errors="coerce") >= pd.to_datetime(start_date)) & \
                    (pd.to_datetime(all_data[date_col], errors="coerce") <= pd.to_datetime(end_date))
            report_df = all_data.loc[mask, selected_columns]
        else:
            report_df = all_data[selected_columns]
    
        # --- Optional: Filter by Customer ---
        if "Customer" in all_data.columns:
            st.markdown("**Filter by Customer:**")
            customers = ["All"] + sorted(all_data["Customer"].dropna().unique().tolist())
            selected_customer = st.selectbox("Customer", customers)
            if selected_customer != "All":
                report_df = report_df[report_df["Customer"] == selected_customer]
    
        # --- Balance Due dropdown filter ---
        balance_due_options = ["All", "YES", "NO"]
        selected_balance_due = st.selectbox("Balance Due", balance_due_options)
        # Calculate BALANCE DUE if not present
        if "BALANCE DUE" not in report_df.columns and "Paid Amount" in report_df.columns and "Estimated Agent Comm (New 50% Renewal 25%)" in report_df.columns:
            paid_amounts = pd.to_numeric(report_df["Paid Amount"], errors="coerce").fillna(0)
            # Try both possible commission columns, fallback to zeros if neither exists
            if "Estimated Agent Comm" in report_df.columns:
                commission_amounts = pd.to_numeric(report_df["Estimated Agent Comm"], errors="coerce").fillna(0)
            else:
                commission_amounts = pd.to_numeric(report_df["Estimated Agent Comm (New 50% Renewal 25%)"], errors="coerce").fillna(0)
            report_df["BALANCE DUE"] = commission_amounts - paid_amounts
        # Ensure BALANCE DUE is numeric for filtering
        report_df["BALANCE DUE"] = pd.to_numeric(report_df["BALANCE DUE"], errors="coerce").fillna(0)
        # Apply Balance Due filter
        if selected_balance_due != "All" and "BALANCE DUE" in report_df.columns:
            if selected_balance_due == "YES":
                report_df = report_df[report_df["BALANCE DUE"] > 0]
            elif selected_balance_due == "NO":
                report_df = report_df[report_df["BALANCE DUE"] <= 0]
    
        st.markdown("**Report Preview:**")
        st.dataframe(format_currency_columns(format_dates_mmddyyyy(report_df)), use_container_width=True, height=max(400, 40 + 40 * len(report_df)))
    
        # --- Download button ---
        st.download_button(
            label="Download Report as CSV",
            data=report_df.to_csv(index=False),
            file_name="custom_report.csv",
            mime="text/csv"
        )
    
        # --- Download as Excel ---
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            report_df.to_excel(writer, index=False, sheet_name='Report')
        st.download_button(
            label="Download Report as Excel",
            data=output.getvalue(),
            file_name="custom_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
        st.info("To print or save this report as PDF, use your browser's print feature (Ctrl+P or Cmd+P).")
    
    # --- All Policies in Database ---
    elif page == "All Policies in Database":
        st.subheader("All Policies in Database")
        st.info("Tip: Use your browser's zoom-out (Ctrl -) to see more columns. Scroll horizontally for wide tables.")
        # Reduce the height so the table fits better on the page and horizontal scroll bar is visible
        st.dataframe(format_currency_columns(format_dates_mmddyyyy(all_data)), use_container_width=True, height=350)
    
    # --- Add New Policy Transaction ---
    elif page == "Add New Policy Transaction":
        st.subheader("Add New Policy Transaction")
        import datetime
        db_columns = all_data.columns.tolist()
    
        # --- Client Name Search for Existing Client ID ---
        st.markdown("#### Search for Existing Client ID by Name")
        client_names = sorted(all_data["Customer"].dropna().unique().tolist()) if "Customer" in all_data.columns else []
        search_name = st.text_input("Type client name to search:")
        matched_id = None
        matched_name = None
        if search_name:
            matches = all_data[all_data["Customer"].str.lower().str.contains(search_name.strip().lower(), na=False)]
            if not matches.empty and "Client ID" in matches.columns:
                matched_id = matches.iloc[0]["Client ID"]
                matched_name = matches.iloc[0]["Customer"]
                st.info(f"Client ID for '{matched_name}': **{matched_id}**")
                if st.button("Assign This Client ID and Name to Transaction", key="assign_client_id_btn"):
                    st.session_state["assigned_client_id"] = matched_id
                    st.session_state["assigned_client_name"] = matched_name
            else:
                st.warning("No matching client found.")
    
        # --- Premium Sold Calculator ---
        st.markdown("### Premium Sold Calculator (for Endorsements)")
        col_calc1, col_calc2, col_calc3 = st.columns([1,1,1])
        with col_calc1:
            existing_premium = st.number_input(
                "Existing Premium",
                min_value=-1000000.0,
                max_value=1000000.0,
                step=0.01,
                format="%.2f",
                key="existing_premium_calc"
            )
        with col_calc2:
            new_premium = st.number_input(
                "New/Revised Premium",
                min_value=-1000000.0,
                max_value=1000000.0,
                step=0.01,
                format="%.2f",
                key="new_premium_calc"
            )
        with col_calc3:
            premium_sold_calc = round(new_premium - existing_premium, 2)
            st.markdown(f"**Premium Sold (New - Existing):** <span style='font-size:1.5em'>{premium_sold_calc:+.2f}</span>", unsafe_allow_html=True)
            if st.button("Use This Value for Premium Sold"):
                st.session_state["premium_sold_input_live"] = premium_sold_calc
    
        # --- Live Premium Sold and Agency Revenue outside the form ---
        if "premium_sold_input" not in st.session_state:
            st.session_state["premium_sold_input"] = 0.0
        st.subheader("Enter Premium Sold and see Agency Revenue:")
        premium_sold_val = st.number_input(
            "Premium Sold",
            min_value=-1000000.0,  # Allow large negative values
            max_value=1000000.0,
            step=0.01,
            format="%.2f",
            key="premium_sold_input_live"
        )
        agency_revenue_val = round(premium_sold_val * 0.10, 2)
        st.number_input(
            "Agency Revenue (10% of Premium Sold)",
            value=agency_revenue_val,
            disabled=True,
            format="%.2f",
            key="agency_revenue_display_live"
        )
        # --- The rest of the form ---
        with st.form("add_policy_form"):
            new_row = {}
            auto_transaction_id = generate_transaction_id() if "Transaction ID" in db_columns else None
            assigned_client_id = st.session_state.get("assigned_client_id", None)
            assigned_client_name = st.session_state.get("assigned_client_name", None)
            for col in db_columns:
                if col in [
                    "Lead Source",
                    "Producer",
                    "Agency Gross Paid",
                    "Paid",
                    "Gross Agency Comm %",
                    "Agency Gross Comm",
                    "Statement Date",
                    "STMT DATE",
                    "Items",
                    "Paid Amount",
                    "PAST DUE"
                ]:
                    continue  # Skip these fields in the form
                if col == "Premium Sold":
                    new_row[col] = premium_sold_val
                elif col == "Agency Revenue":
                    new_row[col] = agency_revenue_val
                elif col == "Transaction ID":
                    val = st.text_input(col, value=auto_transaction_id, disabled=True)
                    new_row[col] = auto_transaction_id
                elif col == "Client ID":
                    val = st.text_input(col, value=assigned_client_id if assigned_client_id else generate_client_id(), disabled=True)
                    new_row[col] = val
                elif col == "Customer":
                    val = st.text_input(col, value=assigned_client_name if assigned_client_name else "")
                    new_row[col] = val
                elif "date" in col.lower() or col.lower() in ["x-date", "xdate", "stmt date", "statement date"]:
                    # Make these date fields optional/blank by default
                    if col in ["Policy Origination Date", "Effective Date", "X-Date", "X-DATE", "Statement Date", "STMT DATE"]:
                        val = st.date_input(col, value=None, format="MM/DD/YYYY")
                        if val is None or (isinstance(val, str) and not val):
                            new_row[col] = ""
                        else:
                            new_row[col] = val.strftime("%m/%d/%Y") if isinstance(val, datetime.date) else str(val)
                    else:
                        today = datetime.date.today()
                        val = st.date_input(col, value=today, format="MM/DD/YYYY")
                        new_row[col] = val.strftime("%m/%d/%Y") if isinstance(val, datetime.date) else str(val)
                elif col == "Calculated Commission":
                    val = st.number_input(col, min_value=-1000000.0, max_value=1000000.0, step=0.01, format="%.2f")
                    new_row[col] = val
                elif col == "Paid":
                    val = st.selectbox(col, ["No", "Yes"])
                    new_row[col] = val
                elif col == "NEW/RWL":
                    val = st.selectbox(col, ["NEW", "NBS", "STL", "BoR", "END", "PCH", "RWL", "REWRITE", "CAN", "XCL"])
                    new_row[col] = val
                else:
                    val = st.text_input(col)
                    new_row[col] = val
            submitted = st.form_submit_button("Add Transaction")
        if submitted:
            # Auto-generate IDs if present
            if "Client ID" in db_columns:
                new_row["Client ID"] = generate_client_id()
            if "Transaction ID" in db_columns:
                new_row["Transaction ID"] = auto_transaction_id
            # Calculate commission if needed
            if "Calculated Commission" in db_columns:
                new_row["Calculated Commission"] = calculate_commission(new_row)
            # --- Calculate Agent Estimated Comm $ for new rows ---
            def parse_money(val):
                import re
                if val is None:
                    return 0.0
                try:
                    return float(re.sub(r'[^0-9.-]', '', str(val)))
                except Exception:
                    return 0.0
            def parse_percent(val):
                import re
                if val is None:
                    return 0.0
                try:
                    return float(re.sub(r'[^0-9.-]', '', str(val)))
                except Exception:
                    return 0.0
            if "Agent Estimated Comm $" in db_columns:
                premium = new_row.get("Premium Sold", 0)
                pct = new_row.get("Policy Gross Comm %", 0)
                p = parse_money(premium)
                pc = parse_percent(pct)
                new_row["Agent Estimated Comm $"] = p * (pc / 100.0)
            # --- Calculate Balance Due for new rows ---
            if "Balance Due" in db_columns:
                def parse_money_bd(val):
                    import re
                    if val is None:
                        return 0.0
                    try:
                        return float(re.sub(r'[^0-9.-]', '', str(val)))
                    except Exception:
                        return 0.0
                agent_est = new_row.get("Agent Estimated Comm $", 0)
                paid_amt = new_row.get("Paid Amount", 0)
                agent_est_val = parse_money_bd(agent_est)
                paid_amt_val = parse_money_bd(paid_amt)
                new_row["Balance Due"] = agent_est_val - paid_amt_val
            new_df = pd.DataFrame([new_row])
            new_df.to_sql('policies', engine, if_exists='append', index=False)
            st.success("New policy transaction added!")
    
    # --- Edit Policies in Database ---
    elif page == "Edit Policies in Database":
        st.subheader("Edit Policies in Database")
        db_columns = all_data.columns.tolist()
        st.markdown("**Reorder columns by dragging the boxes below (no delete):**")
        # Use streamlit-sortables for drag-and-drop, no delete
        order = sortables.sort_items(
            items=db_columns,
            direction="horizontal",
            key="edit_db_col_order_sortable"
        )
        edited_db_df = st.data_editor(format_currency_columns(format_dates_mmddyyyy(all_data[order].reset_index(drop=True))))
        if st.button("Update Database with Edits and Column Order"):
            edited_db_df = edited_db_df[order]
            # --- Recalculate Balance Due for all rows before saving ---
            def parse_money_bd(val):
                import re
                if val is None:
                    return 0.0
                try:
                    return float(re.sub(r'[^0-9.-]', '', str(val)))
                except Exception:
                    return 0.0
            # Robust recalculation for both 'Balance Due' and 'BALANCE DUE'
            balance_due_cols = [col for col in edited_db_df.columns if col.strip().lower() in ["balance due", "balance_due", "balance_due$", "balance due$"]]
            agent_comm_col = next((col for col in edited_db_df.columns if col.strip().lower() == "agent estimated comm $".lower()), None)
            paid_amt_col = next((col for col in edited_db_df.columns if col.strip().lower() == "paid amount".lower()), None)
            if balance_due_cols and agent_comm_col and paid_amt_col:
                for bd_col in balance_due_cols:
                    edited_db_df[bd_col] = edited_db_df.apply(
                        lambda row: parse_money_bd(row[agent_comm_col]) - parse_money_bd(row[paid_amt_col]), axis=1
                    )
                st.info(f"Recalculated '{', '.join(balance_due_cols)}' for all rows.")
                # Show a sample of recalculated values for debugging
                st.write("Sample recalculated Balance Due values:", edited_db_df[balance_due_cols].head())
            else:
                st.warning("Could not find all required columns for Balance Due recalculation.")
            edited_db_df.to_sql('policies', engine, if_exists='replace', index=False)
            # --- Force reload of all_data after update ---
            import time
            time.sleep(0.5)  # Give DB a moment to update
            all_data = pd.read_sql('SELECT * FROM policies', engine)
            st.success("Database updated with your edits and new column order! Data reloaded.")
            st.rerun()
    
    # --- Search & Filter ---
    elif page == "Search & Filter":
        st.subheader("Search & Filter Policies")
    
        # Dropdown to select which column to search by (all headers)
        columns = all_data.columns.tolist()
        default_index = columns.index("Customer") if "Customer" in columns else 0
        st.markdown(
            """
            <style>
            /* Highlight the selectbox for 'Search by column' */
            div[data-testid="stSelectbox"]:has(label:contains('Search by column')) > div[data-baseweb="select"] {
                background-color: #fff3b0 !important;
                border: 2px solid #e6a800 !important;
                border-radius: 6px !important;
            }
            /* Highlight the selectbox for 'Balance Due' */
            div[data-testid="stSelectbox"]:has(label:contains('Balance Due')) > div[data-baseweb="select"] {
                background-color: #fff3b0 !important;
                border: 2px solid #e6a800 !important;
                border-radius: 6px !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        search_column = st.selectbox("Search by column:", columns, index=default_index)
        # --- Highlighted Customer search input ---
        if search_column == "Customer":
            # Place the CSS BEFORE the text_input so it is injected before the widget renders
            st.markdown(
                """
                <style>
                /* Only highlight the border for the Customer search field, no fill */
                input[type="text"][aria-label^="Search for value in 'Customer'"] {
                    border: 2px solid #e6a800 !important;
                    background-color: white !important;
                    border-radius: 6px !important;
                    color: #222 !important;
                    position: relative;
                    z-index: 1;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            search_text = st.text_input(
                f"Search for value in '{search_column}':",
                key="search_customer_highlighted",
                help="Type a client name to search.",
                label_visibility="visible",
                placeholder="Type client name..."
            )
        else:
            search_text = st.text_input(f"Search for value in '{search_column}':")
    
        # Dropdown to filter by Balance Due status
        balance_due_options = ["All", "YES", "NO"]
        selected_balance_due = st.selectbox("Balance Due", balance_due_options)
    
        filtered_data = all_data.copy()
    
        # Apply search filter
        if search_text:
            filtered_data = filtered_data[filtered_data[search_column].astype(str).str.contains(search_text, case=False, na=False)]
    
        # Calculate BALANCE DUE if not present
        if "BALANCE DUE" not in filtered_data.columns and "Paid Amount" in filtered_data.columns and "Estimated Agent Comm (New 50% Renewal 25%)" in filtered_data.columns:
            paid_amounts = pd.to_numeric(filtered_data["Paid Amount"], errors="coerce").fillna(0)
            commission_amounts = pd.to_numeric(filtered_data["Estimated Agent Comm (New 50% Renewal 25%)"], errors="coerce").fillna(0)
            filtered_data["BALANCE DUE"] = commission_amounts - paid_amounts
    
        # Apply Balance Due filter
        if selected_balance_due != "All" and "BALANCE DUE" in filtered_data.columns:
            if selected_balance_due == "YES":
                filtered_data = filtered_data[filtered_data["BALANCE DUE"] > 0]
            elif selected_balance_due == "NO":
                filtered_data = filtered_data[filtered_data["BALANCE DUE"] <= 0]
    
        st.subheader("Filtered Policies")
        st.dataframe(format_currency_columns(format_dates_mmddyyyy(filtered_data)), use_container_width=True, height=400)  # Increased height so first row is always visible
    
        # --- Export filtered data as CSV or Excel ---
        st.markdown("**Export Filtered Results:**")
        st.download_button(
            label="Download as CSV",
            data=filtered_data.to_csv(index=False),
            file_name="filtered_policies.csv",
            mime="text/csv"
        )
    
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            filtered_data.to_excel(writer, index=False, sheet_name='Filtered Policies')
        st.download_button(
            label="Download as Excel",
            data=output.getvalue(),
            file_name="filtered_policies.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # --- Admin Panel ---
    elif page == "Admin Panel":
        st.warning("⚠️ The Admin Panel is for administrative use only. Changes here can affect your entire database. Proceed with caution!")
        # --- All other Admin Panel code goes below this line ---
        st.header("Admin Panel: Column Mapping & Header Editing")
        mapping_file = "column_mapping.json"
        default_columns = [
            "Customer", "Policy Type", "Carrier Name", "Policy Number", "NEW/RWL",
            "Agency Revenue", "Policy Origination Date", "Effective Date"
        ]
        # Load mapping
        if os.path.exists(mapping_file):
            with open(mapping_file, "r") as f:
                column_mapping = json.load(f)
        else:
            column_mapping = {}
    
        st.subheader("Current Column Mapping")
        # Always show current mapping
        if column_mapping:
            mapping_df = pd.DataFrame(list(column_mapping.items()), columns=["App Field", "Mapped To"])
            st.dataframe(mapping_df, use_container_width=True)
        else:
            st.info("No column mapping found yet.")
    
        # --- Column mapping customization as before ---
        uploaded_file = st.file_uploader("Upload a file to customize mapping", type=["xlsx", "xls", "csv", "pdf"], key="admin_upload")
        if uploaded_file:
            if uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith(".xls"):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".pdf"):
                with pdfplumber.open(uploaded_file) as pdf:
                    all_tables = []
                    for page in pdf.pages:
                        tables = page.extract_tables()
                        for table in tables:
                            temp_df = pd.DataFrame(table[1:], columns=table[0])
                            all_tables.append(temp_df)
                    if all_tables:
                        df = pd.concat(all_tables, ignore_index=True)
                    else:
                        st.error("No tables found in PDF.")
                        st.stop()
            df.columns = df.columns.str.strip()
            uploaded_columns = df.columns.tolist()
            new_mapping = {}
            for col in default_columns:
                mapped = st.selectbox(
                    f"Map '{col}' to uploaded column:",
                    options=[""] + uploaded_columns,
                    index=(uploaded_columns.index(column_mapping.get(col)) + 1) if column_mapping.get(col) in uploaded_columns else 0,
                    key=f"admin_map_{col}_panel"
                )
                if mapped:
                    new_mapping[col] = mapped
            if st.button("Save Mapping", key="admin_save_mapping"):
                column_mapping.update(new_mapping)
                with open(mapping_file, "w") as f:
                    json.dump(column_mapping, f)
                st.success("Mapping saved! Reload or re-upload to apply.")
            st.subheader("Uploaded File Columns")
            st.write(uploaded_columns)
            st.subheader("Database Columns")
            st.write(all_data.columns.tolist())
    
        # --- Add/Delete Columns Section ---
        st.subheader("Add or Delete Database Columns")
        db_columns = all_data.columns.tolist()
    
        # Add Column
        with st.form("add_column_form"):
            new_col_name = st.text_input("New column name")
            add_col_submitted = st.form_submit_button("Add Column")
    
        if add_col_submitted and new_col_name and new_col_name not in db_columns:
            st.session_state["pending_add_col"] = new_col_name
    
        if "pending_add_col" in st.session_state:
            st.warning(f"Are you sure you want to add the column '{st.session_state['pending_add_col']}'? This action cannot be undone from the app.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Continue", key="confirm_add_col"):
                    with engine.begin() as conn:
                        conn.execute(sqlalchemy.text(f'ALTER TABLE policies ADD COLUMN "{st.session_state["pending_add_col"]}" TEXT'))
                    st.success(f"Column '{st.session_state['pending_add_col']}' added.")
                    st.session_state.pop("pending_add_col")
                    st.rerun()
            with col2:
                if st.button("Cancel", key="cancel_add_col"):
                    st.info("Add column cancelled.")
                    st.session_state.pop("pending_add_col")
                    st.rerun()
    
        elif add_col_submitted and new_col_name in db_columns:
            st.warning(f"Column '{new_col_name}' already exists.")
    
        # Delete Column
        with st.form("delete_column_form"):
            st.markdown(
                """
                <style>
                /* Remove background fill for the 'Select column to delete' selectbox */
                div[data-testid="stSelectbox"]:has(label:contains('Select column to delete')) > div[data-baseweb="select"] {
                    background-color: white !important;
                    border: 2px solid #e6a800 !important;
                    border-radius: 6px !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            col_to_delete = st.selectbox("Select column to delete", [""] + db_columns, index=0)
            delete_col_submitted = st.form_submit_button("Delete Column")
    
        # --- Improved robust two-step confirmation for column deletion ---
        if delete_col_submitted and col_to_delete:
            st.session_state["pending_delete_col"] = col_to_delete
            st.session_state["delete_confirmed"] = False
            st.rerun()
    
        if "pending_delete_col" in st.session_state:
            col_name = st.session_state["pending_delete_col"]
            st.error(f"⚠️ You are about to permanently delete the column: '{col_name}'. This cannot be undone.\n\n**It is strongly recommended to BACK UP your database first!**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Confirm Delete Column", key="confirm_del_col"):
                    st.session_state["delete_confirmed"] = True
                    st.rerun()
            with col2:
                if st.button("Cancel", key="cancel_del_col"):
                    st.session_state.pop("pending_delete_col")
                    st.session_state.pop("delete_confirmed", None)
                    st.info("Delete column cancelled.")
                    st.rerun()
    
        if st.session_state.get("delete_confirmed", False):
            col_name = st.session_state["pending_delete_col"]
            remaining_cols = [col for col in db_columns if col != col_name]
            cols_str = ", ".join([f'"{col}"' for col in remaining_cols])
            with engine.begin() as conn:
                conn.execute(sqlalchemy.text('ALTER TABLE policies RENAME TO policies_old'))
                pragma = conn.execute(sqlalchemy.text('PRAGMA table_info(policies_old)')).fetchall()
                col_types = {row[1]: row[2] for row in pragma if row[1] in remaining_cols}
                create_cols = ", ".join([f'"{col}" {col_types[col]}' for col in remaining_cols])
                conn.execute(sqlalchemy.text(f'CREATE TABLE policies ({create_cols})'))
                conn.execute(sqlalchemy.text(f'INSERT INTO policies ({cols_str}) SELECT {cols_str} FROM policies_old'))
                conn.execute(sqlalchemy.text('DROP TABLE policies_old'))
            # Run VACUUM to force SQLite to update schema and clear cache
            with engine.begin() as conn:
                conn.execute(sqlalchemy.text('VACUUM'))
            st.success(f"Column '{col_name}' deleted.")
            st.session_state.pop("pending_delete_col")
            st.session_state.pop("delete_confirmed")
            st.rerun()
    
        # --- Header renaming section (at the bottom) ---
        st.subheader("Rename Database Column Headers")
        db_columns = all_data.columns.tolist()
        with st.form("rename_single_header_form"):
            col_to_rename = st.selectbox("Select column to rename", [""] + db_columns, index=0, key="rename_col_select")
            new_col_name = st.text_input("New column name", value="", key="rename_col_new_name")
            rename_submitted = st.form_submit_button("Rename Column")
    
        if rename_submitted:
            if col_to_rename and new_col_name and new_col_name != col_to_rename:
                with engine.begin() as conn:
                    conn.execute(sqlalchemy.text(f'ALTER TABLE policies RENAME COLUMN "{col_to_rename}" TO "{new_col_name}"'))
                st.success(f"Renamed column '{col_to_rename}' to '{new_col_name}'")
                st.rerun()
            elif not col_to_rename:
                st.info("Please select a column to rename.")
            else:
                st.info("Please enter a new name different from the current column name.")
    
        # --- Backup/Restore Section ---
        st.subheader("Database Backup & Restore (Recommended Before Schema Changes)")
        backup_path = "commissions_backup.db"
        backup_log_path = "commissions_backup_log.json"
    
        # Load last backup info
        last_backup_time = None
        if os.path.exists(backup_log_path):
            with open(backup_log_path, "r") as f:
                backup_log = json.load(f)
                last_backup_time = backup_log.get("last_backup_time")
        else:
            backup_log = {}
    
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Backup Database Now"):
                import shutil
                import datetime
                shutil.copyfile("commissions.db", backup_path)
                now_str = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                backup_log["last_backup_time"] = now_str
                with open(backup_log_path, "w") as f:
                    json.dump(backup_log, f)
                st.success(f"Database backed up to {backup_path} at {now_str}")
                last_backup_time = now_str
        with col2:
            if st.button("Restore Database from Backup"):
                import shutil
                if os.path.exists(backup_path):
                    shutil.copyfile(backup_path, "commissions.db")
                    st.success("Database restored from backup. Please restart the app.")
                else:
                    st.error("No backup file found. Please create a backup first.")
    
        # Show last backup time
        if last_backup_time:
            st.info(f"Last backup: {last_backup_time}")
        else:
            st.info("No backup has been made yet.")
    
        # --- Database Download/Upload Section ---
        st.subheader("Database Download & Upload")
        st.markdown("⚠️ **Use these features to sync database changes between different installations or devices.**")
        
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("**📥 Download Database**")
            st.markdown("Download the current database file to sync to another device.")
            
            if st.button("Download Database File"):
                try:
                    # Read the current database file
                    with open("commissions.db", "rb") as file:
                        db_data = file.read()
                    
                    # Create a download timestamp for the filename
                    import datetime
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"commissions_database_{timestamp}.db"
                    
                    # Provide download link
                    st.download_button(
                        label="📥 Click to Download Database File",
                        data=db_data,
                        file_name=filename,
                        mime="application/octet-stream",
                        help="Save this file to upload to another installation"
                    )
                    
                    st.success(f"Database ready for download as '{filename}'")
                    
                except Exception as e:
                    st.error(f"Error preparing database for download: {str(e)}")
        
        with col4:
            st.markdown("**📤 Upload Database**")
            st.markdown("Upload a database file to replace the current one.")
            
            uploaded_db = st.file_uploader(
                "Choose database file to upload", 
                type=['db'],
                help="Upload a .db file from another installation",
                key="admin_db_upload"
            )
            
            if uploaded_db is not None:
                st.warning("⚠️ **WARNING**: This will completely replace your current database!")
                st.markdown("**Before proceeding:**")
                st.markdown("- Make sure you've backed up your current database above")
                st.markdown("- Verify the uploaded file is from a trusted source")
                st.markdown("- This action cannot be undone")
                
                if st.checkbox("I understand this will replace my current database", key="db_replace_confirm"):
                    if st.button("🔄 Replace Database", type="primary"):
                        try:
                            # Create a backup before replacing
                            import shutil
                            import datetime
                            backup_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            backup_before_upload = f"commissions_backup_before_upload_{backup_timestamp}.db"
                            shutil.copyfile("commissions.db", backup_before_upload)
                            
                            # Write the uploaded file
                            with open("commissions.db", "wb") as f:
                                f.write(uploaded_db.getvalue())
                            
                            st.success("✅ Database successfully replaced!")
                            st.info(f"Previous database backed up as: {backup_before_upload}")
                            st.markdown("**Please refresh the page to see the new data.**")
                            
                            # Update backup log
                            now_str = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                            backup_log["last_backup_time"] = now_str
                            backup_log["backup_before_upload"] = backup_before_upload
                            with open(backup_log_path, "w") as f:
                                json.dump(backup_log, f)
                                
                        except Exception as e:
                            st.error(f"Error replacing database: {str(e)}")
                            st.error("Your original database should still be intact.")
    
        # --- Formula Documentation Section ---
        st.subheader("Current Formula Logic in App")
        st.markdown("""
        **Below are the formulas/calculations used in the app. To change a formula, you must edit the code in `commission_app.py`.**
    
        | Field/Column              | Formula/Logic                                                                 |
        |---------------------------|------------------------------------------------------------------------------|
        | Calculated Commission     | See `calculate_commission(row)` function. Logic depends on 'NEW/RWL' value.  |
        | BALANCE DUE               | `BALANCE DUE = [Estimated Agent Comm] - [Paid Amount]`                       |
        | Agency Revenue            | `Agency Revenue = Premium Sold * 0.10` (in Add New Policy Transaction form)   |
        | Total Paid Amount         | Sum of 'Paid Amount' for selected client                                      |
        | Total Balance Due         | Sum of 'BALANCE DUE' for overdue, underpaid policies                          |
        | Premium Sold (Calculator) | `Premium Sold = New/Revised Premium - Existing Premium`                       |
        """)
        st.info("To change a formula, edit the relevant function or calculation in the code. If you need help, ask your developer or Copilot.")
    
    # --- Accounting Page ---
    elif page == "Accounting":
        st.subheader("Accounting")
        import datetime
        st.info("This section provides accounting summaries, reconciliation tools, and export options. Use the reconciliation tool below to match your commission statement to your database and mark payments as received.")
    
        # --- Ensure commission_payments table exists for audit/history ---
        with engine.begin() as conn:
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS commission_payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    policy_number TEXT,
                    customer TEXT,
                    payment_amount REAL,
                    statement_date TEXT,
                    payment_timestamp TEXT
                )
            '''))
        # --- Ensure manual_commission_entries table exists for persistence ---
        with engine.begin() as conn:
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS manual_commission_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer TEXT,
                    policy_type TEXT,
                    policy_number TEXT,
                    effective_date TEXT,
                    transaction_type TEXT,
                    commission_paid REAL,
                    agency_commission_received REAL,
                    statement_date TEXT
                )
            '''))
        # --- Ensure statement_details column exists in commission_payments ---
        with engine.begin() as conn:
            try:
                conn.execute(sqlalchemy.text('ALTER TABLE commission_payments ADD COLUMN statement_details TEXT'))
            except Exception:
                pass  # Ignore if already exists
    
        # --- Load manual entries from DB if session state is empty ---
        if "manual_commission_rows" not in st.session_state or not st.session_state["manual_commission_rows"]:
            manual_entries_df = pd.read_sql('SELECT * FROM manual_commission_entries', engine)
            if not manual_entries_df.empty:
                # Convert DB rows to dicts for session state
                st.session_state["manual_commission_rows"] = [
                    {
                        "Customer": row["customer"],
                        "Policy Type": row["policy_type"],
                        "Policy Number": row["policy_number"],
                        "Effective Date": row["effective_date"],
                        "Transaction Type": row["transaction_type"],
                        "Commission Paid": row["commission_paid"],
                        "Agency Commission Received $": row["agency_commission_received"],
                        "Statement Date": row["statement_date"]
                    }
                    for _, row in manual_entries_df.iterrows()
                ]
            else:
                st.session_state["manual_commission_rows"] = []
    
        # --- Accounting UI code continues here ---
        st.markdown("## Reconcile Commission Statement")
        entry_mode = st.radio("How would you like to enter your commission statement?", ["Upload File", "Manual Entry"], key="reconcile_entry_mode")
        statement_df = None
        if entry_mode == "Upload File":
            uploaded_statement = st.file_uploader(
                "Upload your commission statement (CSV, Excel, or PDF)",
                type=["csv", "xlsx", "xls", "pdf"],
                key="reconcile_statement_upload"
            )
            if uploaded_statement:
                if uploaded_statement.name.endswith(".csv"):
                    statement_df = pd.read_csv(uploaded_statement)
                elif uploaded_statement.name.endswith(".xlsx") or uploaded_statement.name.endswith(".xls"):
                    statement_df = pd.read_excel(uploaded_statement)
                elif uploaded_statement.name.endswith(".pdf"):
                    with pdfplumber.open(uploaded_statement) as pdf:
                        all_tables = []
                        for page in pdf.pages:
                            tables = page.extract_tables()
                            for table in tables:
                                temp_df = pd.DataFrame(table[1:], columns=table[0])
                                all_tables.append(temp_df)
                        if all_tables:
                            statement_df = pd.concat(all_tables, ignore_index=True)
                        else:
                            st.error("No tables found in PDF.")
                            st.stop()
        elif entry_mode == "Manual Entry":
            st.markdown("### Manually Enter Commission Statement Data")
            # --- Stepwise dependent selection for each entry ---
            if "manual_commission_rows" not in st.session_state:
                st.session_state["manual_commission_rows"] = []
            # --- Step 1: Select Customer ---
            customers = sorted(all_data["Customer"].dropna().unique().tolist())
            selected_customer = st.selectbox("Select Customer", ["Select..."] + customers, key="recon_customer_select")
            policy_types = []
            policy_numbers = []
            effective_dates = []
            if selected_customer and selected_customer != "Select...":
                # Step 2: Policy Type (filtered)
                policy_types = sorted(all_data[all_data["Customer"] == selected_customer]["Policy Type"].dropna().unique().tolist())
                selected_policy_type = st.selectbox("Select Policy Type", ["Select..."] + policy_types, key="recon_policy_type_select")
                if selected_policy_type and selected_policy_type != "Select...":
                    # Step 3: Policy Number (filtered)
                    policy_numbers = sorted(all_data[(all_data["Customer"] == selected_customer) & (all_data["Policy Type"] == selected_policy_type)]["Policy Number"].dropna().unique().tolist())
                    selected_policy_number = st.selectbox("Select Policy Number", ["Select..."] + policy_numbers, key="recon_policy_number_select")
                    if selected_policy_number and selected_policy_number != "Select...":
                        # Step 4: Effective Date (filtered)
                        effective_dates = sorted(all_data[(all_data["Customer"] == selected_customer) & (all_data["Policy Type"] == selected_policy_type) & (all_data["Policy Number"] == selected_policy_number)]["Effective Date"].dropna().unique().tolist())
                        selected_effective_date = st.selectbox("Select Effective Date", ["Select..."] + effective_dates, key="recon_effective_date_select")
                        if selected_effective_date and selected_effective_date != "Select...":
                            # Step 5: Enter Transaction Type, Commission Paid, Agency Commission Received, and Statement Date
                            transaction_types = ["NEW", "NBS", "STL", "BoR", "END", "PCH", "RWL", "REWRITE", "CAN", "XCL"]
                            transaction_type = st.selectbox("Transaction Type", transaction_types, key="recon_transaction_type_select")
                            # New field: Agent Comm (New 50% RWL 25%) below Transaction Type
                            agent_comm_new_rwl = st.number_input(
                                "Agent Comm (New 50% RWL 25%) (%)",
                                min_value=0.0,
                                max_value=100.0,
                                step=0.01,
                                format="%.2f",
                                value=None,
                                key="recon_agent_comm_new_rwl_input",
                                help="Enter as a percent (e.g., 50 for 50%). Leave blank if not applicable."
                            )
                            # Update label to 'Agency Gross Comm Received'
                            agency_comm_received = st.number_input("Agency Gross Comm Received", min_value=0.0, step=0.01, format="%.2f", key="recon_agency_comm_received_input")
                            commission_paid = st.number_input("Commission Paid", min_value=0.0, step=0.01, format="%.2f", key="recon_comm_paid_input")
                            statement_date = st.date_input("Statement Date", value=None, format="MM/DD/YYYY", key="recon_stmt_date_input")
                            if st.button("Add Entry", key="recon_add_entry_btn"):
                                if statement_date is None or statement_date == "":
                                    stmt_date_str = ""
                                elif isinstance(statement_date, datetime.date):
                                    stmt_date_str = statement_date.strftime("%m/%d/%Y")
                                else:
                                    try:
                                        stmt_date_str = pd.to_datetime(statement_date).strftime("%m/%d/%Y")
                                    except Exception:
                                        stmt_date_str = ""
                                # Add entry to session state (now includes Transaction Type and Agent Comm (New 50% RWL 25%))
                                st.session_state["manual_commission_rows"].append({
                                    "Customer": selected_customer,
                                    "Policy Type": selected_policy_type,
                                    "Policy Number": selected_policy_number,
                                    "Effective Date": selected_effective_date,
                                    "Transaction Type": transaction_type,
                                    "Agent Comm (New 50% RWL 25%)": agent_comm_new_rwl if agent_comm_new_rwl is not None else "",
                                    "Agency Gross Comm Received": agency_comm_received,
                                    "Commission Paid": commission_paid,
                                    "Statement Date": stmt_date_str
                                })
                                st.success("Entry added. You can review and edit below.")
    
        # --- Show, edit, and delete manual entries ---
        if st.session_state["manual_commission_rows"]:
            # Always display Statement Date as MM/DD/YYYY or blank
            display_rows = []
            # Load current policies from DB for math/effect preview
            policies_df = pd.read_sql('SELECT * FROM policies', engine)
            for idx, row in enumerate(st.session_state["manual_commission_rows"]):
                date_val = row.get("Statement Date", "")
                if date_val:
                    try:
                        date_val = pd.to_datetime(date_val).strftime("%m/%d/%Y")
                    except Exception:
                        date_val = ""
                display_row = row.copy()
                display_row["Statement Date"] = date_val
                display_row["Delete"] = False  # Add a delete checkbox/button per row
                # Ensure Agency Gross Comm Received is present for all rows
                if "Agency Gross Comm Received" not in display_row:
                    # If legacy column exists, migrate value
                    if "Agency Commission Received $" in display_row:
                        display_row["Agency Gross Comm Received"] = display_row.pop("Agency Commission Received $")
                    else:
                        display_row["Agency Gross Comm Received"] = 0.0
                # Ensure Transaction Type is present for all rows (for legacy rows)
                if "Transaction Type" not in display_row:
                    display_row["Transaction Type"] = ""
                # --- Math/Effect column ---
                match = policies_df[
                    (policies_df["Policy Number"].astype(str).str.strip() == str(row.get("Policy Number", "")).strip()) &
                    (policies_df["Effective Date"].astype(str).str.strip() == str(row.get("Effective Date", "")).strip()) &
                    (policies_df["Customer"].astype(str).str.strip() == str(row.get("Customer", "")).strip())
                ]
                def parse_money(val):
                    if isinstance(val, (int, float)):
                        return float(val)
                    if isinstance(val, str):
                        return float(val.replace('$', '').replace(',', '').strip() or 0)
                    return 0.0
                # Commission Paid math
                if not match.empty:
                    db_row = match.iloc[0].to_dict()
                    existing_comm = parse_money(db_row.get("Commission Paid", 0))
                    existing_agency = parse_money(db_row.get("Agency Gross Comm Received", db_row.get("Agency Commission Received $", 0)))
                else:
                    existing_comm = 0.0
                    existing_agency = 0.0
                manual_comm = parse_money(display_row.get("Commission Paid", 0))
                manual_agency = parse_money(display_row.get("Agency Gross Comm Received", 0))
                # Transaction Type logic
                tx_type = str(row.get("Transaction Type", "")).upper()
                # Commission Paid math
                if tx_type in ["END", "ENDORSEMENT", "ADJ", "ADJUSTMENT"]:
                    result_comm = existing_comm + manual_comm
                    op_comm = "+"
                    result_agency = existing_agency + manual_agency
                    op_agency = "+"
                    op_word_comm = "Add"
                    op_word_agency = "Add"
                elif tx_type in ["CAN", "CANCEL"]:
                    result_comm = existing_comm - manual_comm
                    op_comm = "-"
                    result_agency = existing_agency - manual_agency
                    op_agency = "-"
                    op_word_comm = "Subtract"
                    op_word_agency = "Subtract"
                else:
                    # For all other types, do not allow overwrite, just add
                    result_comm = existing_comm + manual_comm
                    op_comm = "+"
                    result_agency = existing_agency + manual_agency
                    op_agency = "+"
                    op_word_comm = "Add"
                    op_word_agency = "Add"
                math_comm = (
                    f"Existing: ${existing_comm:,.2f}<br>"
                    f"{op_word_comm}: {op_comm}${abs(manual_comm):,.2f}<br>"
                    f"Result: ${result_comm:,.2f}"
                )
                math_agency = (
                    f"Existing: ${existing_agency:,.2f}<br>"
                    f"{op_word_agency}: {op_agency}${abs(manual_agency):,.2f}<br>"
                    f"Result: ${result_agency:,.2f}"
                )
                display_row["Math Effect: Commission Paid"] = math_comm
                display_row["Math Effect: Agency Commission Received"] = math_agency
                display_rows.append(display_row)
            df_manual = pd.DataFrame(display_rows)
            # Move 'Delete' column to the first position and math effect columns to the end
            cols = df_manual.columns.tolist()
            if 'Delete' in cols:
                cols.insert(0, cols.pop(cols.index('Delete')))
            # Move both math effect columns to the end
            for col in ["Math Effect: Commission Paid", "Math Effect: Agency Commission Received"]:
                if col in cols:
                    cols.append(cols.pop(cols.index(col)))
            # Remove the obsolete 'Math/Effect' column if present
            if 'Math/Effect' in cols:
                cols.remove('Math/Effect')
            df_manual = df_manual[cols]
            # Show the table with math effect columns as non-editable
            edited_df = st.data_editor(
                df_manual,
                use_container_width=True,
                key="manual_comm_rows_editor",
                height=max(400, 40 + 40 * max(10, len(df_manual))),
                disabled=[col for col in df_manual.columns if col.startswith('Math Effect:')]
            )
    
            # --- Show totals row at the bottom ---
            if not df_manual.empty:
                # Only sum numeric columns, exclude 'Delete' and math effect columns
                numeric_cols = [col for col in df_manual.columns if pd.api.types.is_numeric_dtype(df_manual[col]) and col not in ['Delete', 'Math Effect: Commission Paid', 'Math Effect: Agency Commission Received']]
                totals = {col: df_manual[col].apply(pd.to_numeric, errors='coerce').sum() for col in numeric_cols}
                # Build a totals row with blank for non-numeric columns
                totals_row = {col: (totals[col] if col in totals else "") for col in df_manual.columns}
                # Label the first non-delete, non-math effect column as 'TOTAL'
                for col in df_manual.columns:
                    if col not in ['Delete', 'Math Effect: Commission Paid', 'Math Effect: Agency Commission Received']:
                        totals_row[col] = 'TOTAL'
                        break
                # --- Add one extra blank row for visual space ---
                blank_row = {col: "" for col in df_manual.columns}
                totals_df = pd.DataFrame([totals_row, blank_row])
                st.markdown("**Totals for all manual entries below:**")
                st.dataframe(totals_df, use_container_width=True, height=50*2)
    
            # --- Save changes to pending entries ---
            if st.button("Save Changes to Pending Entries", key="save_manual_entries_btn"):
                # Remove rows marked for deletion
                new_rows = []
                for i, row in edited_df.iterrows():
                    if not row.get("Delete", False):
                        # Ensure Statement Date is MM/DD/YYYY or blank
                        date_val = row.get("Statement Date", "")
                        if date_val:
                            try:
                                date_val = pd.to_datetime(date_val).strftime("%m/%d/%Y")
                            except Exception:
                                date_val = ""
                        new_row = row.drop("Delete").to_dict()
                        new_row["Statement Date"] = date_val
                        # Ensure Transaction Type is present
                        if "Transaction Type" not in new_row:
                            new_row["Transaction Type"] = ""
                        new_rows.append(new_row)
                st.session_state["manual_commission_rows"] = new_rows
                st.success("Pending entries updated.")
                # Also update the DB table to match session state
                with engine.begin() as conn:
                    conn.execute(sqlalchemy.text('DELETE FROM manual_commission_entries'))
                    for row in new_rows:
                        conn.execute(sqlalchemy.text('''
                            INSERT INTO manual_commission_entries (customer, policy_type, policy_number, effective_date, transaction_type, commission_paid, agency_commission_received, statement_date)
                            VALUES (:customer, :policy_type, :policy_number, :effective_date, :transaction_type, :commission_paid, :agency_commission_received, :statement_date)
                        '''), {
                            "customer": row.get("Customer", ""),
                            "policy_type": row.get("Policy Type", ""),
                            "policy_number": row.get("Policy Number", ""),
                            "effective_date": row.get("Effective Date", ""),
                            "transaction_type": row.get("Transaction Type", ""),
                            "commission_paid": row.get("Commission Paid", 0.0),
                            "agency_commission_received": row.get("Agency Gross Comm Received", 0.0),
                            "statement_date": row.get("Statement Date", "")
                        })
    
            # --- Clear manual entries ---
            if st.button("Clear Manual Entries", key="clear_manual_entries_btn"):
                st.session_state["manual_commission_rows"] = []
                # Also clear the DB table
                with engine.begin() as conn:
                    conn.execute(sqlalchemy.text('DELETE FROM manual_commission_entries'))
                st.success("All manual entries cleared.")
    
            # --- Use manual entries for reconciliation ---
            if st.button("Use Manual Entries for Reconciliation", key="use_manual_entries_btn"):
                st.session_state["reconcile_with_manual_entries"] = True
                # Save all current manual entries to DB (overwrite)
    
                with engine.begin() as conn:
                    conn.execute(sqlalchemy.text('DELETE FROM manual_commission_entries'))
                    for row in st.session_state["manual_commission_rows"]:
                        conn.execute(sqlalchemy.text('''
                            INSERT INTO manual_commission_entries (customer, policy_type, policy_number, effective_date, transaction_type, commission_paid, agency_commission_received, statement_date)
                            VALUES (:customer, :policy_type, :policy_number, :effective_date, :transaction_type, :commission_paid, :agency_commission_received, :statement_date)
                        '''), {
                            "customer": row.get("Customer", ""),
                            "policy_type": row.get("Policy Type", ""),
                            "policy_number": row.get("Policy Number", ""),
                            "effective_date": row.get("Effective Date", ""),
                            "transaction_type": row.get("Transaction Type", ""),
                            "commission_paid": row.get("Commission Paid", 0.0),
                            "agency_commission_received": row.get("Agency Gross Comm Received", 0.0),
                            "statement_date": row.get("Statement Date", "")
                        })
                st.success("Manual entries ready for reconciliation.")
    
            # --- Payment/Reconciliation History Viewer ---
            st.markdown("---")
            st.markdown("### Payment/Reconciliation History")
            payment_history = pd.read_sql('SELECT * FROM commission_payments ORDER BY payment_timestamp DESC', engine)
            if not payment_history.empty:
                payment_history["statement_date"] = pd.to_datetime(payment_history["statement_date"], errors="coerce").dt.strftime("%m/%d/%Y").fillna("")
                payment_history["payment_timestamp"] = pd.to_datetime(payment_history["payment_timestamp"], errors="coerce").dt.strftime("%m/%d/%Y %I:%M %p").fillna("")
    
                for idx, row in payment_history.iterrows():
                    with st.expander(f"Statement Date: {row['statement_date']} | Customer: {row['customer']} | Amount: ${row['payment_amount']:,.2f} | Time: {row['payment_timestamp']}"):
                        # Show the full commission statement as a locked table
                        try:
                            details = json.loads(row.get('statement_details', '[]'))
                            if details:
                                df_details = pd.DataFrame(details)
                                st.dataframe(df_details, use_container_width=True, height=min(400, 40 + 40 * len(df_details)))
                            else:
                                st.info("No statement details available for this record.")
                        except Exception:
                            st.info("No statement details available or could not parse.")
            else:
                st.info("No payment/reconciliation history found.")
    
        # --- Reconcile & Commit manual entries ---
        if st.button("Reconcile & Commit Manual Entries", key="reconcile_commit_btn"):
            db_columns = pd.read_sql('SELECT * FROM policies LIMIT 1', engine).columns.tolist()
            if st.session_state["manual_commission_rows"]:
                manual_columns = list(st.session_state["manual_commission_rows"][0].keys())
            else:
                manual_columns = []
            unmatched = [col for col in manual_columns if col not in db_columns]
            mapping_file = "manual_recon_column_mapping.json"
            # Load previous mapping if it exists
            if os.path.exists(mapping_file):
                with open(mapping_file, "r") as f:
                    saved_mapping = json.load(f)
            else:
                saved_mapping = {}
            # Only prompt for new unmatched columns
            new_unmatched = [col for col in unmatched if col not in saved_mapping]
            mapping = saved_mapping.copy()
            if new_unmatched:
                st.warning("Some columns in your manual entries do not match the database columns. Please map each unmatched column to a database column or choose to skip it. This mapping will be remembered for future reconciliations.")
                for col in new_unmatched:
                    options = ["(Skip)"] + db_columns
                    selected = st.selectbox(f"Map manual entry column '{col}' to database column:", options, key=f"recon_map_{col}")
                    mapping[col] = selected if selected != "(Skip)" else None
                if st.button("Confirm Mapping and Commit", key="confirm_mapping_commit_btn"):
                    # Save mapping for future use
                    with open(mapping_file, "w") as f:
                        json.dump(mapping, f)
                    # Apply mapping to manual entries
                    mapped_entries = []
                    for row in st.session_state["manual_commission_rows"]:
                        mapped_row = {}
                        for k, v in row.items():
                            if k in mapping and mapping[k]:
                                mapped_row[mapping[k]] = v
                            elif k in db_columns:
                                mapped_row[k] = v
                        mapped_entries.append(mapped_row)
                    # Now commit mapped_entries to the database as before
                    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    n_committed = 0
                    statement_json = json.dumps(mapped_entries)
                    with engine.begin() as conn:
                        for row in mapped_entries:
                            conn.execute(sqlalchemy.text('''
                                INSERT INTO commission_payments (policy_number, customer, payment_amount, statement_date, payment_timestamp, statement_details)
                                VALUES (:policy_number, :customer, :payment_amount, :statement_date, :payment_timestamp, :statement_details)
                            '''), {
                                "policy_number": row.get("Policy Number", ""),
                                "customer": row.get("Customer", ""),
                                "payment_amount": row.get("Commission Paid", 0.0),
                                "statement_date": row.get("Statement Date", ""),
                                "payment_timestamp": now_str,
                                "statement_details": statement_json
                            })
                            n_committed += 1
                    st.success(f"Reconciled and committed {n_committed} manual entries to payment history.")
                    st.session_state["manual_commission_rows"] = []
                    # --- Clear the mapping file after successful commit
                    if os.path.exists(mapping_file):
                        os.remove(mapping_file)
    
    # --- Help Page ---
    elif page == "Help":
        st.subheader("Help & Documentation")
        st.markdown("*Comprehensive guide to using the Sales Commission Tracker - scroll through sections below for easy navigation*")
        
        # Add search functionality at the top
        with st.expander("🔍 Search Help Content"):
            st.markdown("""
            **Search for specific topics or keywords** (e.g., commission calculation, backup, export)
            
            **Quick Navigation:**
            - **Getting Started**: First-time setup, key concepts, quick start checklist
            - **Features**: Dashboard, reports, data entry, editing, search capabilities  
            - **Tips & Tricks**: Efficiency shortcuts, workflows, optimization strategies
            - **Troubleshooting**: Common issues, error messages, recovery procedures
            - **Formulas**: Commission calculations, premium formulas, validation rules
            - **FAQ**: Common questions about calculations, reports, technical issues
            - **Data Protection**: Security system, backup procedures, emergency recovery
            - **Roadmap**: Future features, development timeline, enhancement requests
            """)
            
            search_term = st.text_input("Search help content:")
            if search_term:
                st.info(f"💡 **Suggestions for '{search_term}':**")
                # Smart search suggestions based on common terms
                suggestions = {
                    "commission": "📊 See 'Formulas' section for commission calculation details",
                    "backup": "🛡️ Check 'Data Protection' section for backup procedures", 
                    "export": "🔧 Review 'Features Guide' for export options in Reports",
                    "error": "⚠️ Visit 'Troubleshooting' section for error resolution",
                    "calculate": "🧮 Check 'Formulas' section for calculation references",
                    "upload": "🛡️ See 'Data Protection' for safe upload procedures",
                    "report": "📋 Review 'Features Guide' for reporting capabilities",
                    "edit": "✏️ Check 'Features Guide' for editing instructions",
                    "search": "🔍 See 'Features Guide' for search and filter options"
                }
                
                found_suggestions = []
                for key, suggestion in suggestions.items():
                    if key.lower() in search_term.lower():
                        found_suggestions.append(suggestion)
                
                if found_suggestions:
                    for suggestion in found_suggestions:
                        st.write(f"• {suggestion}")
                else:
                    st.write("• Try browsing the sections below for comprehensive information")
                    st.write("• Use keywords like: commission, backup, export, error, calculate")
    
        st.markdown("---")
        
        # 📖 Getting Started Section
        st.markdown("""
        # 📖 Getting Started Guide
            
            ## Welcome to the Sales Commission Tracker!
            
            This application is designed to help insurance agents and agencies track sales commissions, manage policy data, and reconcile commission statements. Here's how to get started:
            
            ### 🎯 First Time Setup
            
            1. **Start with Dashboard**: Navigate using the sidebar to see your current data
            2. **Add Your First Policy**: Go to "Add New Policy Transaction" to enter your first policy
            3. **Explore Your Data**: Use "All Policies in Database" to see what you've entered
            4. **Generate Reports**: Create custom reports to analyze your commission data
            
            ### 🗂️ Understanding the Interface
            
            **Sidebar Navigation**: Use the radio buttons on the left to switch between different sections
            **Main Content Area**: This is where all the action happens - forms, tables, and reports
            **Yellow Highlighted Fields**: These are input fields where you can enter or edit data
            **Locked/Disabled Fields**: These are automatically calculated and cannot be edited directly
            
            ### 📊 Key Concepts
            
            **Client ID**: A unique identifier for each client (auto-generated)
            **Transaction ID**: A unique identifier for each policy transaction (auto-generated)
            **Policy Balance Due**: Calculated as Commission Owed minus Amount Paid
            **Statement Reconciliation**: Matching your commission statement to database records
            
            ### 🎯 Quick Start Checklist
            
            - [ ] Review the Dashboard to understand current data
            - [ ] Add a new policy transaction to test the system
            - [ ] Generate your first report
            - [ ] Explore the search and filter capabilities
            - [ ] Set up your first commission statement reconciliation
            
            ### 🔒 Data Safety
            
            Your data is automatically protected with:
            - **Automatic backups** before major changes
            - **Schema protection** to prevent data loss
            - **Audit trails** for all transactions
            - **Recovery options** in the Admin Panel
        """)
    
        st.markdown("---")
        
        st.markdown("""
        # 🔧 Complete Features Guide
        
        ## 📊 Dashboard
            
            **What it does**: Provides an overview of your commission data and quick access to client information
            
            **Key Features**:
            - **Metrics Display**: See total transactions and commission amounts at a glance
            - **Client Search**: Quickly find and edit specific client data
            - **Pagination**: Browse through client policies 10 at a time
            - **Quick Edit**: Add new transactions for existing clients directly from the dashboard
            
            **How to use**:
            1. Select a client from the dropdown to see their policies
            2. Use the page navigation to browse through multiple policies
            3. Edit data directly in the table and click "Update This Client's Data"
            4. Add new transactions by filling the blank row at the bottom
            
            ---
            
            ## 📝 Add New Policy Transaction
            
            **What it does**: Adds new insurance policies and transactions to your database
            
            **Key Features**:
            - **Client ID Lookup**: Search existing clients by name to auto-fill Client ID
            - **Premium Calculator**: Calculate premium sold for endorsements (New - Existing)
            - **Live Commission Preview**: See estimated commission as you type
            - **Auto-Generated IDs**: Automatic Client ID and Transaction ID creation
            - **Date Fields**: Easy date entry with MM/DD/YYYY format
            
            **Step-by-step process**:
            1. **Search for existing client** (optional): Type client name to find existing Client ID
            2. **Use Premium Calculator** (for endorsements): Enter existing and new premiums
            3. **Enter Premium Sold**: This auto-calculates Agency Estimated Commission
            4. **Fill out the form**: All yellow highlighted fields are editable
            5. **Submit**: Click "Add Transaction" to save
            
            **Pro Tips**:
            - The Transaction Type determines commission calculations
            - Date fields use MM/DD/YYYY format automatically
            - Client ID and Transaction ID are auto-generated for uniqueness
            
            ---
            
            ## 📋 Reports
            
            **What it does**: Creates customizable reports with filtering and export capabilities
            
            **Key Features**:
            - **Column Selection**: Choose exactly which fields to include
            - **Date Range Filtering**: Filter by any date field in your data
            - **Customer Filtering**: Focus on specific clients
            - **Balance Due Filtering**: Find policies with outstanding balances
            - **Export Options**: Download as CSV or Excel
            
            **How to create a report**:
            1. **Select Columns**: Choose which data fields to include
            2. **Set Date Range**: Pick a date column and specify the range
            3. **Apply Filters**: Optionally filter by customer or balance due status
            4. **Preview**: Review the report in the preview section
            5. **Export**: Download as CSV or Excel for further analysis
    
        ---
    
        # 💡 Tips & Tricks for Power Users
            
            ## 🚀 Efficiency Tips
            
            ### Quick Navigation
            - **Use the sidebar** to jump between sections quickly
            - **Bookmark important views** in your browser
            - **Learn keyboard shortcuts** for your browser (Ctrl+R to refresh)
            
            ### Data Entry Best Practices
            - **Use consistent naming** for customers and carriers
            - **Enter dates in MM/DD/YYYY format** for consistency
            - **Review calculations** before saving transactions
            - **Use descriptive Transaction IDs** when entering manually
            
            ### Report Generation
            - **Save time with column presets** - select frequently used column combinations
            - **Use date filters** to focus on specific time periods
            - **Export to Excel** for advanced analysis and pivot tables
            - **Filter by Balance Due** to focus on collections
            
            ## 🎯 Advanced Techniques
            
            ### Dashboard Optimization
            - **Use browser zoom** (Ctrl + or Ctrl -) to see more data
            - **Scroll horizontally** in tables to see all columns
            - **Sort by clicking headers** in data tables
            
            ### Search & Filter Power User Tips
            - **Combine multiple filters** for precise results
            - **Use partial matches** - search "Smith" to find "John Smith"
            - **Filter by date ranges** to analyze specific periods
            - **Export filtered results** to create targeted reports
            
            ### Admin Panel Mastery
            - **Always backup before changes** - use Enhanced Backup
            - **Map columns properly** for accurate calculations
            - **Test with small changes first** before bulk operations
            - **Document your custom fields** for future reference
    
        ---
    
        # ⚠️ Troubleshooting Guide
            
            ## Common Issues & Solutions
            
            ### Application Won't Load
            **Problem**: Page shows error or won't start
            **Solutions**:
            1. Refresh your browser (Ctrl+R or F5)
            2. Clear browser cache and cookies
            3. Check that all files are in the correct directory
            4. Restart the Streamlit application
            
            ### Data Not Appearing
            **Problem**: Database seems empty or missing data
            **Solutions**:
            1. Check if database file exists (commissions.db)
            2. Verify file permissions for the database
            3. Use Admin Panel to check database status
            4. Restore from backup if necessary
            
            ### Calculation Errors
            **Problem**: Commission calculations seem wrong
            **Solutions**:
            1. Check Transaction Type - this affects commission percentage
            2. Verify Policy Gross Commission % is entered correctly
            3. Ensure Premium Sold is accurate
            4. Review the Formulas tab for calculation details
            
            ### Export Issues
            **Problem**: Can't download CSV or Excel files
            **Solutions**:
            1. Check browser download settings
            2. Ensure popup blockers aren't preventing downloads
            3. Try a different browser
            4. Clear browser downloads folder if full
            
            ## Error Messages
            
            ### "Column not found" errors
            **Cause**: Database structure doesn't match expected columns
            **Solution**: Use Admin Panel to map columns or add missing columns
            
            ### "Permission denied" errors
            **Cause**: File access restrictions
            **Solution**: Run application with appropriate permissions or move to unrestricted folder
            
            ### "Database locked" errors
            **Cause**: Multiple applications trying to access database
            **Solution**: Close other applications that might be using the database file
        ---
    
        # 🧮 Formulas & Calculations Reference
            
            ## Commission Calculations
            
            ### Agent Estimated Commission
            **Formula**: `Premium Sold × (Policy Gross Comm % ÷ 100) × (Agent Comm % ÷ 100)`
            
            **Example**: 
            - Premium Sold: $1,000
            - Policy Gross Comm %: 15%
            - Agent Comm %: 50%
            - Result: $1,000 × 0.15 × 0.50 = $75
            
            ### Agency Estimated Commission/Revenue
            **Formula**: `Premium Sold × (Policy Gross Comm % ÷ 100)`
            
            **Example**:
            - Premium Sold: $1,000
            - Policy Gross Comm %: 15%
            - Result: $1,000 × 0.15 = $150
            
            ### Policy Balance Due
            **Formula**: `Agent Estimated Comm $ - Agent Paid Amount (STMT)`
            
            **Example**:
            - Agent Estimated Comm: $75
            - Agent Paid Amount: $50
            - Balance Due: $75 - $50 = $25
            
            ## Transaction Types & Commission Rates
            
            ### NEW Business (50% Commission)
            - **NEW**: New business policies
            - **NBS**: New business submitted
            - **STL**: Sold to live
            - **BoR**: Broker of record transfers
            
            ### RENEWAL Business (25% Commission)
            - **RWL**: Renewal
            - **REWRITE**: Policy rewrites
            
            ### Special Cases
            - **END**: Endorsements (50% if new policy date = effective date, otherwise 25%)
            - **PCH**: Policy changes (same rule as endorsements)
            - **CAN**: Cancellations (0% commission)
            - **XCL**: Excluded transactions (0% commission)
            
            ## Date Calculations
            
            ### Policy Terms
            - Most policies are annual (12 months)
            - X-DATE typically = Effective Date + 1 year
            - Renewal notifications typically sent 30-60 days before X-DATE
        ---
    
        # ❓ Frequently Asked Questions
            
            ## General Usage
            
            **Q: How do I add my first policy?**
            A: Go to "Add New Policy Transaction" and fill out the form. The app will auto-generate Client ID and Transaction ID for you.
            
            **Q: Can I edit existing policies?**
            A: Yes! Use "Edit Policies in Database" to modify existing data, or "Policy Revenue Ledger" for detailed transaction-level editing.
            
            **Q: How do I generate reports?**
            A: Use the "Reports" page to select columns, set filters, and export data as CSV or Excel files.
            
            **Q: What's the difference between the different commission fields?**
            A: 
            - **Agent Estimated Comm $**: What you should earn (calculated)
            - **Agent Paid Amount (STMT)**: What you actually received
            - **Policy Balance Due**: The difference (what's still owed)
            
            ## Technical Questions
            
            **Q: Where is my data stored?**
            A: All data is stored locally in a SQLite database file called "commissions.db" in the application folder.
            
            **Q: Can I backup my data?**
            A: Yes! Use the Admin Panel's "Enhanced Backup & Restore" feature to create timestamped backups.
            
            **Q: Can I import data from Excel?**
            A: Yes! Use the Admin Panel's file upload feature with column mapping to import your existing data.
            
            **Q: Is my data secure?**
            A: Your data never leaves your computer - it's stored locally and includes automatic backup protection.
            
            ## Business Questions
            
            **Q: How do I reconcile commission statements?**
            A: Use the "Accounting" page to enter commission statement data and match it against your database records.
            
            **Q: Can I track multiple agents or just myself?**
            A: The current version is designed for individual agents, but you can track multiple clients and their policies.
            
            **Q: What transaction types should I use?**
            A: Use NEW for new business (50% commission), RWL for renewals (25% commission), and CAN for cancellations.
            
            **Q: How do I handle endorsements?**
            A: Use END transaction type. Commission is 50% if it's a new policy effective date, otherwise 25%.
        """)
        
        st.markdown("""
        ---
    
        # 🛡️ Database Protection System
            
            ## Built-in Protection Features
            
            ### Automatic Backups
            - **Before major changes**: The app automatically creates backups
            - **Manual backups**: Use Admin Panel's Enhanced Backup feature
            - **Timestamped files**: Each backup includes date and time
            - **Safe storage**: Backups are stored in the same folder as your app
            
            ### Database Integrity
            - **Schema protection**: Database structure is validated on startup
            - **Data validation**: Input validation prevents corrupt data
            - **Audit trails**: All changes are logged for accountability
            - **Recovery options**: Multiple ways to restore data if needed
            
            ### File Security
            - **Local storage**: Your data never leaves your computer
            - **No cloud dependency**: Works completely offline
            - **File permissions**: Standard operating system security applies
            - **Backup encryption**: Consider encrypting backup files for extra security
            
            ## Best Practices
            
            ### Regular Backups
            1. **Weekly backups**: Create Enhanced backups at least weekly
            2. **Before major changes**: Always backup before bulk operations
            3. **Store safely**: Keep backups in a separate location (USB, cloud storage)
            4. **Test restores**: Periodically test that backups work properly
            
            ### Access Control
            - **Secure your computer**: Use password protection and screen locks
            - **Limit access**: Only authorized users should access the application
            - **Monitor changes**: Review the application logs periodically
            - **Update regularly**: Keep your operating system and browser updated
            
            ### Data Hygiene
            - **Clean data entry**: Consistent naming and formatting
            - **Regular reviews**: Periodically audit your data for accuracy
            - **Remove test data**: Clean out any test entries
            - **Document changes**: Keep notes about major data modifications
    
        ---
    
        # 🗺️ Development Roadmap
            
            ## Recently Added Features ✅
            
            ### Enhanced Database Protection
            - Automatic backup system with timestamps
            - Database integrity monitoring
            - Protected upload with multiple confirmations
            - Recovery center with backup management
            
            ### Improved User Experience
            - Column reordering in Edit Policies
            - Enhanced help system with tabs
            - Better error handling and user feedback
            - Responsive design improvements
            
            ### Advanced Reporting
            - Policy Revenue Ledger with transaction-level detail
            - Customizable reports with column selection
            - Export capabilities for CSV and Excel
            - Date range filtering and customer filtering
            
            ## Planned Features 🚧
            
            ### Short Term (Next Release)
            - **Mobile responsiveness**: Better experience on phones and tablets
            - **Dark mode**: Optional dark theme for better usability
            - **Bulk operations**: Upload multiple policies from Excel/CSV
            - **Advanced search**: More powerful search and filtering options
            
            ### Medium Term (Next 3 Months)
            - **Multi-agent support**: Track multiple agents in one database
            - **Commission tracking**: Enhanced commission statement reconciliation
            - **Automated calculations**: More sophisticated commission calculations
            - **Reporting dashboards**: Visual charts and graphs for better insights
            
            ### Long Term (6-12 Months)
            - **Cloud sync**: Optional cloud backup and sync between devices
            - **API integration**: Connect with carrier systems and CRM platforms
            - **Mobile app**: Dedicated mobile application for on-the-go access
            - **Team collaboration**: Multi-user access with role-based permissions
            
            ## Feature Requests
            
            **Have an idea for a new feature?** We're always looking to improve the application based on user feedback.
            
            **Common requests we're considering**:
            - Integration with popular insurance carriers
            - Automated commission statement importing
            - Advanced analytics and trend analysis
            - Customer relationship management (CRM) features
            - Automated renewal reminders and tracking
            
            **Priority is given to features that**:
            - Improve day-to-day efficiency
            - Reduce manual data entry
            - Enhance data accuracy and protection
            - Provide better business insights
            
            ## Version History
            
            **Current Version**: 2.0 (Enhanced Protection & Usability)
            - Added database protection system
            - Enhanced help and documentation
            - Improved user interface and experience
            - Better error handling and recovery options
            
            **Previous Version**: 1.0 (Core Functionality)
            - Basic commission tracking
            - Simple reporting and export
            - Database storage and management
            - Initial user interface
    
        This roadmap is a living document that evolves based on user needs, technological advances, and industry requirements. Your feedback and suggestions are invaluable in shaping the future of the Sales Commission Tracker!
        """)
    
    # --- Policy Revenue Ledger ---
    elif page == "Policy Revenue Ledger":
        st.subheader("Policy Revenue Ledger")
        st.info("Search for a policy to view and edit a detailed ledger of all commission credits and debits for that policy. You can edit, delete transactions below. Be sure to click 'Save Changes' to commit your edits.")
    
        # --- Granular Policy Search ---
        customers = all_data["Customer"].dropna().unique().tolist() if "Customer" in all_data.columns else []
        selected_customer = st.selectbox("Select Customer:", ["Select..."] + sorted(customers), key="ledger_customer_select")
    
        filtered_data = all_data.copy()
        if selected_customer and selected_customer != "Select...":
            filtered_data = filtered_data[filtered_data["Customer"] == selected_customer]
    
        policy_types = filtered_data["Policy Type"].dropna().unique().tolist() if "Policy Type" in filtered_data.columns else []
        selected_policy_type = st.selectbox("Select Policy Type:", ["Select..."] + sorted(policy_types), key="ledger_policytype_select")
        if selected_policy_type and selected_policy_type != "Select...":
            filtered_data = filtered_data[filtered_data["Policy Type"] == selected_policy_type]
    
        effective_dates = filtered_data["Effective Date"].dropna().unique().tolist() if "Effective Date" in filtered_data.columns else []
        selected_effective_date = st.selectbox("Select Policy Effective Date:", ["Select..."] + sorted(effective_dates), key="ledger_effectivedate_select")
        if selected_effective_date and selected_effective_date != "Select...":
            filtered_data = filtered_data[filtered_data["Effective Date"] == selected_effective_date]
    
        # Only show policy number select if all three are chosen
        policy_numbers = filtered_data["Policy Number"].dropna().unique().tolist() if "Policy Number" in filtered_data.columns else []
        selected_policy = None
        if selected_customer != "Select..." and selected_policy_type != "Select..." and selected_effective_date != "Select...":
            selected_policy = st.selectbox("Select Policy Number:", ["Select..."] + sorted(policy_numbers), key="ledger_policy_select")
    
        if selected_policy and selected_policy != "Select...":
            # Get all rows for this policy, using only real database data
            policy_rows = all_data[all_data["Policy Number"] == selected_policy].copy()
            # Define the original ledger columns
            ledger_columns = [
                "Transaction ID",
                "Description", 
                "Credit (Commission Owed)",
                "Debit (Paid to Agent)",
                "Transaction Type"
            ]
    
            # --- Always include all ledger columns, filling missing with empty values ---
            if not policy_rows.empty:
                # --- Ledger construction using mapped column names ---
                # Get mapped column names for credits and debits
                credit_col = get_mapped_column("Agent Estimated Comm $") or "Agent Estimated Comm $"
                debit_col = get_mapped_column("Agent Paid Amount (STMT)") or "Agent Paid Amount (STMT)"
                transaction_id_col = get_mapped_column("Transaction ID") or "Transaction ID"
                description_col = get_mapped_column("Description") or "Description"
                transaction_type_col = get_mapped_column("Transaction Type") or "Transaction Type"
                
                # Build ledger_df with correct mapping
                ledger_df = pd.DataFrame()
                ledger_df["Transaction ID"] = policy_rows[transaction_id_col] if transaction_id_col in policy_rows.columns else ""
                ledger_df["Description"] = policy_rows[description_col] if description_col in policy_rows.columns else ""
                
                # Credit (Commission Owed) from mapped Agent Estimated Comm $
                if credit_col in policy_rows.columns:
                    ledger_df["Credit (Commission Owed)"] = policy_rows[credit_col]
                else:
                    ledger_df["Credit (Commission Owed)"] = 0.0
                    
                # Debit (Paid to Agent) from mapped Agent Paid Amount (STMT)
                if debit_col in policy_rows.columns:
                    ledger_df["Debit (Paid to Agent)"] = policy_rows[debit_col]
                else:
                    ledger_df["Debit (Paid to Agent)"] = 0.0
                ledger_df["Transaction Type"] = policy_rows[transaction_type_col] if transaction_type_col in policy_rows.columns else ""
                # Ensure correct column order
                ledger_df = ledger_df[ledger_columns]
                # Reset index for clean display
                ledger_df = ledger_df.reset_index(drop=True)
            else:
                # If no rows, show empty DataFrame with correct columns
                ledger_df = pd.DataFrame(columns=ledger_columns)
                    
            if not ledger_df.empty:
                st.markdown("### Policy Details (Editable)")
                # Show policy-level details using mapped column names
                policy_detail_field_names = [
                    "Customer", "Client ID", "Policy Number", "Policy Type", "Carrier Name",
                    "Effective Date", "Policy Origination Date", "Policy Gross Comm %", 
                    "Agent Comm (NEW 50% RWL 25%)", "X-DATE"
                ]
                policy_detail_cols = []
                for field_name in policy_detail_field_names:
                    mapped_col = get_mapped_column(field_name)
                    if mapped_col and mapped_col in policy_rows.columns:
                        policy_detail_cols.append(mapped_col)
                    elif field_name in policy_rows.columns:
                        policy_detail_cols.append(field_name)
                
                policy_details_df = policy_rows.iloc[[0]][policy_detail_cols].copy() if not policy_rows.empty else pd.DataFrame(columns=policy_detail_cols)
                edited_details_df = st.data_editor(
                    policy_details_df,
                    use_container_width=True,
                    key="policy_details_editor",
                    num_rows="fixed",
                    height=100
                )
                
                if st.button("Save Policy Details", key="save_policy_details_btn") and not edited_details_df.empty:
                    update_sql = "UPDATE policies SET " + ", ".join([f'"{col}" = :{col}' for col in policy_detail_cols if col != "Policy Number"]) + " WHERE \"Policy Number\" = :policy_number"
                    update_params = {col: edited_details_df.iloc[0][col] for col in policy_detail_cols if col != "Policy Number"}
                    update_params["policy_number"] = edited_details_df.iloc[0]["Policy Number"]
                    with engine.begin() as conn:
                        conn.execute(sqlalchemy.text(update_sql), update_params)
                    st.success("Policy details updated.")
                    st.rerun()
    
                st.markdown("### Policy Ledger (Editable)")
                # Ensure Credit and Debit columns are numeric
                if "Credit (Commission Owed)" in ledger_df.columns:
                    ledger_df["Credit (Commission Owed)"] = pd.to_numeric(ledger_df["Credit (Commission Owed)"], errors="coerce").fillna(0.0)
                if "Debit (Paid to Agent)" in ledger_df.columns:
                    ledger_df["Debit (Paid to Agent)"] = pd.to_numeric(ledger_df["Debit (Paid to Agent)"], errors="coerce").fillna(0.0)
    
                # Lock formula columns
                column_config = {}
                column_config["Credit (Commission Owed)"] = {
                    "disabled": True,
                    "help": "This column is automatically calculated and cannot be edited."
                }
                column_config["Debit (Paid to Agent)"] = {
                    "disabled": True,
                    "help": "This column is automatically calculated and cannot be edited."
                }
                column_config["Transaction ID"] = {
                    "disabled": True,
                    "help": "Transaction ID is a unique identifier and cannot be changed."
                }
    
                # Show the table as editable, with locked columns
                edited_ledger_df = st.data_editor(
                    ledger_df,
                    use_container_width=True,
                    height=max(400, 40 + 40 * len(ledger_df)),
                    key="policy_ledger_editor",
                    num_rows="fixed",
                    column_config=column_config,
                    hide_index=True
                )
    
                # --- Ledger Totals Section ---
                total_credits = edited_ledger_df["Credit (Commission Owed)"].apply(pd.to_numeric, errors="coerce").sum() if "Credit (Commission Owed)" in edited_ledger_df.columns else 0.0
                total_debits = edited_ledger_df["Debit (Paid to Agent)"].apply(pd.to_numeric, errors="coerce").sum() if "Debit (Paid to Agent)" in edited_ledger_df.columns else 0.0
                balance_due = total_credits - total_debits
    
                st.markdown("#### Ledger Totals")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Credits", f"${total_credits:,.2f}")
                with col2:
                    st.metric("Total Debits", f"${total_debits:,.2f}")
                with col3:
                    st.metric("Balance Due", f"${balance_due:,.2f}")
    
                if st.button("Save Changes", key="save_policy_ledger_btn"):
                    for idx, row in edited_ledger_df.iterrows():
                        update_sql = "UPDATE policies SET " + ", ".join([f'"{col}" = :{col}' for col in ledger_columns if col != "Transaction ID"]) + " WHERE \"Transaction ID\" = :transaction_id"
                        update_params = {col: row[col] for col in ledger_columns if col != "Transaction ID"}
                        update_params["transaction_id"] = row["Transaction ID"]
                        with engine.begin() as conn:
                            conn.execute(sqlalchemy.text(update_sql), update_params)
                    st.success("Policy ledger changes saved.")
                    st.rerun()
    
    elif page == "Policy Revenue Ledger Reports":
        st.subheader("Policy Revenue Ledger Reports")
        st.success("📊 Generate customizable reports for policy summaries with Balance Due calculations and export capabilities.")
        
        if all_data.empty:
            st.warning("No policy data loaded. Please check database connection or import data.")
        else:
            # Simple data processing - AGGREGATE BY POLICY NUMBER using mapped columns
            working_data = all_data.copy()
            policy_number_col = get_mapped_column("Policy Number") or "Policy Number"
            
            if policy_number_col in working_data.columns and not working_data.empty:
                agg_dict = {}
                
                # For descriptive fields, take the first value
                descriptive_field_names = ["Customer", "Policy Type", "Carrier Name", "Effective Date", 
                                            "Policy Origination Date", "X-DATE", "Client ID"]
                for field_name in descriptive_field_names:
                    mapped_col = get_mapped_column(field_name)
                    target_col = mapped_col if mapped_col and mapped_col in working_data.columns else (field_name if field_name in working_data.columns else None)
                    if target_col:
                        agg_dict[target_col] = 'first'
    
                # For monetary fields, sum all transactions for each policy
                monetary_field_names = ["Agent Estimated Comm $", "Agent Paid Amount (STMT)", 
                                        "Agency Estimated Comm/Revenue (CRM)", "Premium Sold", "Policy Gross Comm %"]
                for field_name in monetary_field_names:
                    mapped_col = get_mapped_column(field_name)
                    target_col = mapped_col if mapped_col and mapped_col in working_data.columns else (field_name if field_name in working_data.columns else None)
                    if target_col:
                        working_data[target_col] = pd.to_numeric(working_data[target_col], errors='coerce').fillna(0)
                        agg_dict[target_col] = 'sum'
                
                # Group by Policy Number and aggregate
                working_data = working_data.groupby('Policy Number', as_index=False).agg(agg_dict)
            
            # Calculate Policy Balance Due
            if "Policy Balance Due" in working_data.columns:
                working_data = working_data.drop(columns=["Policy Balance Due"])
            
            if "Agent Paid Amount (STMT)" in working_data.columns and "Agent Estimated Comm $" in working_data.columns:
                paid_amounts = pd.to_numeric(working_data["Agent Paid Amount (STMT)"], errors="coerce").fillna(0)
                commission_amounts = pd.to_numeric(working_data["Agent Estimated Comm $"], errors="coerce").fillna(0)
                working_data["Policy Balance Due"] = commission_amounts - paid_amounts
            else:
                working_data["Policy Balance Due"] = 0
            
            if "Policy Balance Due" in working_data.columns:
                working_data["Policy Balance Due"] = pd.to_numeric(working_data["Policy Balance Due"], errors="coerce").fillna(0)
    
            # Calculate metrics
            total_policies = len(working_data)
            if "Policy Balance Due" in working_data.columns:
                outstanding_policies = len(working_data[working_data["Policy Balance Due"] > 0])
                total_balance = working_data["Policy Balance Due"].sum()
            else:
                outstanding_policies = 0
                total_balance = 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Policies", f"{total_policies:,}")
            with col2:
                st.metric("Outstanding Balances", f"{outstanding_policies:,}")
            with col3:
                st.metric("Total Balance Due", f"${total_balance:,.2f}")
            
            # Column Selection
            st.markdown("### 🔧 Column Selection")
            if "prl_templates" not in st.session_state:
                st.session_state.prl_templates = {}
            
            all_columns = list(working_data.columns)
            default_columns = ["Customer", "Policy Number", "Agent Estimated Comm $", "Agent Paid Amount (STMT)", "Policy Balance Due"]
            available_default_columns = [col for col in default_columns if col in all_columns]
            
            if "prl_selected_columns" not in st.session_state:
                st.session_state.prl_selected_columns = available_default_columns
    
            selected_columns = st.multiselect(
                "Choose columns to display in your report",
                options=all_columns,
                default=st.session_state.prl_selected_columns,
                key="prl_column_multiselect"
            )
            st.session_state.prl_selected_columns = selected_columns
            
            # Data Preview
            st.markdown("### 📊 Report Preview")
            if selected_columns and not working_data.empty:
                valid_columns = [col for col in selected_columns if col in working_data.columns]
                
                if valid_columns:
                    records_per_page = st.selectbox(
                        "Records per page:",
                        options=[20, 50, 100, 200, 500, "All"],
                        index=0,
                        key="prl_records_per_page"
                    )
                    
                    if records_per_page == "All":
                        display_data = working_data[valid_columns]
                        caption_text = f"Showing all {len(working_data):,} records with {len(valid_columns)} columns"
                    else:
                        current_page = st.number_input("Page:", min_value=1, value=1, key="prl_current_page")
                        records_per_page_int = int(records_per_page)
                        start_idx = (current_page - 1) * records_per_page_int
                        end_idx = start_idx + records_per_page_int
                        display_data = working_data[valid_columns].iloc[start_idx:end_idx]
                        caption_text = f"Showing records {start_idx + 1}-{min(end_idx, len(working_data))} of {len(working_data):,} total records"
                    
                    st.dataframe(display_data, use_container_width=True)
                    st.caption(caption_text)
    
                    # Export functionality
                    export_col1, export_col2 = st.columns(2)
                    with export_col1:
                        import datetime as dt
                        filename = f"policy_report_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        csv_data = working_data[valid_columns].to_csv(index=False)
                        st.download_button(
                            "📄 Export as CSV",
                            csv_data,
                            f"{filename}.csv",
                            "text/csv"
                        )
                    
                    with export_col2:
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                            working_data[valid_columns].to_excel(writer, sheet_name='Policy Revenue Report', index=False)
                        excel_buffer.seek(0)
                        
                        st.download_button(
                            "📊 Export as Excel",
                            excel_buffer.getvalue(),
                            f"{filename}.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                else:
                    st.warning("Selected columns are not available in the current data.")
            else:
                if not selected_columns:
                    st.info("Please select columns to display the report.")
                else:
                    st.warning("No data available for report generation.")
    
    elif page == "Pending Policy Renewals":
        st.subheader("Pending Policy Renewals")
        st.info("📅 View and manage policies that are due for renewal based on their expiration dates.")
        
        if all_data.empty:
            st.warning("No policy data loaded. Please check database connection or import data.")
        else:
            # Get mapped column names
            policy_number_col = get_mapped_column("Policy Number") or "Policy Number"
            transaction_type_col = get_mapped_column("Transaction Type") or "Transaction Type"
            x_date_col = get_mapped_column("X-DATE") or "X-DATE"
            customer_col = get_mapped_column("Customer") or "Customer"
            effective_date_col = get_mapped_column("Effective Date") or "Effective Date"
            
            # Filter for NEW and RWL transactions that have expired
            import datetime
            today = datetime.date.today()
            
            # Check if required columns exist
            if transaction_type_col in all_data.columns and x_date_col in all_data.columns:
                try:
                    # Filter policies that are due for renewal
                    renewal_candidates = all_data[
                        all_data[transaction_type_col].isin(["NEW", "RWL"])
                    ].copy()
                    
                    # Convert X-DATE to datetime and filter expired policies
                    if x_date_col in renewal_candidates.columns:
                        # First check if there's any data to process
                        if renewal_candidates.empty:
                            st.info("No NEW or RWL transactions found in the database.")
                        else:
                            # Convert X-DATE to datetime with proper error handling
                            renewal_candidates[x_date_col] = pd.to_datetime(renewal_candidates[x_date_col], errors='coerce')
                            
                            # Check if any valid dates were found after conversion
                            valid_dates_count = renewal_candidates[x_date_col].notna().sum()
                            if valid_dates_count == 0:
                                st.warning(f"No valid dates found in {x_date_col} column. Please check your date formats.")
                            else:
                                # Remove rows with invalid dates
                                renewal_candidates = renewal_candidates.dropna(subset=[x_date_col])
                                
                                # Filter for expired policies (X-DATE is in the past)
                                try:
                                    # Double-check that we have valid datetime data before using .dt accessor
                                    if not renewal_candidates.empty and renewal_candidates[x_date_col].notna().any():
                                        expired_policies = renewal_candidates[
                                            renewal_candidates[x_date_col].dt.date < today
                                        ]
                                    else:
                                        expired_policies = pd.DataFrame()
                                except Exception as e:
                                    st.error(f"Error processing dates: {str(e)}")
                                    expired_policies = pd.DataFrame()
                    else:
                        st.error(f"Column '{x_date_col}' not found in database.")
                        expired_policies = pd.DataFrame()
                    
                    # Get the most recent transaction for each policy
                    if not expired_policies.empty and policy_number_col in expired_policies.columns:
                        # Group by policy number and get the most recent transaction
                        latest_transactions = expired_policies.loc[
                            expired_policies.groupby(policy_number_col)[x_date_col].idxmax()
                        ]
                        
                        # Calculate renewal metrics
                        total_due_for_renewal = len(latest_transactions)
                        
                        # Display metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Policies", f"{len(all_data):,}")
                        with col2:
                            st.metric("Due for Renewal", f"{total_due_for_renewal:,}")
                        with col3:
                            renewal_percentage = (total_due_for_renewal / len(all_data) * 100) if len(all_data) > 0 else 0
                            st.metric("Renewal Rate", f"{renewal_percentage:.1f}%")
                        
                        if not latest_transactions.empty:
                            st.markdown("### 📋 Policies Due for Renewal")
                            
                            # Add calculated renewal date (X-DATE + 1 year)
                            display_data = latest_transactions.copy()
                            
                            # Ensure X-DATE column is datetime in display_data
                            try:
                                if x_date_col in display_data.columns:
                                    # Initialize columns with default values first
                                    display_data["Days Overdue"] = 0
                                    display_data["Proposed Renewal Date"] = "Invalid Date"
                                    
                                    # Convert to datetime with multiple validation steps
                                    display_data[x_date_col] = pd.to_datetime(display_data[x_date_col], errors='coerce')
                                    
                                    # Validate that conversion actually created datetime objects
                                    if not pd.api.types.is_datetime64_any_dtype(display_data[x_date_col]):
                                        st.warning(f"Unable to convert {x_date_col} to datetime format.")
                                    else:
                                        # Only calculate for rows with valid dates (not NaT)
                                        valid_date_mask = display_data[x_date_col].notna()
                                        valid_count = valid_date_mask.sum()
                                        
                                        if valid_count > 0:
                                            try:
                                                # Extract only valid dates for calculation
                                                valid_dates = display_data.loc[valid_date_mask, x_date_col]
                                                
                                                # Additional safety: remove any remaining non-datetime values
                                                try:
                                                    # Test .dt accessor on a small sample
                                                    if len(valid_dates) > 0:
                                                        test_sample = valid_dates.iloc[:1]
                                                        _ = test_sample.dt.date  # Test if .dt accessor works
                                                except:
                                                    # If .dt accessor fails, try to clean the data further
                                                    valid_dates = pd.to_datetime(valid_dates, errors='coerce')
                                                    # Update the mask to reflect the original dataframe indices
                                                    original_indices = valid_dates.index
                                                    final_valid_mask = valid_dates.notna()
                                                    # Update the original mask to only include the truly valid dates
                                                    valid_date_mask = display_data.index.isin(original_indices[final_valid_mask])
                                                    valid_dates = valid_dates[final_valid_mask]
                                                
                                                # Double-check that valid_dates is actually datetime
                                                if pd.api.types.is_datetime64_any_dtype(valid_dates) and len(valid_dates) > 0:
                                                    # Calculate days overdue for valid dates only
                                                    try:
                                                        days_overdue = (today - valid_dates.dt.date).dt.days
                                                        display_data.loc[valid_date_mask, "Days Overdue"] = days_overdue
                                                    except Exception as date_calc_error:
                                                        # Fallback method without .dt accessor
                                                        try:
                                                            import datetime as dt
                                                            days_overdue_fallback = []
                                                            for date_val in valid_dates:
                                                                if pd.notna(date_val):
                                                                    if hasattr(date_val, 'date'):
                                                                        days_diff = (today - date_val.date()).days
                                                                    else:
                                                                        # Convert to date manually
                                                                        date_obj = pd.to_datetime(date_val).date()
                                                                        days_diff = (today - date_obj).days
                                                                    days_overdue_fallback.append(days_diff)
                                                                else:
                                                                    days_overdue_fallback.append(0)
                                                            display_data.loc[valid_date_mask, "Days Overdue"] = days_overdue_fallback
                                                        except Exception:
                                                            st.warning(f"Could not calculate days overdue: {str(date_calc_error)}")
                                                    
                                                    # Calculate proposed renewal date for valid dates only
                                                    try:
                                                        proposed_dates = (valid_dates + pd.DateOffset(years=1)).dt.strftime("%m/%d/%Y")
                                                        display_data.loc[valid_date_mask, "Proposed Renewal Date"] = proposed_dates
                                                    except Exception as renewal_calc_error:
                                                        # Simple fallback method without .dt accessor
                                                        try:
                                                            import datetime as dt
                                                            renewal_dates_fallback = []
                                                            for date_val in valid_dates:
                                                                if pd.notna(date_val):
                                                                    try:
                                                                        # Convert to date and add 1 year (365 days)
                                                                        if hasattr(date_val, 'date'):
                                                                            base_date = date_val.date()
                                                                        else:
                                                                            base_date = pd.to_datetime(date_val).date()
                                                                        renewal_date = base_date.replace(year=base_date.year + 1)
                                                                        renewal_dates_fallback.append(renewal_date.strftime("%m/%d/%Y"))
                                                                    except:
                                                                        renewal_dates_fallback.append("Invalid Date")
                                                                else:
                                                                    renewal_dates_fallback.append("Invalid Date")
                                                            display_data.loc[valid_date_mask, "Proposed Renewal Date"] = renewal_dates_fallback
                                                        except Exception:
                                                            st.warning(f"Could not calculate renewal dates: {str(renewal_calc_error)}")
                                                else:
                                                    st.warning("Date validation failed - data is not in proper datetime format.")
                                            except Exception as calc_error:
                                                st.warning(f"Error in renewal calculations: {str(calc_error)}")
                                        else:
                                            st.info("No valid dates found for renewal calculations.")
                                else:
                                    st.error(f"Column {x_date_col} not found in data.")
                            except Exception as e:
                                st.error(f"Error calculating renewal dates: {str(e)}")
                                display_data["Days Overdue"] = 0
                                display_data["Proposed Renewal Date"] = "Error"
                            
                            # Select relevant columns for display
                            display_columns = []
                            for col in [customer_col, policy_number_col, transaction_type_col, effective_date_col, x_date_col, "Days Overdue", "Proposed Renewal Date"]:
                                if col in display_data.columns:
                                    display_columns.append(col)
                            
                            if display_columns:
                                # Format dates for display with error handling
                                try:
                                    if x_date_col in display_data.columns:
                                        # Check if column is datetime, if not convert it first
                                        if not pd.api.types.is_datetime64_any_dtype(display_data[x_date_col]):
                                            display_data[x_date_col] = pd.to_datetime(display_data[x_date_col], errors='coerce')
                                        # Format only valid dates, keep NaT as empty string
                                        display_data[x_date_col] = display_data[x_date_col].dt.strftime("%m/%d/%Y").fillna("")
                                    if effective_date_col in display_data.columns:
                                        # Format effective date with NaT handling
                                        effective_datetime = pd.to_datetime(display_data[effective_date_col], errors='coerce')
                                        display_data[effective_date_col] = effective_datetime.dt.strftime("%m/%d/%Y").fillna("")
                                except Exception as e:
                                    st.warning(f"Date formatting issue: {str(e)}. Displaying raw date values.")
                                
                                # Pagination
                                records_per_page = st.selectbox(
                                    "Records per page:",
                                    options=[20, 50, 100, 200, "All"],
                                    index=0,
                                    key="renewals_records_per_page"
                                )
                                
                                if records_per_page == "All":
                                    display_subset = display_data[display_columns]
                                else:
                                    current_page = st.number_input("Page:", min_value=1, value=1, key="renewals_current_page")
                                    start_idx = (current_page - 1) * records_per_page
                                    end_idx = start_idx + records_per_page
                                    display_subset = display_data[display_columns].iloc[start_idx:end_idx]
                                
                                # Display data
                                st.dataframe(display_subset, use_container_width=True)
                                
                                # Export functionality
                                st.markdown("### 📊 Export Renewal Report")
                                export_col1, export_col2 = st.columns(2)
                                
                                with export_col1:
                                    import datetime as dt
                                    filename = f"pending_renewals_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                                    csv_data = display_data[display_columns].to_csv(index=False)
                                    st.download_button(
                                        "📄 Export as CSV",
                                        csv_data,
                                        f"{filename}.csv",
                                        "text/csv",
                                        help="Download pending renewals report as CSV"
                                    )
                                
                                with export_col2:
                                    excel_buffer = io.BytesIO()
                                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                        display_data[display_columns].to_excel(writer, sheet_name='Pending Renewals', index=False)
                                    excel_buffer.seek(0)
                                    
                                    st.download_button(
                                        "📊 Export as Excel",
                                        excel_buffer.getvalue(),
                                        f"{filename}.xlsx",
                                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                        help="Download pending renewals report as Excel"
                                    )
                                
                                # Summary information
                                st.markdown("### 📈 Renewal Summary")
                                summary_data = {
                                    "Total Policies in Database": len(all_data),
                                    "Policies Due for Renewal": total_due_for_renewal,
                                    "Average Days Overdue": f"{display_data['Days Overdue'].mean():.1f}" if not display_data.empty else "0",
                                    "Most Overdue Policy": f"{display_data['Days Overdue'].max()} days" if not display_data.empty else "N/A"
                                }
                                
                                summary_df = pd.DataFrame(list(summary_data.items()), columns=["Metric", "Value"])
                                st.dataframe(summary_df, use_container_width=True, hide_index=True)
                            else:
                                st.warning("Required columns not found for displaying renewal data.")
                        else:
                            st.success("🎉 No policies are currently due for renewal!")
                    else:
                        st.info("No expired policies found or missing policy number column.")
                
                except Exception as e:
                    st.error(f"Error processing renewal data: {str(e)}")
                    st.info("This may be due to data format issues. Please check your X-DATE column format.")
            else:
                missing_cols = []
                if transaction_type_col not in all_data.columns:
                    missing_cols.append("Transaction Type")
                if x_date_col not in all_data.columns:
                    missing_cols.append("X-DATE")
                st.warning(f"Missing required columns for renewal analysis: {', '.join(missing_cols)}")

# Call main function  
main()
