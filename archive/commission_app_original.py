import streamlit as st
st.set_page_config(layout="wide")
import traceback
import string
import random
import pandas as pd
import sqlalchemy
import datetime
import io
import streamlit_sortables
import os
import json
import pdfplumber
import shutil
import uuid
from pathlib import Path
from column_mapping_config import (
    column_mapper, get_mapped_column, get_ui_field_name, 
    is_calculated_field, safe_column_reference
)

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
            transform: translateX(0px) !important;
            margin-left: 0px !important;
        }
        
        /* Force sidebar to stay expanded even when marked as collapsed */
        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(0px) !important;
            margin-left: 0px !important;
            left: 0 !important;
        }
        
        /* Hide ALL possible collapse/hide buttons with comprehensive selectors */
        button[data-testid="collapsedControl"],
        button[kind="header"],
        [data-testid="stSidebarNav"] button[kind="header"],
        [data-testid="stSidebar"] button[kind="header"],
        [data-testid="stSidebar"] [data-testid="collapsedControl"],
        [data-testid="stSidebar"] button[title*="collapse"],
        [data-testid="stSidebar"] button[title*="hide"],
        [data-testid="stSidebar"] button[aria-label*="collapse"],
        [data-testid="stSidebar"] button[aria-label*="hide"],
        .stSidebar button[kind="header"],
        section[data-testid="stSidebar"] > div > button,
        section[data-testid="stSidebar"] button:first-child {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            width: 0 !important;
            height: 0 !important;
        }
        
        /* Ensure sidebar content is always visible */
        [data-testid="stSidebar"] > div {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        
        /* Force sidebar radio buttons to be visible */
        [data-testid="stSidebar"] .stRadio {
            display: block !important;
            visibility: visible !important;
        }
        
        /* Override any CSS that might hide the sidebar */
        [data-testid="stSidebar"] {
            opacity: 1 !important;
            pointer-events: auto !important;
        }
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
        /* Add yellow border to Enter Premium Sold and see Agency Estimated Comm/Revenue (CRM) input */
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
        }        /* Force highlight for all selectboxes labeled 'Transaction Type' everywhere */
        label:has(> div[data-baseweb="select"]) {
            background-color: #fff3b0 !important;
            border-radius: 6px !important;
            padding: 2px 4px !important;
        }
        /* Also target selectbox input and dropdown for 'Transaction Type' */
        [aria-label="Transaction Type"] > div[data-baseweb="select"],
        [aria-label="Transaction Type"] [data-baseweb="select"],
        [aria-label="Transaction Type"] [class*="css-1wa3eu0-placeholder"],
        [aria-label="Transaction Type"] [class*="css-1uccc91-singleValue"],
        [aria-label="Transaction Type"] [class*="css-1okebmr-indicatorSeparator"],
        [aria-label="Transaction Type"] [class*="css-1pahdxg-control"],
        [aria-label="Transaction Type"] [class*="css-1s2u09g-control"],
        [aria-label="Transaction Type"] [class*="css-1n7v3ny-option"],
        [aria-label="Transaction Type"] [class*="css-9gakcf-option"],
        [aria-label="Transaction Type"] [class*="css-1n6sfyn-MenuList"],
        [aria-label="Transaction Type"] [class*="css-1n6sfyn-MenuList"] * {
            background-color: #fff3b0 !important;
            border-color: #e6a800 !important;
            color: #222 !important;
        }
        [aria-label="Transaction Type"] > div[data-baseweb="select"] {
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        [aria-label="Transaction Type"] > div[data-baseweb="select"]:focus,
        [aria-label="Transaction Type"] > div[data-baseweb="select"]:active,
        [aria-label="Transaction Type"] > div[data-baseweb="select"]:focus-visible {
            border: 2px solid #e6a800 !important;
            box-shadow: none !important;
            outline: none !important;
        }
        </style>"""

def apply_css():
    """Apply custom CSS styling to the Streamlit app."""
    with st.container():
        st.markdown(get_custom_css(), unsafe_allow_html=True)

def format_currency(val):
    """Format the value as currency for display."""
    if pd.isna(val) or val is None:
        return ""
    try:
        return f"${val:,.2f}"
    except Exception:
        return val

def format_dates_mmddyyyy(df):
    """Format date columns in MM/DD/YYYY format using mapped column names."""
    date_field_names = ["Policy Origination Date", "Effective Date", "X-Date", "X-DATE", "Statement Date", "STMT DATE"]
    
    for ui_field in date_field_names:
        # Try mapped column first, then fallback to exact match
        mapped_col = get_mapped_column(ui_field)
        target_col = mapped_col if mapped_col and mapped_col in df.columns else ui_field
        
        if target_col in df.columns:
            df[target_col] = pd.to_datetime(df[target_col], errors="coerce")
            df[target_col] = df[target_col].dt.strftime("%m/%d/%Y")
    return df

CURRENCY_COLUMNS = [
    "Premium Sold",    "Agency Comm Received (STMT)",
    "Gross Premium Paid",
    "Agency Gross Comm",
    "Agent Paid Amount (STMT)",
    "Estimated Agent Comm",
    "Policy Balance Due",  # Updated to use the new calculated column
    "Agent Estimated Comm $",
    "Agency Estimated Comm/Revenue (CRM)",
    "Agency Estimated Comm/Revenue (CRM)"
]

def format_currency_columns(df):
    # Use mapped column names for currency formatting
    for ui_field in CURRENCY_COLUMNS:
        mapped_col = get_mapped_column(ui_field)
        if mapped_col and mapped_col in df.columns:
            df[mapped_col] = df[mapped_col].apply(format_currency)
        elif ui_field in df.columns:  # Fallback to original name
            df[ui_field] = df[ui_field].apply(format_currency)
    return df

# --- Helper Functions ---
def generate_client_id(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def generate_transaction_id(length=7):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

# --- Commission calculation function ---
def calculate_commission(row):
    try:
        agency_revenue_col = get_mapped_column("Agency Estimated Comm/Revenue (CRM)")
        revenue = float(row[agency_revenue_col]) if agency_revenue_col and row[agency_revenue_col] is not None else 0.0
    except (ValueError, TypeError, KeyError):
        revenue = 0.0
    
    transaction_type_col = get_mapped_column("Transaction Type")
    policy_orig_col = get_mapped_column("Policy Origination Date") 
    effective_date_col = get_mapped_column("Effective Date")
    
    try:
        transaction_type = row.get(transaction_type_col, "") if transaction_type_col else ""
        if transaction_type in ["NEW", "NBS", "STL", "BoR"]:
            return revenue * 0.50
        elif transaction_type in ["END", "PCH"]:
            policy_orig = row.get(policy_orig_col, "") if policy_orig_col else ""
            effective_date = row.get(effective_date_col, "") if effective_date_col else ""
            return revenue * 0.50 if policy_orig == effective_date else revenue * 0.25
        elif transaction_type in ["RWL", "REWRITE"]:
            return revenue * 0.25
        elif transaction_type in ["CAN", "XCL"]:
            return 0
        else:
            return revenue * 0.25
    except (KeyError, TypeError):
        return revenue * 0.25

def get_pending_renewals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies and generates a DataFrame of policies pending renewal.
    """
    # Filter for relevant transaction types
    renewal_candidates = df[df[get_mapped_column("Transaction Type")].isin(["NEW", "RWL"])].copy()
    
    # Convert date columns to datetime objects
    renewal_candidates['expiration_date'] = pd.to_datetime(renewal_candidates[get_mapped_column("X-DATE")], errors='coerce')
    
    # Sort by policy number and expiration date to find the latest transaction
    renewal_candidates = renewal_candidates.sort_values(by=["Policy Number", "expiration_date"], ascending=[True, False])
    
    # Get the most recent transaction for each policy
    latest_renewals = renewal_candidates.drop_duplicates(subset="Policy Number", keep="first")
    
    # Filter for policies that are expired or expiring soon (e.g., within 60 days)
    today = pd.to_datetime(datetime.date.today())
    pending_renewals = latest_renewals[latest_renewals['expiration_date'] < (today + pd.DateOffset(days=60))]
    
    return pending_renewals

def duplicate_for_renewal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Duplicates the given policies and updates their dates for renewal.
    """
    if df.empty:
        return pd.DataFrame()

    renewed_df = df.copy()
    
    # Calculate new term dates
    renewed_df['new_effective_date'] = renewed_df['expiration_date']
    renewed_df['new_expiration_date'] = renewed_df['new_effective_date'] + pd.DateOffset(months=6) # Assuming 6-month terms for now
    
    # Update the relevant columns
    renewed_df[get_mapped_column("Effective Date")] = renewed_df['new_effective_date'].dt.strftime('%m/%d/%Y')
    renewed_df[get_mapped_column("X-DATE")] = renewed_df['new_expiration_date'].dt.strftime('%m/%d/%Y')
    renewed_df[get_mapped_column("Transaction Type")] = "RWL"
    
    return renewed_df

def main():
    # Apply CSS styling
    apply_css()
      # --- Page Selection ---
    page = st.sidebar.radio(
        "Navigation",        [
            "Dashboard",
            "Reports",
            "All Policies in Database",
            "Edit Policies in Database",
            "Add New Policy Transaction",
            "Search & Filter",
            "Admin Panel",
            "Tools",
            "Accounting",
            "Help",
            "Policy Revenue Ledger",
            "Policy Revenue Ledger Reports",
            "Pending Policy Renewals"
        ]
    )
    
    # --- Load data with caching for better performance ---
    all_data = load_policies_data()
    engine = get_database_engine()
    
    if all_data.empty:
        st.warning("No data found in policies table. Please add some policy data first.")

    # --- Page Navigation ---
    if page == "Dashboard":
        st.title("📊 Commission Dashboard")
        
        if not all_data.empty:
            # --- Dashboard Metrics ---
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_policies = len(all_data)
                st.metric("Total Policies", f"{total_policies:,}")
            
            with col2:
                if 'Commission_Paid' in all_data.columns:
                    total_commission = all_data['Commission_Paid'].sum()
                    st.metric("Total Commission", f"${total_commission:,.2f}")
                else:
                    st.metric("Total Commission", "N/A")
            
            with col3:
                if 'Agency_Commission_Received' in all_data.columns:
                    agency_commission = all_data['Agency_Commission_Received'].sum()
                    st.metric("Agency Commission", f"${agency_commission:,.2f}")
                else:
                    st.metric("Agency Commission", "N/A")
            
            with col4:
                if 'Balance_Due' in all_data.columns:
                    balance_due = all_data['Balance_Due'].sum()
                    st.metric("Balance Due", f"${balance_due:,.2f}")
                else:
                    st.metric("Balance Due", "N/A")
            
            st.divider()
            
            # --- Client Search and Quick Actions ---
            st.subheader("🔍 Quick Client Search")
            
            search_col1, search_col2 = st.columns([3, 1])
            
            with search_col1:
                search_term = st.text_input("Search by Client Name, Policy Number, or Transaction ID", 
                                          placeholder="Enter search term...")
            
            with search_col2:
                st.write("")  # Spacing
                search_button = st.button("Search", type="primary")
            
            # Search functionality
            if search_term or search_button:
                if search_term:
                    # Search across multiple columns
                    mask = pd.Series(False, index=all_data.index)
                    search_columns = ['Customer', 'Policy_Number', 'Transaction_ID', 'Client_ID']
                    
                    for col in search_columns:
                        if col in all_data.columns:
                            mask |= all_data[col].astype(str).str.contains(search_term, case=False, na=False)
                    
                    search_results = all_data[mask]
                    
                    if not search_results.empty:
                        st.success(f"Found {len(search_results)} matching records")
                        
                        # Display search results in an editable table
                        edited_data = st.data_editor(
                            search_results,
                            use_container_width=True,
                            height=400,
                            key="dashboard_search_editor"
                        )
                        
                        # Update button for search results
                        if st.button("Save Changes", key="dashboard_save"):
                            try:
                                # Update the database with changes
                                for idx, row in edited_data.iterrows():
                                    update_query = f"UPDATE policies SET "
                                    update_values = []
                                    for col in edited_data.columns:
                                        if col != 'Transaction_ID':  # Don't update primary key
                                            update_query += f"{col} = ?, "
                                            update_values.append(row[col])
                                    
                                    update_query = update_query.rstrip(', ') + " WHERE Transaction_ID = ?"
                                    update_values.append(row['Transaction_ID'])
                                    
                                    with engine.begin() as conn:
                                        conn.execute(sqlalchemy.text(update_query), update_values)
                                
                                st.success("Changes saved successfully!")
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"Error saving changes: {e}")
                    else:
                        st.warning("No records found matching your search term")
                else:
                    st.info("Enter a search term to find records")
            
            st.divider()
            
            # --- Recent Activity ---
            st.subheader("📈 Recent Activity")
            
            # Show last 10 records
            recent_data = all_data.head(10)
            st.dataframe(
                recent_data,
                use_container_width=True,
                height=300
            )
            
            # --- Quick Statistics ---
            st.subheader("📊 Quick Statistics")
            
            stats_col1, stats_col2 = st.columns(2)
            
            with stats_col1:
                if 'Policy_Type' in all_data.columns:
                    policy_type_counts = all_data['Policy_Type'].value_counts()
                    st.write("**Policies by Type:**")
                    for policy_type, count in policy_type_counts.items():
                        st.write(f"• {policy_type}: {count}")
                        
            with stats_col2:
                if 'Transaction_Type' in all_data.columns:
                    transaction_type_counts = all_data['Transaction_Type'].value_counts()
                    st.write("**Transactions by Type:**")
                    for trans_type, count in transaction_type_counts.items():
                        st.write(f"• {trans_type}: {count}")
            
        else:
            st.info("No data available. Please add some policy data to see dashboard metrics.")
    
    # --- Reports ---
    elif page == "Reports":
        st.title("📈 Reports")
        
        if not all_data.empty:
            tab1, tab2, tab3, tab4 = st.tabs(["Summary Reports", "Commission Analysis", "Policy Reports", "Custom Reports"])
            
            with tab1:
                st.subheader("Summary Reports")
                
                # Overall summary
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Total Policies", len(all_data))
                    if 'Commission_Paid' in all_data.columns:
                        st.metric("Total Commission Paid", f"${all_data['Commission_Paid'].sum():,.2f}")
                    if 'Agency_Commission_Received' in all_data.columns:
                        st.metric("Total Agency Commission", f"${all_data['Agency_Commission_Received'].sum():,.2f}")
                
                with col2:
                    if 'Balance_Due' in all_data.columns:
                        st.metric("Total Balance Due", f"${all_data['Balance_Due'].sum():,.2f}")
                    if 'Effective_Date' in all_data.columns:
                        latest_date = pd.to_datetime(all_data['Effective_Date'], errors='coerce').max()
                        st.metric("Latest Policy Date", latest_date.strftime('%m/%d/%Y') if pd.notnull(latest_date) else "N/A")
            
            with tab2:
                st.subheader("Commission Analysis")
                
                if 'Commission_Paid' in all_data.columns and 'Policy_Type' in all_data.columns:
                    commission_by_type = all_data.groupby('Policy_Type')['Commission_Paid'].sum().sort_values(ascending=False)
                    st.write("**Commission by Policy Type:**")
                    st.dataframe(commission_by_type.reset_index())
                    
                if 'Transaction_Type' in all_data.columns and 'Commission_Paid' in all_data.columns:
                    commission_by_transaction = all_data.groupby('Transaction_Type')['Commission_Paid'].sum().sort_values(ascending=False)
                    st.write("**Commission by Transaction Type:**")
                    st.dataframe(commission_by_transaction.reset_index())
            
            with tab3:
                st.subheader("Policy Reports")
                
                if 'Policy_Type' in all_data.columns:
                    policy_counts = all_data['Policy_Type'].value_counts()
                    st.write("**Policy Count by Type:**")
                    st.dataframe(policy_counts.reset_index())
                
                if 'Transaction_Type' in all_data.columns:
                    transaction_counts = all_data['Transaction_Type'].value_counts()
                    st.write("**Transaction Count by Type:**")
                    st.dataframe(transaction_counts.reset_index())
            
            with tab4:
                st.subheader("Custom Reports")
                st.info("Custom report builder - Select criteria to generate custom reports")
                
                # Date range filter
                if 'Effective_Date' in all_data.columns:
                    date_col = st.columns(2)
                    with date_col[0]:
                        start_date = st.date_input("Start Date")
                    with date_col[1]:
                        end_date = st.date_input("End Date")
                
                # Policy type filter
                if 'Policy_Type' in all_data.columns:
                    policy_types = st.multiselect("Policy Types", all_data['Policy_Type'].unique())
                
                if st.button("Generate Custom Report"):
                    filtered_data = all_data.copy()
                    
                    # Apply filters
                    if 'Effective_Date' in all_data.columns and start_date and end_date:
                        filtered_data['Effective_Date'] = pd.to_datetime(filtered_data['Effective_Date'], errors='coerce')
                        filtered_data = filtered_data[
                            (filtered_data['Effective_Date'] >= pd.Timestamp(start_date)) &
                            (filtered_data['Effective_Date'] <= pd.Timestamp(end_date))
                        ]
                    
                    if policy_types:
                        filtered_data = filtered_data[filtered_data['Policy_Type'].isin(policy_types)]
                    
                    st.write(f"**Custom Report Results ({len(filtered_data)} records):**")
                    st.dataframe(filtered_data, use_container_width=True)
        else:
            st.info("No data available for reports.")
    
    # --- All Policies in Database ---
    elif page == "All Policies in Database":
        st.title("📋 All Policies in Database")
        
        if not all_data.empty:
            st.write(f"**Total Records: {len(all_data)}**")
            
            # Pagination controls
            items_per_page = st.selectbox("Items per page", [25, 50, 100, 200], index=1)
            total_pages = max(1, len(all_data) // items_per_page + (1 if len(all_data) % items_per_page > 0 else 0))
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                page_num = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
            
            # Calculate pagination
            start_idx = (page_num - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, len(all_data))
            
            # Display paginated data
            paginated_data = all_data.iloc[start_idx:end_idx]
            
            st.write(f"Showing records {start_idx + 1} to {end_idx} of {len(all_data)}")
            
            # Display the data in a scrollable table
            st.dataframe(
                paginated_data,
                use_container_width=True,
                height=600
            )
            
            # Export options
            st.subheader("Export Options")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Export Current Page to CSV"):
                    csv = paginated_data.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"policies_page_{page_num}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("Export All Data to CSV"):
                    csv = all_data.to_csv(index=False)
                    st.download_button(
                        label="Download All Data CSV",
                        data=csv,
                        file_name="all_policies.csv",
                        mime="text/csv"
                    )
        else:
            st.info("No policies found in database.")
    
    # --- Edit Policies in Database ---
    elif page == "Edit Policies in Database":
        st.title("✏️ Edit Policies in Database")
        
        if not all_data.empty:
            st.warning("⚠️ Be careful when editing data. Changes are saved directly to the database.")
            
            # Search and filter options
            st.subheader("Find Policies to Edit")
            
            search_col1, search_col2 = st.columns([3, 1])
            
            with search_col1:
                edit_search_term = st.text_input("Search policies to edit", placeholder="Enter search term...")
            
            with search_col2:
                st.write("")  # Spacing
                edit_search_button = st.button("Find Records", type="primary")
            
            # Show filtered data for editing
            if edit_search_term or edit_search_button:
                if edit_search_term:
                    # Search across multiple columns
                    mask = pd.Series(False, index=all_data.index)
                    search_columns = ['Customer', 'Policy_Number', 'Transaction_ID', 'Client_ID']
                    
                    for col in search_columns:
                        if col in all_data.columns:
                            mask |= all_data[col].astype(str).str.contains(edit_search_term, case=False, na=False)
                    
                    edit_results = all_data[mask]
                    
                    if not edit_results.empty:
                        st.success(f"Found {len(edit_results)} records for editing")
                        
                        # Editable data grid
                        edited_data = st.data_editor(
                            edit_results,
                            use_container_width=True,
                            height=500,
                            key="edit_policies_editor",
                            num_rows="dynamic"
                        )
                        
                        # Save changes button
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            if st.button("💾 Save All Changes", type="primary"):
                                try:
                                    # Update each record in the database
                                    for idx, row in edited_data.iterrows():
                                        if 'Transaction_ID' in row:
                                            update_query = "UPDATE policies SET "
                                            update_values = []
                                            
                                            for col in edited_data.columns:
                                                if col != 'Transaction_ID':  # Don't update primary key
                                                    update_query += f"{col} = ?, "
                                                    update_values.append(row[col])
                                            
                                            update_query = update_query.rstrip(', ') + " WHERE Transaction_ID = ?"
                                            update_values.append(row['Transaction_ID'])
                                            
                                            with engine.begin() as conn:
                                                conn.execute(sqlalchemy.text(update_query), update_values)
                                    
                                    st.success(f"Successfully updated {len(edited_data)} records!")
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"Error saving changes: {e}")
                        
                        with col2:
                            if st.button("🔄 Refresh Data"):
                                st.rerun()
                    else:
                        st.warning("No records found matching your search")
                else:
                    st.info("Enter a search term to find records to edit")
            else:
                st.info("Use the search box above to find policies to edit, or edit all policies below:")
                
                # Option to edit all data (with pagination for performance)
                if st.checkbox("Show all policies for editing (use with caution)"):
                    st.warning("Editing all policies at once can be slow with large datasets")
                    
                    # Limit to first 50 records for performance
                    edit_all_data = all_data.head(50)
                    st.write(f"Showing first 50 records for editing out of {len(all_data)} total")
                    
                    edited_all_data = st.data_editor(
                        edit_all_data,
                        use_container_width=True,
                        height=500,
                        key="edit_all_policies_editor"
                    )
                    
                    if st.button("💾 Save Changes", key="save_all_edits"):
                        try:
                            for idx, row in edited_all_data.iterrows():
                                if 'Transaction_ID' in row:
                                    update_query = "UPDATE policies SET "
                                    update_values = []
                                    
                                    for col in edited_all_data.columns:
                                        if col != 'Transaction_ID':
                                            update_query += f"{col} = ?, "
                                            update_values.append(row[col])
                                    
                                    update_query = update_query.rstrip(', ') + " WHERE Transaction_ID = ?"
                                    update_values.append(row['Transaction_ID'])
                                    
                                    with engine.begin() as conn:
                                        conn.execute(sqlalchemy.text(update_query), update_values)
                            
                            st.success("All changes saved successfully!")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Error saving changes: {e}")
        else:
            st.info("No policies available to edit.")
    
    # --- Add New Policy Transaction ---
    elif page == "Add New Policy Transaction":
        st.title("➕ Add New Policy Transaction")
        
        with st.form("add_policy_form"):
            st.subheader("Policy Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                client_id = st.text_input("Client ID", value=generate_client_id())
                transaction_id = st.text_input("Transaction ID", value=generate_transaction_id())
                customer = st.text_input("Customer Name", placeholder="Enter customer name")
                policy_number = st.text_input("Policy Number", placeholder="Enter policy number")
                policy_type = st.selectbox("Policy Type", ["Auto", "Home", "Life", "Health", "Commercial", "Other"])
            
            with col2:
                effective_date = st.date_input("Effective Date", value=datetime.date.today())
                transaction_type = st.selectbox("Transaction Type", ["New Business", "Renewal", "Endorsement", "Cancellation", "Reinstatement"])
                commission_paid = st.number_input("Commission Paid", value=0.0, format="%.2f")
                agency_commission_received = st.number_input("Agency Commission Received", value=0.0, format="%.2f")
            
            st.subheader("Additional Information")
            
            col3, col4 = st.columns(2)
            
            with col3:
                premium = st.number_input("Premium", value=0.0, format="%.2f")
                commission_rate = st.number_input("Commission Rate (%)", value=0.0, format="%.2f", min_value=0.0, max_value=100.0)
            
            with col4:
                balance_due = st.number_input("Balance Due", value=0.0, format="%.2f")
                notes = st.text_area("Notes", placeholder="Any additional notes...")
            
            # Submit button
            submitted = st.form_submit_button("Add Policy Transaction", type="primary")
            
            if submitted:
                if customer and policy_number:
                    try:
                        # Insert new record into database
                        insert_query = """
                        INSERT INTO policies (
                            Client_ID, Transaction_ID, Customer, Policy_Number, Policy_Type,
                            Effective_Date, Transaction_Type, Commission_Paid, Agency_Commission_Received,
                            Premium, Commission_Rate, Balance_Due, Notes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """
                        
                        with engine.begin() as conn:
                            conn.execute(sqlalchemy.text(insert_query), [
                                client_id, transaction_id, customer, policy_number, policy_type,
                                effective_date.strftime('%m/%d/%Y'), transaction_type, commission_paid,
                                agency_commission_received, premium, commission_rate, balance_due, notes
                            ])
                        
                        st.success(f"✅ Successfully added new policy transaction for {customer}")
                        st.balloons()
                        
                        # Option to add another
                        if st.button("Add Another Policy"):
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"Error adding policy: {e}")
                else:
                    st.error("Please fill in at least Customer Name and Policy Number")
    
    # --- Search & Filter ---
    elif page == "Search & Filter":
        st.title("🔍 Advanced Search & Filter")
        
        if not all_data.empty:
            st.subheader("Search Criteria")
            
            # Create filter form
            with st.form("advanced_search_form"):
                search_col1, search_col2 = st.columns(2)
                
                with search_col1:
                    # Text search fields
                    customer_search = st.text_input("Customer Name Contains")
                    policy_number_search = st.text_input("Policy Number Contains")
                    client_id_search = st.text_input("Client ID Contains")
                    transaction_id_search = st.text_input("Transaction ID Contains")
                
                with search_col2:
                    # Dropdown filters
                    if 'Policy_Type' in all_data.columns:
                        policy_type_filter = st.multiselect("Policy Type", all_data['Policy_Type'].unique())
                    
                    if 'Transaction_Type' in all_data.columns:
                        transaction_type_filter = st.multiselect("Transaction Type", all_data['Transaction_Type'].unique())
                    
                    # Date range
                    if 'Effective_Date' in all_data.columns:
                        date_from = st.date_input("Effective Date From", value=None)
                        date_to = st.date_input("Effective Date To", value=None)
                
                # Numeric filters
                st.subheader("Numeric Filters")
                numeric_col1, numeric_col2 = st.columns(2)
                
                with numeric_col1:
                    if 'Commission_Paid' in all_data.columns:
                        commission_min = st.number_input("Min Commission Paid", value=0.0, format="%.2f")
                        commission_max = st.number_input("Max Commission Paid", value=float(all_data['Commission_Paid'].max() if all_data['Commission_Paid'].max() > 0 else 999999), format="%.2f")
                
                with numeric_col2:
                    if 'Balance_Due' in all_data.columns:
                        balance_min = st.number_input("Min Balance Due", value=0.0, format="%.2f")
                        balance_max = st.number_input("Max Balance Due", value=float(all_data['Balance_Due'].max() if all_data['Balance_Due'].max() > 0 else 999999), format="%.2f")
                
                # Submit search
                search_submitted = st.form_submit_button("🔍 Apply Filters", type="primary")
            
            # Reset filters button
            if st.button("🔄 Clear All Filters"):
                st.rerun()
            
            # Apply filters and show results
            if search_submitted or any([customer_search, policy_number_search, client_id_search, transaction_id_search]):
                filtered_data = all_data.copy()
                
                # Apply text filters
                if customer_search:
                    filtered_data = filtered_data[filtered_data['Customer'].str.contains(customer_search, case=False, na=False)]
                
                if policy_number_search:
                    filtered_data = filtered_data[filtered_data['Policy_Number'].str.contains(policy_number_search, case=False, na=False)]
                
                if client_id_search:
                    filtered_data = filtered_data[filtered_data['Client_ID'].str.contains(client_id_search, case=False, na=False)]
                
                if transaction_id_search:
                    filtered_data = filtered_data[filtered_data['Transaction_ID'].str.contains(transaction_id_search, case=False, na=False)]
                
                # Apply dropdown filters
                if 'Policy_Type' in all_data.columns and policy_type_filter:
                    filtered_data = filtered_data[filtered_data['Policy_Type'].isin(policy_type_filter)]
                
                if 'Transaction_Type' in all_data.columns and transaction_type_filter:
                    filtered_data = filtered_data[filtered_data['Transaction_Type'].isin(transaction_type_filter)]
                
                # Apply date filters
                if 'Effective_Date' in all_data.columns and (date_from or date_to):
                    filtered_data['Effective_Date'] = pd.to_datetime(filtered_data['Effective_Date'], errors='coerce')
                    
                    if date_from:
                        filtered_data = filtered_data[filtered_data['Effective_Date'] >= pd.Timestamp(date_from)]
                    
                    if date_to:
                        filtered_data = filtered_data[filtered_data['Effective_Date'] <= pd.Timestamp(date_to)]
                
                # Apply numeric filters
                if 'Commission_Paid' in all_data.columns:
                    filtered_data = filtered_data[
                        (filtered_data['Commission_Paid'] >= commission_min) &
                        (filtered_data['Commission_Paid'] <= commission_max)
                    ]
                
                if 'Balance_Due' in all_data.columns:
                    filtered_data = filtered_data[
                        (filtered_data['Balance_Due'] >= balance_min) &
                        (filtered_data['Balance_Due'] <= balance_max)
                    ]
                
                # Show results
                st.subheader(f"Search Results ({len(filtered_data)} records found)")
                
                if not filtered_data.empty:
                    # Display filtered data
                    st.dataframe(
                        filtered_data,
                        use_container_width=True,
                        height=500
                    )
                    
                    # Export filtered results
                    csv = filtered_data.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Filtered Results as CSV",
                        data=csv,
                        file_name="filtered_policies.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No records match your search criteria")
            else:
                st.info("Use the form above to search and filter policies")
        else:
            st.info("No data available to search.")
    
    # --- Admin Panel ---
    elif page == "Admin Panel":
        st.title("⚙️ Admin Panel")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Database Info", "Column Mapping", "Data Management", "System Tools"])
        
        with tab1:
            st.subheader("Database Information")
            
            # Database stats
            if not all_data.empty:
                st.metric("Total Records", len(all_data))
                st.metric("Total Columns", len(all_data.columns))
                
                st.subheader("Column Information")
                col_info = pd.DataFrame({
                    'Column': all_data.columns,
                    'Data Type': [str(all_data[col].dtype) for col in all_data.columns],
                    'Non-Null Count': [all_data[col].count() for col in all_data.columns],
                    'Null Count': [all_data[col].isnull().sum() for col in all_data.columns]
                })
                st.dataframe(col_info, use_container_width=True)
                
                st.subheader("Sample Data")
                st.dataframe(all_data.head(), use_container_width=True)
            else:
                st.info("No data available")
        
        with tab2:
            st.subheader("Column Mapping Configuration")
            st.info("Column mapping settings are managed in column_mapping_config.py")
            
            if not all_data.empty:
                st.write("**Current Database Columns:**")
                for col in sorted(all_data.columns):
                    st.write(f"• {col}")
        
        with tab3:
            st.subheader("Data Management")
            
            st.warning("⚠️ These operations affect your database. Use with caution!")
            
            # Database backup
            if st.button("📁 Create Database Backup"):
                try:
                    import shutil
                    backup_name = f"commissions_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                    shutil.copy2("commissions.db", backup_name)
                    st.success(f"Database backed up as {backup_name}")
                except Exception as e:
                    st.error(f"Backup failed: {e}")
            
            # Data validation
            if st.button("🔍 Validate Data Integrity"):
                if not all_data.empty:
                    issues = []
                    
                    # Check for duplicates
                    if 'Transaction_ID' in all_data.columns:
                        duplicates = all_data['Transaction_ID'].duplicated().sum()
                        if duplicates > 0:
                            issues.append(f"Found {duplicates} duplicate Transaction IDs")
                    
                    # Check for missing critical data
                    if 'Customer' in all_data.columns:
                        missing_customers = all_data['Customer'].isnull().sum()
                        if missing_customers > 0:
                            issues.append(f"Found {missing_customers} records with missing customer names")
                    
                    if issues:
                        st.warning("Data integrity issues found:")
                        for issue in issues:
                            st.write(f"• {issue}")
                    else:
                        st.success("No data integrity issues found!")
                else:
                    st.info("No data to validate")
        
        with tab4:
            st.subheader("System Tools")
            
            # System information
            st.write("**System Information:**")
            st.write(f"• Python version: {pd.__version__}")
            st.write(f"• Pandas version: {pd.__version__}")
            st.write(f"• SQLAlchemy version: {sqlalchemy.__version__}")
            
            # Clear session state
            if st.button("🔄 Clear Session State"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success("Session state cleared!")
                st.rerun()
    
    # --- Tools ---
    elif page == "Tools":
        st.title("🛠️ Tools")
        
        tab1, tab2, tab3 = st.tabs(["Data Tools", "Utility Functions", "Import/Export"])
        
        with tab1:
            st.subheader("Data Tools")
            
            # Commission calculator
            st.write("**Commission Calculator**")
            calc_col1, calc_col2 = st.columns(2)
            
            with calc_col1:
                premium_amount = st.number_input("Premium Amount", value=0.0, format="%.2f")
                commission_rate = st.number_input("Commission Rate (%)", value=10.0, format="%.2f")
            
            with calc_col2:
                calculated_commission = premium_amount * (commission_rate / 100)
                st.metric("Calculated Commission", f"${calculated_commission:.2f}")
            
            st.divider()
            
            # ID Generators
            st.write("**ID Generators**")
            gen_col1, gen_col2 = st.columns(2)
            
            with gen_col1:
                if st.button("Generate Client ID"):
                    new_client_id = generate_client_id()
                    st.code(new_client_id)
            
            with gen_col2:
                if st.button("Generate Transaction ID"):
                    new_transaction_id = generate_transaction_id()
                    st.code(new_transaction_id)
        
        with tab2:
            st.subheader("Utility Functions")
            
            # Currency formatter
            st.write("**Currency Formatter**")
            currency_input = st.number_input("Amount to format", value=1234.56, format="%.2f")
            formatted_currency = format_currency(currency_input)
            st.write(f"Formatted: {formatted_currency}")
            
            st.divider()
            
            # Date formatter
            st.write("**Date Formatter**")
            date_input = st.date_input("Date to format")
            formatted_date = date_input.strftime('%m/%d/%Y')
            st.write(f"Formatted (MM/DD/YYYY): {formatted_date}")
        
        with tab3:
            st.subheader("Import/Export Tools")
            
            # CSV export of all data
            if not all_data.empty:
                csv_data = all_data.to_csv(index=False)
                st.download_button(
                    label="📥 Export All Data to CSV",
                    data=csv_data,
                    file_name=f"all_policies_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            st.divider()
            
            # CSV import
            st.write("**Import CSV Data**")
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            
            if uploaded_file is not None:
                try:
                    import_df = pd.read_csv(uploaded_file)
                    st.write("**Preview of uploaded data:**")
                    st.dataframe(import_df.head(), use_container_width=True)
                    
                    if st.button("Import Data to Database"):
                        # This would need additional validation and mapping logic
                        st.warning("Import functionality requires additional setup for column mapping and validation")
                except Exception as e:
                    st.error(f"Error reading CSV file: {e}")
    
    # --- Accounting ---
    elif page == "Accounting":
        st.subheader("Accounting")
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
        # --- Ensure manual_commission_entries table exists with client_id and transaction_id ---
        with engine.begin() as conn:
            pragma = conn.execute(sqlalchemy.text('PRAGMA table_info(manual_commission_entries)')).fetchall()
            existing_cols = [row[1] for row in pragma]
            if not pragma:
                # Table does not exist, create with new schema
                conn.execute(sqlalchemy.text('''
                    CREATE TABLE IF NOT EXISTS manual_commission_entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_id TEXT,
                        transaction_id TEXT,
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
            else:
                # Table exists, add columns if missing
                if "client_id" not in existing_cols:
                    try:
                        conn.execute(sqlalchemy.text('ALTER TABLE manual_commission_entries ADD COLUMN client_id TEXT'))
                    except Exception:
                        pass
                if "transaction_id" not in existing_cols:
                    try:
                        conn.execute(sqlalchemy.text('ALTER TABLE manual_commission_entries ADD COLUMN transaction_id TEXT'))
                    except Exception:
                        pass
        # --- Ensure statement_details column exists in commission_payments ---
        with engine.begin() as conn:
            try:
                conn.execute(sqlalchemy.text('ALTER TABLE commission_payments ADD COLUMN statement_details TEXT'))
            except Exception:
                pass  # Ignore if already exists

        # --- Ensure renewal_history table exists ---
        with engine.begin() as conn:
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS renewal_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    renewal_timestamp TEXT,
                    renewed_by TEXT,
                    original_transaction_id TEXT,
                    new_transaction_id TEXT,
                    details TEXT
                )
            '''))        # --- Load manual entries from DB if session state is empty ---
        if "manual_commission_rows" not in st.session_state:
            st.session_state["manual_commission_rows"] = []
            
        # Only reload from DB if session state is completely empty (not after deletions)
        if not st.session_state["manual_commission_rows"] and "deletion_performed" not in st.session_state:
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
                        "Agency Comm Received (STMT)": row["agency_commission_received"],
                        "Statement Date": row["statement_date"],
                        "Client ID": row.get("client_id", ""),
                        "Transaction ID": row.get("transaction_id", "")
                    }
                    for _, row in manual_entries_df.iterrows()
                ]

        # --- Accounting UI code continues here ---
        st.markdown("## Reconcile Commission Statement")
        entry_mode = st.radio("How would you like to enter your commission statement?", ["Manual Entry", "Upload File"], key="reconcile_entry_mode")
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
            if "manual_commission_rows" not in st.session_state:
                st.session_state["manual_commission_rows"] = []
            customers = sorted(all_data["Customer"].dropna().unique().tolist())
            selected_customer = st.selectbox("Select Customer", ["Select..."] + customers, key="recon_customer_select")
            # Initialize variables for policy selections
            policy_types = []
            policy_numbers = []
            effective_dates = []
            selected_policy_type = None
            selected_policy_number = None
            selected_effective_date = None
            client_id = None
            
            if selected_customer and selected_customer != "Select...":
                policy_types = sorted(all_data[all_data["Customer"] == selected_customer]["Policy Type"].dropna().unique().tolist())
                selected_policy_type = st.selectbox("Select Policy Type", ["Select..."] + policy_types, key="recon_policy_type_select")
                if selected_policy_type and selected_policy_type != "Select...":
                    policy_numbers = sorted(all_data[(all_data["Customer"] == selected_customer) & (all_data["Policy Type"] == selected_policy_type)]["Policy Number"].dropna().unique().tolist())
                    selected_policy_number = st.selectbox("Select Policy Number", ["Select..."] + policy_numbers, key="recon_policy_number_select")
                    if selected_policy_number and selected_policy_number != "Select...":
                        effective_dates = sorted(all_data[(all_data["Customer"] == selected_customer) & (all_data["Policy Type"] == selected_policy_type) & (all_data["Policy Number"] == selected_policy_number)]["Effective Date"].dropna().unique().tolist())
                        selected_effective_date = st.selectbox("Select Effective Date", ["Select..."] + effective_dates, key="recon_effective_date_select")
                        
                        # Lookup Client ID using exact match of all selected fields
                        if selected_effective_date and selected_effective_date != "Select...":
                            exact_match = all_data[
                                (all_data["Customer"] == selected_customer) &
                                (all_data["Policy Type"] == selected_policy_type) &
                                (all_data["Policy Number"] == selected_policy_number) &
                                (all_data["Effective Date"] == selected_effective_date)
                            ]
                            if not exact_match.empty and "Client ID" in exact_match.columns:
                                client_id = exact_match.iloc[0]["Client ID"]
                                st.success(f"✅ Client ID found: {client_id}")
                            else:
                                st.warning("⚠️ Client ID not found for this exact combination")
            transaction_types = ["NEW", "NBS", "STL", "BoR", "END", "PCH", "RWL", "REWRITE", "CAN", "XCL"]
            transaction_type = st.selectbox("Transaction Type", transaction_types, key="recon_transaction_type_select")
            # Auto-calculate Agent Comm (New 50% RWL 25%) based on Transaction Type
            def calc_agent_comm_pct(tx_type):
                if tx_type == "NEW":
                    return 50.0
                elif tx_type in ["RWL", "RENEWAL"]:
                    return 25.0
                else:
                    return 0.0
            agent_comm_new_rwl = calc_agent_comm_pct(transaction_type)
            # --- Enter statement date ONCE for all entries in this session ---
            if "recon_stmt_date" not in st.session_state:
                st.session_state["recon_stmt_date"] = None
            st.session_state["recon_stmt_date"] = st.date_input(
                "Commission Statement Date (applies to all entries below)",
                value=st.session_state["recon_stmt_date"] or None,
                format="MM/DD/YYYY",
                key="recon_stmt_date_input_global"
            )
            statement_date = st.session_state["recon_stmt_date"]
            agency_comm_received = st.number_input("Agency Comm Received (STMT)", min_value=0.0, step=0.01, format="%.2f", key="recon_agency_comm_received_input")
            amount_paid = st.number_input("Agent Paid Amount (STMT)", min_value=0.0, step=0.01, format="%.2f", key="recon_amount_paid_input")
            if st.button("Add Entry", key="recon_add_entry_btn"):
                # Use the same transaction ID rules as new policy transaction: 7 chars, uppercase letters and digits
                transaction_id = generate_transaction_id()  # 7 chars, uppercase letters and digits
                # Use the global statement date for all entries
                stmt_date_str = ""
                if statement_date is None or statement_date == "":
                    stmt_date_str = ""
                elif isinstance(statement_date, datetime.date):
                    stmt_date_str = statement_date.strftime("%m/%d/%Y")
                else:
                    try:
                        stmt_date_str = pd.to_datetime(statement_date).strftime("%m/%d/%Y")
                    except Exception:
                        stmt_date_str = ""
                entry = {
                    "Client ID": client_id if client_id else "",
                    "Transaction ID": transaction_id,
                    "Customer": selected_customer,
                    "Policy Type": selected_policy_type if selected_policy_type else "",
                    "Policy Number": selected_policy_number if selected_policy_number else "",
                    "Effective Date": selected_effective_date if selected_effective_date else "",
                    "Transaction Type": transaction_type,
                    "Agent Comm (New 50% RWL 25%)": agent_comm_new_rwl,
                    "Agency Comm Received (STMT)": agency_comm_received,
                    "Amount Paid": amount_paid,
                    "Statement Date": stmt_date_str
                }
                # Insert new row into DB (non-destructive, always insert)
                with engine.begin() as conn:
                    conn.execute(sqlalchemy.text('''
                        INSERT INTO manual_commission_entries (
                            client_id, transaction_id, customer, policy_type, policy_number, effective_date, transaction_type, commission_paid, agency_commission_received, statement_date
                        ) VALUES (:client_id, :transaction_id, :customer, :policy_type, :policy_number, :effective_date, :transaction_type, :commission_paid, :agency_commission_received, :statement_date)
                    '''), {
                        "client_id": client_id if client_id else "",
                        "transaction_id": transaction_id,
                        "customer": selected_customer,
                        "policy_type": selected_policy_type if selected_policy_type else "",
                        "policy_number": selected_policy_number if selected_policy_number else "",
                        "effective_date": selected_effective_date if selected_effective_date else "",
                        "transaction_type": transaction_type,
                        "commission_paid": amount_paid,
                        "agency_commission_received": agency_comm_received,
                        "statement_date": stmt_date_str
                    })
                st.session_state["manual_commission_rows"].append(entry)
                st.success("Entry added (non-destructive, unique 7-character Transaction ID). You can review and edit below.")        # Show manual entries for editing/management if any exist        if st.session_state.get("manual_commission_rows"):
            st.markdown("### Manual Commission Entries")
              # Show persistent deletion success message
            if "deletion_success_msg" in st.session_state:
                st.success(st.session_state["deletion_success_msg"])
                del st.session_state["deletion_success_msg"]  # Clear after showing
            
            st.info("Manual entries are non-destructive and saved to database. Use controls below to manage entries.")
              # Display summary of entries
            total_entries = len(st.session_state["manual_commission_rows"])
            total_paid = sum(float(row.get("Commission Paid", 0) or row.get("Amount Paid", 0)) for row in st.session_state["manual_commission_rows"])
            total_received = sum(float(row.get("Agency Comm Received (STMT)", 0)) for row in st.session_state["manual_commission_rows"])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Entries", total_entries)
            with col2:
                st.metric("Total Agent Comm Paid", f"${total_paid:,.2f}")
            with col3:
                st.metric("Total Agency Comm", f"${total_received:,.2f}")
            
            # Show entries in an editable table with selection capability
            df_display = pd.DataFrame(st.session_state["manual_commission_rows"])
            df_display.insert(0, "Select", False)  # Add selection column at the beginning
            
            edited_df = st.data_editor(
                df_display, 
                use_container_width=True, 
                height=max(400, 40 + 40 * len(df_display)),
                column_config={
                    "Select": st.column_config.CheckboxColumn("Select", help="Check to select rows for deletion")
                },
                disabled=[col for col in df_display.columns if col != "Select"],  # Only allow editing the Select column
                key="manual_entries_editor"            )
            
            # Delete selected rows functionality
            selected_indices = edited_df[edited_df["Select"] == True].index.tolist()
            if selected_indices:
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("🗑️ Delete Selected", type="secondary", key="delete_selected_entries"):
                        # Remove selected entries from session state
                        original_count = len(st.session_state["manual_commission_rows"])
                          # Get the transaction IDs of rows to delete BEFORE removing from session state
                        transaction_ids_to_delete = []
                        for idx in selected_indices:
                            if idx < len(st.session_state["manual_commission_rows"]):
                                entry = st.session_state["manual_commission_rows"][idx]
                                transaction_id = entry.get("Transaction ID", "")
                                transaction_ids_to_delete.append(transaction_id)
                        
                        # Remove from session state
                        st.session_state["manual_commission_rows"] = [
                            entry for i, entry in enumerate(st.session_state["manual_commission_rows"]) 
                            if i not in selected_indices
                        ]
                        deleted_count = original_count - len(st.session_state["manual_commission_rows"])
                          # Delete from database using the collected transaction IDs
                        db_deleted_count = 0
                        failed_deletions = []
                        for transaction_id in transaction_ids_to_delete:
                            if transaction_id and transaction_id.strip():  # Only if transaction_id is not empty
                                try:
                                    with engine.begin() as conn:
                                        result = conn.execute(
                                            sqlalchemy.text("DELETE FROM manual_commission_entries WHERE transaction_id = :tid"),
                                            {"tid": transaction_id}
                                        )
                                        if result.rowcount > 0:
                                            db_deleted_count += 1
                                        else:
                                            failed_deletions.append(f"No DB row found for ID: {transaction_id}")
                                except Exception as e:
                                    failed_deletions.append(f"Error deleting {transaction_id}: {str(e)}")
                            else:
                                failed_deletions.append("Empty transaction ID")
                         # Get mapped column names
                        customer_col = get_mapped_column("Customer")
                        policy_type_col = get_mapped_column("Policy Type")
                        policy_number_col = get_mapped_column("Policy Number")
                        effective_date_col = get_mapped_column("Effective Date")
                        transaction_type_col = get_mapped_column("Transaction Type")
                        agent_paid_col = get_mapped_column("Agent Paid Amount (STMT)")
                        agency_comm_col = get_mapped_column("Agency Comm Received (STMT)")
                        client_id_col = get_mapped_column("Client ID")
                        transaction_id_col = get_mapped_column("Transaction ID")
                        
                       
                        # Set flag to prevent automatic reload from database
                        st.session_state["deletion_performed"] = True
                          # Create success message
                        success_msg = f"Deleted {deleted_count} entries from session and {db_deleted_count} from database."
                        if failed_deletions:
                            success_msg += f" Issues: {'; '.join(failed_deletions[:3])}"  # Show first 3 issues
                        elif db_deleted_count == 0 and transaction_ids_to_delete:
                            success_msg += f" (Transaction IDs attempted: {transaction_ids_to_delete})"
                        
                        st.session_state["deletion_success_msg"] = success_msg
                        st.rerun()
                with col2:
                    st.info(f"📋 {len(selected_indices)} row(s) selected for deletion")
            else:
                st.info("💡 Tip: Check the 'Select' boxes next to entries you want to delete, then click the delete button.")
              # --- Reconcile Button to Save Statement to History ---
            st.markdown("---")
            if st.session_state["manual_commission_rows"]:
                st.markdown("#### Reconcile Commission Statement")
                col1, col2 = st.columns([2, 3])
                with col1:
                    statement_date = st.date_input(
                        "Statement Date",
                        value=datetime.date.today(),
                        format="MM/DD/YYYY",
                        key="reconcile_statement_date_v2"
                    )
                with col2:
                    statement_description = st.text_input(
                        "Statement Description (optional)",
                        placeholder="e.g., Monthly Commission Statement - December 2024",
                        key="reconcile_description"                    )
                  # Calculate totals for the statement
                total_commission_paid = sum(float(row.get("Commission Paid", 0) or row.get("Amount Paid", 0)) for row in st.session_state["manual_commission_rows"])
                total_agency_received = sum(float(row.get("Agency Comm Received (STMT)", 0)) for row in st.session_state["manual_commission_rows"])
                
                st.markdown(f"**Statement Summary:** {len(st.session_state['manual_commission_rows'])} entries | Amount Paid: ${total_commission_paid:,.2f} | Agency Received: ${total_agency_received:,.2f}")
                
                if st.button("💾 Reconcile & Save to History", type="primary", key="reconcile_statement_btn"):
                    try:
                        # Prepare statement details for JSON storage
                        statement_details = []
                        for row in st.session_state["manual_commission_rows"]:
                            statement_details.append({
                                "Customer": row.get("Customer", ""),
                                "Policy Type": row.get("Policy Type", ""),
                                "Policy Number": row.get("Policy Number", ""),
                                "Effective Date": row.get("Effective Date", ""),
                                "Transaction Type": row.get("Transaction Type", ""),
                                "Commission Paid": row.get("Amount Paid", 0),
                                "Agency Comm Received (STMT)": row.get("Agency Comm Received (STMT)", 0),
                                "Client ID": row.get("Client ID", ""),
                                "Transaction ID": row.get("Transaction ID", "")
                            })
                        
                        # PHASE 1: Existing audit/history functionality (preserved exactly)
                        # Save to commission_history table
                        with engine.begin() as conn:
                            conn.execute(sqlalchemy.text('''
                                INSERT INTO commission_history (statement_id, description, total_commission_paid, total_agency_received, statement_date, payment_timestamp, statement_details)
                                VALUES (:statement_id, :description, :total_commission_paid, :total_agency_received, :statement_date, :payment_timestamp, :statement_details)
                            '''), {
                                "statement_id": f"STMT-{uuid.uuid4().hex[:8].upper()}",
                                "description": statement_description,
                                "total_commission_paid": total_commission_paid,
                                "total_agency_received": total_agency_received,
                                "statement_date": statement_date.strftime('%Y-%m-%d'),
                                "payment_timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                "statement_details": json.dumps(statement_details)
                            })
                        
                        # Save individual entries to manual_commission_entries table as well
                        for row in st.session_state["manual_commission_rows"]:
                            with engine.begin() as conn:
                                conn.execute(sqlalchemy.text('''
                                    INSERT OR REPLACE INTO manual_commission_entries 
                                    (client_id, transaction_id, customer, policy_type, policy_number, effective_date, transaction_type, commission_paid, agency_commission_received, statement_date)
                                    VALUES (:client_id, :transaction_id, :customer, :policy_type, :policy_number, :effective_date, :transaction_type, :commission_paid, :agency_commission_received, :statement_date)
                                '''), {
                                    "client_id": row.get("Client ID", ""),
                                    "transaction_id": row.get("Transaction ID", ""),
                                    "customer": row.get("Customer", ""),
                                    "policy_type": row.get("Policy Type", ""),
                                    "policy_number": row.get("Policy Number", ""),
                                    "effective_date": row.get("Effective Date", ""),
                                    "transaction_type": row.get("Transaction Type", ""),
                                    "commission_paid": float(row.get("Amount Paid", 0)),
                                    "agency_commission_received": float(row.get("Agency Comm Received (STMT)", 0)),
                                    "statement_date": statement_date.strftime('%Y-%m-%d')
                                })
                        
                        # PHASE 2: NEW - Add reconciled transactions to main policies database
                        new_main_db_transactions = []
                        for row in st.session_state["manual_commission_rows"]:
                            # Create new transaction record for main policies table using centralized mapping
                            new_transaction = {}
                            
                            # Use centralized mapping to ensure field consistency                            transaction_id_col = get_mapped_column("Transaction ID")
                            customer_col = get_mapped_column("Customer")
                            policy_type_col = get_mapped_column("Policy Type") 
                            policy_number_col = get_mapped_column("Policy Number")
                            effective_date_col = get_mapped_column("Effective Date")
                            transaction_type_col = get_mapped_column("Transaction Type")
                            stmt_date_col = get_mapped_column("STMT DATE")
                            agency_comm_col = get_mapped_column("Agency Comm Received (STMT)")
                            agent_paid_col = get_mapped_column("Agent Paid Amount (STMT)")
                            client_id_col = get_mapped_column("Client ID")
                            
                            # Populate with reconciliation data using flexible transaction types
                            if transaction_id_col:                                # Generate new unique transaction ID for main DB to avoid conflicts
                                new_transaction[transaction_id_col] = generate_transaction_id()
                            if customer_col:
                                new_transaction[customer_col] = row.get("Customer", "")
                            if policy_type_col:
                                new_transaction[policy_type_col] = row.get("Policy Type", "")
                            if policy_number_col:
                                new_transaction[policy_number_col] = row.get("Policy Number", "")
                            if effective_date_col:
                                new_transaction[effective_date_col] = row.get("Effective Date", "")
                            if transaction_type_col:
                                # PRESERVE USER'S TRANSACTION TYPE FLEXIBILITY - use exactly what they entered
                                new_transaction[transaction_type_col] = row.get("Transaction Type", "")
                            if stmt_date_col:
                                new_transaction[stmt_date_col] = statement_date.strftime('%m/%d/%Y')
                            if agency_comm_col:
                                new_transaction[agency_comm_col] = float(row.get("Agency Comm Received (STMT)", 0))
                            if agent_paid_col:
                                new_transaction[agent_paid_col] = float(row.get("Amount Paid", 0))
                            if client_id_col:
                                new_transaction[client_id_col] = row.get("Client ID", "")
                            
                            # Add description field to identify reconciled transactions
                            description_col = get_mapped_column("Description")
                            if description_col:
                                new_transaction[description_col] = f"Reconciled Statement - {statement_date.strftime('%m/%d/%Y')}"
                            
                            new_main_db_transactions.append(new_transaction)
                        
                        # Insert new transactions into main policies table
                        main_db_added_count = 0
                        if new_main_db_transactions:
                            try:
                                new_df = pd.DataFrame(new_main_db_transactions)
                                new_df.to_sql("policies", engine, if_exists="append", index=False)
                                main_db_added_count = len(new_main_db_transactions)
                            except Exception as e:
                                st.warning(f"⚠️ Reconciliation saved to history, but could not add to main database: {str(e)}")
                        
                        # Clear the manual entries after successful reconciliation
                        st.session_state["manual_commission_rows"] = []
                        
                        # Enhanced success message showing both operations
                        success_msg = f"✅ Commission statement reconciled and saved to history! Statement date: {statement_date.strftime('%m/%d/%Y')}"
                        if main_db_added_count > 0:
                            success_msg += f"\n💾 Added {main_db_added_count} new transactions to main policies database"
                            success_msg += f"\n🔍 View in 'All Policies in Database' or 'Policy Revenue Ledger' pages"
                        st.success(success_msg)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error saving commission statement: {str(e)}")
            else:
                st.info("ℹ️ Add manual commission entries above to reconcile a statement.")

        # --- Payment/Reconciliation History Viewer ---
        st.markdown("---")
        st.markdown("### Payment/Reconciliation History")
        payment_history = pd.read_sql('SELECT * FROM commission_payments ORDER BY payment_timestamp DESC', engine)
        if not payment_history.empty:
            payment_history["statement_date"] = pd.to_datetime(payment_history["statement_date"], errors="coerce").dt.strftime("%m/%d/%Y").fillna("")
            payment_history["payment_timestamp"] = pd.to_datetime(payment_history["payment_timestamp"], errors="coerce").dt.strftime("%m/%d/%Y %I:%M %p").fillna("")

            for idx, row in payment_history.iterrows():
                col1, col2 = st.columns([0.9, 0.1])
                with col1:
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
                with col2:
                    if 'id' in row and pd.notna(row['id']):
                        if st.button("Delete", key=f"delete_history_{row['id']}"):
                            st.session_state['pending_delete_history_id'] = row['id']
                            st.rerun()
                    else:
                        st.warning("Cannot delete row without a valid ID.")
        
        if 'pending_delete_history_id' in st.session_state:
            st.warning(f"Are you sure you want to delete this history record? This cannot be undone.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Confirm Delete", key="confirm_delete_history"):
                    with engine.begin() as conn:
                        conn.execute(sqlalchemy.text("DELETE FROM commission_payments WHERE id = :id"), {"id": st.session_state['pending_delete_history_id']})
                    st.success("History record deleted.")
                    del st.session_state['pending_delete_history_id']
                    st.rerun()
            with col2:
                if st.button("Cancel", key="cancel_delete_history"):
                    del st.session_state['pending_delete_history_id']
                    st.rerun()
        else:
            st.info("No payment/reconciliation history found.")# --- Policy Revenue Ledger ---
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

        if selected_policy and selected_policy != "Select...":            # Get all rows for this policy, using only real database data
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
            import numpy as np
            if not policy_rows.empty:
                # --- Ledger construction using mapped column names ---
                # Get mapped column names for credits and debits
                credit_col = get_mapped_column("Agent Estimated Comm $") or "Agent Estimated Comm $"
                debit_col = get_mapped_column("Agent Paid Amount (STMT)") or "Agent Paid Amount (STMT)"
                transaction_id_col = get_mapped_column("Transaction ID") or "Transaction ID"
                stmt_date_col = get_mapped_column("STMT DATE") or "STMT DATE"
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
                    ledger_df["Credit (Commission Owed)"] = 0.0                # Debit (Paid to Agent) from mapped Agent Paid Amount (STMT)
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
                if st.button("Test Mapping (Preview Policy Details)", key="test_mapping_policy_details_btn") or st.session_state.get("show_policy_details_mapping_preview", False):
                    st.session_state["show_policy_details_mapping_preview"] = True
                    
                    def get_policy_details_column_mapping(col, val):
                        mapping = {
                            "Customer": "customer",
                            "Client ID": "client_id",
                            "Policy Number": "policy_number",
                            "Policy Type": "policy_type",
                            "Carrier Name": "carrier_name",
                            "Effective Date": "policy_effective_date",
                            "Policy Origination Date": "policy_origination_date",
                            "Policy Gross Comm %": "policy_commission_pct",
                            "Agent Comm (NEW 50% RWL 25%)": "agent_commission_pct",
                            "X-DATE": "policy_expiration_date"
                        }
                        db_col = mapping.get(col, col)
                        return {
                            "UI Column Title": col,
                            "Database Column Name": db_col,
                            "Current Value": val
                        }
                    mapping_table = [get_policy_details_column_mapping(col, edited_details_df.iloc[0][col]) for col in policy_detail_cols] if not edited_details_df.empty else []
                    mapping_df = pd.DataFrame(mapping_table)
                    with st.expander("Preview Policy Details Mapping & Changes", expanded=True):
                        st.write("**Column Mapping (UI → Database):**")
                        st.dataframe(mapping_df, use_container_width=True)
                else:
                    st.session_state["show_policy_details_mapping_preview"] = False
                if st.button("Save Policy Details", key="save_policy_details_btn") and not edited_details_df.empty:
                    update_sql = "UPDATE policies SET " + ", ".join([f'"{col}" = :{col}' for col in policy_detail_cols if col != "Policy Number"]) + " WHERE \"Policy Number\" = :policy_number"
                    update_params = {col: edited_details_df.iloc[0][col] for col in policy_detail_cols if col != "Policy Number"}
                    update_params["policy_number"] = edited_details_df.iloc[0]["Policy Number"]
                    with engine.begin() as conn:
                        conn.execute(sqlalchemy.text(update_sql), update_params)
                    st.success("Policy details updated.")
                    st.rerun()

                st.markdown("### Policy Ledger (Editable)")                # Ensure Credit and Debit columns are numeric
                if "Credit (Commission Owed)" in ledger_df.columns:
                    ledger_df["Credit (Commission Owed)"] = pd.to_numeric(ledger_df["Credit (Commission Owed)"], errors="coerce").fillna(0.0)
                if "Debit (Paid to Agent)" in ledger_df.columns:
                    ledger_df["Debit (Paid to Agent)"] = pd.to_numeric(ledger_df["Debit (Paid to Agent)"], errors="coerce").fillna(0.0)

                # Lock formula columns
                formula_columns = []
                for col in ["Credit (Commission Owed)", "Debit (Paid to Agent)"]:
                    if col in ledger_df.columns:
                        formula_columns.append(col)
                column_config = {}
                for col in ledger_df.columns:
                    if col in formula_columns:
                        column_config[col] = {"disabled": True}

                # Prevent deletion of the first (opening) row
                ledger_df_display = ledger_df.copy()
                ledger_df_display["Delete"] = True
                ledger_df_display.loc[0, "Delete"] = False  # Opening row cannot be deleted
                display_cols = ledger_columns + ["Delete"]

                # --- Ensure all display columns exist in the DataFrame ---
                for col in display_cols:
                    if col not in ledger_df_display.columns:
                        # For Delete, default to True except first row; for others, empty string
                        if col == "Delete":
                            ledger_df_display[col] = [True] * len(ledger_df_display)
                            if len(ledger_df_display) > 0:
                                ledger_df_display.loc[0, "Delete"] = False
                        else:
                            ledger_df_display[col] = ""
                # Reorder columns safely
                ledger_df_display = ledger_df_display[display_cols]

                st.markdown("<b>Why are some columns locked?</b>", unsafe_allow_html=True)
                with st.expander("Locked Columns Explanation", expanded=False):
                    st.markdown("""
                    Some columns in the Policy Revenue Ledger are locked because their values are automatically calculated by the app based on other fields or business rules. These formula columns ensure the accuracy of your commission and revenue calculations. If you need to change a value in a locked column, you must update the underlying fields that drive the calculation, or contact your administrator if you believe the formula needs to be changed.
                    
                    **Locked columns in this ledger include:**
                    - Credit (Commission Owed)
                    - Debit (Paid to Agent)
                    """)

                # Show the table as editable, with locked columns and strictly no row add/delete
                # Lock formula columns and Transaction ID, and set num_rows to 'fixed' to prevent row add/delete
                column_config["Credit (Commission Owed)"] = {
                    "disabled": True,
                    "help": "This column is automatically calculated and cannot be edited. See 'Why are some columns locked?' above."
                }
                column_config["Debit (Paid to Agent)"] = {
                    "disabled": True,
                    "help": "This column is automatically calculated and cannot be edited. See 'Why are some columns locked?' above."
                }
                column_config["Transaction ID"] = {
                    "disabled": True,
                    "help": "Transaction ID is a unique identifier and cannot be changed."
                }
                edited_ledger_df = st.data_editor(
                    ledger_df_display,
                    use_container_width=True,
                    height=max(400, 40 + 40 * len(ledger_df_display)),
                    key="policy_ledger_editor",
                    num_rows="fixed",
                    column_config=column_config,
                    hide_index=True
                )

                # Strictly prevent row addition and deletion: only allow editing of existing rows
                # Remove the Delete column before saving (no row deletion allowed)
                edited_ledger_df = edited_ledger_df.drop(columns=["Delete"])
                # Only keep the original ledger columns (no extra columns)
                edited_ledger_df = edited_ledger_df[ledger_columns]                # --- Test Mapping (Preview Policy Ledger) Button and Expander ---
                if st.button("Test Mapping (Preview Policy Ledger)", key="test_mapping_policy_ledger_btn") or st.session_state.get("show_policy_ledger_mapping_preview", False):
                    st.session_state["show_policy_ledger_mapping_preview"] = True
                    def get_policy_ledger_column_mapping(col, val):
                        mapping = {
                            "Transaction ID": "transaction_id",
                            "Description": "description",
                            "Credit (Commission Owed)": "agent_estimated_comm",
                            "Debit (Paid to Agent)": "Agent Paid Amount (STMT)",
                            "Transaction Type": "transaction_type"
                        }
                        db_col = mapping.get(col, col)
                        return {
                            "UI Column Title": col,
                            "Database Column Name": db_col,
                            "Current Value": val
                        }
                    mapping_table = [get_policy_ledger_column_mapping(col, edited_ledger_df.iloc[0][col] if not edited_ledger_df.empty else "") for col in ledger_columns]
                    mapping_df = pd.DataFrame(mapping_table)
                    with st.expander("Preview Policy Ledger Mapping & Changes", expanded=True):
                        st.write("**Column Mapping (UI → Database):**")
                        st.dataframe(mapping_df, use_container_width=True)
                        st.write("**Proposed Policy Ledger Preview:**")
                        st.dataframe(edited_ledger_df, use_container_width=True)
                else:
                    st.session_state["show_policy_ledger_mapping_preview"] = False                # --- Ledger Totals Section ---
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
                    st.rerun()    # --- Help ---
    elif page == "Help":
        st.title("📚 Help & Documentation")
        
        # Create tabs for organized help content
        tab1, tab2, tab3, tab4 = st.tabs(["Getting Started", "Features Guide", "Troubleshooting", "About"])
        
        with tab1:
            st.subheader("🚀 Getting Started")
            st.write("""
            Welcome to the Commission Management Application! This powerful tool helps you manage insurance 
            commission data, track policies, and generate comprehensive reports.
            
            **Quick Start Steps:**
            1. **Add Policy Data**: Use "Add New Policy Transaction" to input your policy information
            2. **View Data**: Navigate to "All Policies in Database" to see your complete dataset
            3. **Generate Reports**: Visit the "Reports" section for analytics and summaries
            4. **Manage Accounting**: Use "Accounting" for commission reconciliation and payments
            """)
            
            st.info("💡 **Tip**: Start by adding a few sample policies to explore all features!")
        
        with tab2:
            st.subheader("📖 Features Guide")
            
            # Dashboard features
            st.write("**📊 Dashboard**")
            st.write("- View key metrics and policy summaries")
            st.write("- Search and edit policies quickly")
            st.write("- Monitor recent activity and statistics")
            
            st.divider()
            
            # Database features
            st.write("**💾 Database Management**")
            st.write("- **All Policies**: Browse paginated policy data with export options")
            st.write("- **Edit Policies**: Search and modify existing policy records")
            st.write("- **Add New**: Create new policy transactions with auto-generated IDs")
            
            st.divider()
            
            # Reporting features
            st.write("**📈 Reports & Analytics**")
            st.write("- **Reports**: Generate summary and commission analysis reports")
            st.write("- **Search & Filter**: Advanced filtering with multiple criteria")
            st.write("- **Policy Revenue Ledger**: Detailed revenue tracking and calculations")
            
            st.divider()
            
            # Administrative features
            st.write("**⚙️ Administrative Tools**")
            st.write("- **Admin Panel**: Database management and system tools")
            st.write("- **Tools**: Utilities for calculations and data formatting")
            st.write("- **Accounting**: Commission reconciliation and payment tracking")
        
        with tab3:
            st.subheader("🔧 Troubleshooting")
            
            st.write("**Common Issues and Solutions:**")
            
            st.write("**❓ No data showing in Dashboard**")
            st.write("- Solution: Add policy data using 'Add New Policy Transaction'")
            st.write("- Check that the database file 'commissions.db' exists")
            
            st.write("**❓ Error saving changes**")
            st.write("- Solution: Ensure all required fields are filled correctly")
            st.write("- Check database permissions and disk space")
            
            st.write("**❓ Slow performance**")
            st.write("- Solution: The app uses caching for better performance")
            st.write("- Large datasets may take longer to load initially")
            
            st.write("**❓ Export not working**")
            st.write("- Solution: Ensure you have data to export")
            st.write("- Check browser settings for file downloads")
            
            st.info("💭 **Need more help?** Contact your system administrator or developer.")
        
        with tab4:
            st.subheader("ℹ️ About")
            st.write("""
            **Commission Management Application**
            
            This application is designed to help insurance agencies and professionals manage their 
            commission data efficiently. Built with Streamlit and Python, it provides a comprehensive 
            suite of tools for policy management, reporting, and financial tracking.
            
            **Key Technologies:**
            - **Frontend**: Streamlit
            - **Database**: SQLite  
            - **Data Processing**: Pandas
            - **File Formats**: CSV, PDF support
            
            **Features:**
            - ✅ Complete CRUD operations for policy data
            - ✅ Advanced search and filtering capabilities
            - ✅ Comprehensive reporting and analytics
            - ✅ Commission reconciliation tools
            - ✅ Data export and import functionality
            - ✅ User-friendly dashboard interface
            
            **Version**: 2.0
            **Last Updated**: 2025
            """)
            
            st.success("🎉 Thank you for using the Commission Management Application!")
    
    # --- Policy Revenue Ledger Reports ---
    elif page == "Policy Revenue Ledger Reports":
        st.subheader("Policy Revenue Ledger Reports")
        st.success("📊 Generate customizable reports for policy summaries with Balance Due calculations and export capabilities.")
        
        if all_data.empty:
            st.warning("No policy data loaded. Please check database connection or import data.")
        else:
            # Simple data processing - AGGREGATE BY POLICY NUMBER using mapped columns
            # This ensures one row per policy with totals from all transactions
            working_data = all_data.copy()
            
            # Get mapped column for Policy Number
            policy_number_col = get_mapped_column("Policy Number") or "Policy Number"
            
            # Group by Policy Number and aggregate the data
            if policy_number_col in working_data.columns and not working_data.empty:
                # Define aggregation rules using mapped column names
                agg_dict = {}
                
                # For descriptive fields, take the first value (they should be the same for all transactions of the same policy)
                descriptive_field_names = ["Customer", "Policy Type", "Carrier Name", "Effective Date", 
                                         "Policy Origination Date", "X-DATE", "Client ID"]
                for field_name in descriptive_field_names:
                    mapped_col = get_mapped_column(field_name)
                    target_col = mapped_col if mapped_col and mapped_col in working_data.columns else (field_name if field_name in working_data.columns else None)
                    if target_col:
                        agg_dict[target_col] = 'first'                  # For monetary fields, sum all transactions for each policy
                monetary_field_names = ["Agent Estimated Comm $", "Agent Paid Amount (STMT)", 
                                       "Agency Estimated Comm/Revenue (CRM)", "Premium Sold", "Policy Gross Comm %"]
                for field_name in monetary_field_names:
                    mapped_col = get_mapped_column(field_name)
                    target_col = mapped_col if mapped_col and mapped_col in working_data.columns else (field_name if field_name in working_data.columns else None)
                    if target_col:
                        # Convert to numeric first, then sum
                        working_data[target_col] = pd.to_numeric(working_data[target_col], errors='coerce').fillna(0)
                        agg_dict[target_col] = 'sum'
                
                # For percentage fields, take the first value (should be consistent per policy)
                percentage_fields = ["Agent Comm (NEW 50% RWL 25%)", "Policy Gross Comm %"]
                for field in percentage_fields:
                    if field in working_data.columns and field not in agg_dict:
                        agg_dict[field] = 'first'
                
                # Group by Policy Number and aggregate
                working_data = working_data.groupby('Policy Number', as_index=False).agg(agg_dict)
            
            # Calculate Policy Balance Due using the EXACT same formula as Policy Revenue Ledger page
            # This ensures consistency between the two pages
            
            # Calculate BALANCE DUE using the same logic as the Policy Revenue Ledger page
            # Force recalculation by removing existing Policy Balance Due column if it exists
            if "Policy Balance Due" in working_data.columns:
                working_data = working_data.drop(columns=["Policy Balance Due"])
            
            # Check for required columns and calculate
            # Formula: Policy Balance Due = "Agent Estimated Comm $" - "Agent Paid Amount (STMT)"
            if "Agent Paid Amount (STMT)" in working_data.columns and "Agent Estimated Comm $" in working_data.columns:
                paid_amounts = pd.to_numeric(working_data["Agent Paid Amount (STMT)"], errors="coerce").fillna(0)
                commission_amounts = pd.to_numeric(working_data["Agent Estimated Comm $"], errors="coerce").fillna(0)
                
                working_data["Policy Balance Due"] = commission_amounts - paid_amounts
            else:
                # If we don't have the required columns, create with zeros
                working_data["Policy Balance Due"] = 0
            
            # Ensure Policy Balance Due is numeric for calculations
            if "Policy Balance Due" in working_data.columns:
                working_data["Policy Balance Due"] = pd.to_numeric(working_data["Policy Balance Due"], errors="coerce").fillna(0)
              # Calculate metrics using the same logic as Policy Revenue Ledger page
            total_policies = len(working_data)
            
            # Count unique policies that have outstanding balance due (Policy Balance Due > 0)
            # This matches the UI formula used on the Policy Revenue Ledger page
            if "Policy Balance Due" in working_data.columns:
                # Get unique policies with Policy Balance Due > 0
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
            
            # Enhanced Column Selection and Template Management
            st.markdown("### 🔧 Column Selection & Templates")
            
            # Initialize session state for templates
            if "prl_templates" not in st.session_state:
                st.session_state.prl_templates = {}
            
            # Get all available columns
            all_columns = list(working_data.columns)
              # Default column selection (updated to use correct column names)
            default_columns = ["Customer", "Policy Number", "Agent Estimated Comm $", "Agent Paid Amount (STMT)", "Policy Balance Due"]
            available_default_columns = [col for col in default_columns if col in all_columns]
            
            # Initialize selected columns in session state
            if "prl_selected_columns" not in st.session_state:
                st.session_state.prl_selected_columns = available_default_columns            # Column selection interface
            col_selection_col1, col_selection_col2 = st.columns([2, 1])
            
            with col_selection_col1:
                st.markdown("**Select Columns:**")
                
                # Available columns multiselect (restored to original style)
                selected_columns = st.multiselect(
                    "Choose columns to display in your report",
                    options=all_columns,
                    default=st.session_state.prl_selected_columns,
                    key="prl_column_multiselect"
                )
                
                # Update session state
                st.session_state.prl_selected_columns = selected_columns
                
                # Column reordering with streamlit_sortables (compact style like Edit Policies page)
                if selected_columns:
                    reorder_col1, reorder_col2 = st.columns([4, 1])
                    
                    with reorder_col1:
                        st.markdown("**Reorder columns by dragging the boxes below:**")
                    
                    with reorder_col2:
                        if st.button("🔄 Refresh", key="refresh_reorder", help="Refresh reorder section to sync with selected columns"):
                            # Force sync by updating the sortable key
                            if "prl_column_order_sortable_counter" not in st.session_state:
                                st.session_state.prl_column_order_sortable_counter = 0
                            st.session_state.prl_column_order_sortable_counter += 1
                            st.rerun()
                    
                    # Generate unique key for sortable component
                    sortable_key = f"prl_column_order_sortable_{st.session_state.get('prl_column_order_sortable_counter', 0)}"
                    
                    reordered_columns = streamlit_sortables.sort_items(
                        items=selected_columns,
                        direction="horizontal",
                        key=sortable_key
                    )
                    
                    # Update session state with reordered columns
                    st.session_state.prl_selected_columns = reordered_columns
                    selected_columns = reordered_columns
            
            with col_selection_col2:
                st.markdown("**Quick Presets:**")
                if st.button("💰 Financial Focus"):
                    financial_cols = ["Customer", "Policy Number", "Agency Estimated Comm/Revenue (CRM)", "Agent Estimated Comm $", "Agent Paid Amount (STMT)", "Policy Balance Due"]
                    st.session_state.prl_selected_columns = [col for col in financial_cols if col in all_columns]
                    st.rerun()
                
                if st.button("📋 Basic Info"):
                    basic_cols = ["Customer", "Policy Type", "Carrier Name", "Policy Number", "Effective Date"]
                    st.session_state.prl_selected_columns = [col for col in basic_cols if col in all_columns]
                    st.rerun()
            
            # Template Management Section
            st.markdown("### 💾 Template Management")
            template_col1, template_col2, template_col3 = st.columns(3)
            
            with template_col1:
                st.markdown("**Save New Template:**")
                new_template_name = st.text_input(
                    "Template Title",
                    placeholder="Enter custom report title",
                    help="Give your template a descriptive name"
                )
                
                if st.button("💾 Save Template", disabled=not new_template_name or not selected_columns):
                    if new_template_name in st.session_state.prl_templates:
                        st.error(f"Template '{new_template_name}' already exists!")
                    else:
                        st.session_state.prl_templates[new_template_name] = {
                            "columns": selected_columns.copy(),
                            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.success(f"✅ Template '{new_template_name}' saved!")
                        st.rerun()
            
            with template_col2:
                st.markdown("**Load Template:**")
                if st.session_state.prl_templates:
                    template_to_load = st.selectbox(
                        "Select template to load",
                        options=list(st.session_state.prl_templates.keys()),
                        key="template_loader"
                    )
                    
                    if st.button("📂 Load Template"):
                        template_data = st.session_state.prl_templates[template_to_load]
                        # Only load columns that still exist in the data
                        valid_columns = [col for col in template_data["columns"] if col in all_columns]
                        st.session_state.prl_selected_columns = valid_columns
                        st.success(f"✅ Loaded template: {template_to_load}")
                        st.rerun()
                else:
                    st.info("No saved templates yet")
            
            with template_col3:
                st.markdown("**Manage Templates:**")
                if st.session_state.prl_templates:
                    template_to_manage = st.selectbox(
                        "Select template to manage",
                        options=list(st.session_state.prl_templates.keys()),
                        key="template_manager"
                    )
                    
                    manage_col1, manage_col2 = st.columns(2)
                    with manage_col1:
                        if st.button("✏️ Edit"):
                            # Load template for editing
                            template_data = st.session_state.prl_templates[template_to_manage]
                            valid_columns = [col for col in template_data["columns"] if col in all_columns]
                            st.session_state.prl_selected_columns = valid_columns
                            st.info(f"Loaded '{template_to_manage}' for editing. Modify columns above and save with a new name.")
                    
                    with manage_col2:
                        if st.button("🗑️ Delete"):
                            del st.session_state.prl_templates[template_to_manage]
                            st.success(f"✅ Deleted template: {template_to_manage}")
                            st.rerun()
                else:
                    st.info("No templates to manage")
              # Show current template status
            if st.session_state.prl_templates:
                with st.expander("📋 Saved Templates", expanded=False):
                    for name, data in st.session_state.prl_templates.items():
                        st.write(f"**{name}** - Created: {data['created']} - Columns: {len(data['columns'])}")
            
            # Data Preview with Selected Columns
            st.markdown("### 📊 Report Preview")
            if selected_columns and not working_data.empty:
                # Filter to only include columns that exist
                valid_columns = [col for col in selected_columns if col in working_data.columns]
                
                if valid_columns:
                    # Pagination controls
                    pagination_col1, pagination_col2, pagination_col3 = st.columns([2, 1, 1])
                    
                    with pagination_col1:
                        records_per_page = st.selectbox(
                            "Records per page:",
                            options=[20, 50, 100, 200, 500, "All"],
                            index=0,
                            key="prl_records_per_page"                        )
                    
                    with pagination_col2:
                        if records_per_page != "All":
                            # Ensure records_per_page is treated as integer for calculations
                            records_per_page_int = int(records_per_page)
                            total_pages = max(1, (len(working_data) + records_per_page_int - 1) // records_per_page_int)
                            current_page = st.number_input(
                                "Page:",
                                min_value=1,
                                max_value=total_pages,
                                value=1,
                                key="prl_current_page"
                            )
                        else:
                            current_page = 1
                            total_pages = 1
                    
                    with pagination_col3:
                        if records_per_page != "All":
                            st.write(f"Page {current_page} of {total_pages}")
                    
                    # Apply pagination
                    if records_per_page == "All":
                        display_data = working_data[valid_columns]
                        caption_text = f"Showing all {len(working_data):,} records with {len(valid_columns)} columns"
                    else:
                        # Ensure type safety for calculations
                        records_per_page_int = int(records_per_page)
                        current_page_int = int(current_page)
                        start_idx = (current_page_int - 1) * records_per_page_int
                        end_idx = start_idx + records_per_page_int
                        display_data = working_data[valid_columns].iloc[start_idx:end_idx]
                        caption_text = f"Showing records {start_idx + 1}-{min(end_idx, len(working_data))} of {len(working_data):,} total records with {len(valid_columns)} columns"
                    
                    st.dataframe(display_data, use_container_width=True)
                    st.caption(caption_text)                    # Create report metadata for export
                    export_metadata = {
                        "Report Generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Report Type": "Policy Revenue Ledger Report",
                        "Total Records": f"{len(working_data):,}",
                        "Selected Columns": f"{len(valid_columns)} columns: {', '.join(valid_columns)}",
                        "Data Aggregation": "Grouped by Policy Number (one row per unique policy)",
                        "Balance Due Formula": "Agent Estimated Comm $ - Agent Paid Amount (STMT)",
                        "Page Size": f"{records_per_page} records per page" if records_per_page != "All" else "All records displayed",
                        "Outstanding Policies": f"{outstanding_policies:,} policies with balance due > $0",
                        "Total Balance Due": f"${total_balance:,.2f}"
                    }
                    
                    # Show active report parameters
                    st.markdown("### 📋 Active Report Parameters")
                    st.markdown("*These parameters will be included in exported files:*")
                    metadata_df = pd.DataFrame(list(export_metadata.items()), columns=["Parameter", "Value"])
                    st.dataframe(metadata_df, use_container_width=True, height=min(300, 40 + 40 * len(metadata_df)))
                    
                    # Enhanced export with custom filename and metadata
                    export_col1, export_col2, export_col3 = st.columns(3)
                    with export_col1:
                        custom_filename = st.text_input(
                            "Custom Export Filename (optional)",
                            placeholder="Leave blank for auto-generated name"
                        )
                    
                    with export_col2:
                        filename = custom_filename if custom_filename else f"policy_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        csv_filename = filename if filename.endswith('.csv') else filename + '.csv'
                        
                        # Create CSV with metadata header
                        csv_lines = ["# Policy Revenue Ledger Report - Export Parameters"]
                        for param, value in export_metadata.items():
                            csv_lines.append(f"# {param}: {value}")
                        csv_lines.append("# " + "="*50)
                        csv_lines.append("")  # Empty line before data
                        
                        # Add the actual data
                        csv_data = working_data[valid_columns].to_csv(index=False)
                        csv_with_metadata = "\n".join(csv_lines) + "\n" + csv_data
                        
                        st.download_button(
                            "📄 Export as CSV (with Parameters)",
                            csv_with_metadata,
                            csv_filename,
                            "text/csv",
                            help="CSV file includes report parameters in header comments"
                        )
                    
                    with export_col3:
                        excel_filename = filename if filename.endswith('.xlsx') else filename + '.xlsx'
                        
                        # Create Excel file with metadata sheet
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                            # Write metadata to first sheet
                            metadata_df.to_excel(writer, sheet_name='Report Parameters', index=False)
                            
                            # Write data to second sheet
                            working_data[valid_columns].to_excel(writer, sheet_name='Policy Revenue Report', index=False)
                            
                            # Get workbook and format metadata sheet
                            workbook = writer.book
                            metadata_sheet = writer.sheets['Report Parameters']                            # Format metadata sheet
                            header_format = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC'})
                            metadata_sheet.set_column('A:A', 25)
                            metadata_sheet.set_column('B:B', 50)
                            metadata_sheet.write_row(0, 0, ['Parameter', 'Value'], header_format)
                        
                        excel_buffer.seek(0)
                        
                        st.download_button(
                            "📊 Export as Excel (with Parameters)",
                            excel_buffer.getvalue(),
                            excel_filename,
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            help="Excel file includes report parameters on separate sheet"
                        )
                else:
                    st.warning("Selected columns are not available in the current data.")
            else:
                if not selected_columns:
                    st.info("Please select columns to display the report.")
                else:
                    st.warning("No data available for report generation.")
            
            # PDF printing instructions
            st.markdown("### 🖨️ Print to PDF")
            st.info("💡 **Tip:** To save this report as PDF, use your browser's print feature (Ctrl+P or Cmd+P) and select 'Save as PDF'. The report parameters shown above will be included in the PDF.")
            
            st.success("✅ Enhanced Policy Revenue Ledger Reports with Templates & Export Parameters!")
    
    # --- Pending Policy Renewals ---
    elif page == "Pending Policy Renewals":
        st.subheader("Pending Policy Renewals")
        
        if 'deleted_renewals' not in st.session_state:
            st.session_state['deleted_renewals'] = []

        pending_renewals_df = get_pending_renewals(all_data)
        duplicated_renewals_df = duplicate_for_renewal(pending_renewals_df)
        
        # Filter out deleted renewals
        if not duplicated_renewals_df.empty:
            display_df = duplicated_renewals_df[~duplicated_renewals_df.index.isin(st.session_state['deleted_renewals'])]
        else:
            display_df = pd.DataFrame()

        if not display_df.empty:
            display_df.insert(0, "Select", False)
            edited_df = st.data_editor(display_df)
            
            selected_rows = edited_df[edited_df["Select"]]
            
            if st.button("Renew Selected"):
                renewed_rows = selected_rows.drop(columns=["Select"])
                
                try:
                    with engine.begin() as conn:
                        renewed_rows.to_sql('policies', conn, if_exists='append', index=False)
                        
                        # Log the renewal
                        for _, row in renewed_rows.iterrows():
                            conn.execute(sqlalchemy.text("""
                                INSERT INTO renewal_history (renewal_timestamp, renewed_by, original_transaction_id, new_transaction_id, details)
                                VALUES (:ts, :user, :orig_id, :new_id, :details)
                            """), {
                                "ts": datetime.datetime.now().isoformat(),
                                "user": "system", # Placeholder for user management
                                "orig_id": row[get_mapped_column("Transaction ID")],
                                "new_id": generate_transaction_id(),
                                "details": row.to_json()
                            })
                    
                    st.success(f"{len(renewed_rows)} policies renewed successfully!")
                    # Remove renewed items from the pending list
                    st.session_state['deleted_renewals'].extend(selected_rows.index.tolist())
                    st.rerun()

                except Exception as e:
                    st.error(f"An error occurred during renewal: {e}")
            
            if st.button("Delete Selected"):
                st.session_state['deleted_renewals'].extend(selected_rows.index.tolist())
                st.rerun()
        else:
            st.info("No policies are pending renewal at this time.")
# Call main function
main()
