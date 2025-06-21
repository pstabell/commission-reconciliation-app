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
import logging
from column_mapping_config import (
    column_mapper, get_mapped_column, get_ui_field_name, 
    is_calculated_field, safe_column_reference
)

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
            <style>            /* Remove default padding and maximize main block width */
            .main .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }
        /* Make tables and editors use reasonable width */
        .stDataFrame, .stDataEditor {
        }        /* Force sidebar to be permanently visible and disable all collapse functionality */
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
        </style>
        """,
        unsafe_allow_html=True
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
    "Estimated Agent Comm (New 50% Renewal 25%)",
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
        revenue = float(row[agency_revenue_col]) if agency_revenue_col else 0.0
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

def main():
    # --- DEBUG: Surface any top-level exceptions ---

    import pdfplumber
    import os
    import json
    import datetime
    import io
    import uuid
    import random
    import string
    import streamlit_sortables as sortables
    import re    # Apply CSS styling
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
            "Accounting",
            "Help",
            "Policy Revenue Ledger",
            "Policy Revenue Ledger Reports"
        ]
    )

    # --- Database connection ---
    engine = sqlalchemy.create_engine('sqlite:///commissions.db')

    # ============================================================================
    # PHASE 1: DATABASE PROTECTION FUNCTIONS
    # Added: June 20, 2025 - Database Protection Implementation
    # Purpose: Prevent data loss and schema corruption during app operations
    # ============================================================================
    
    def create_automatic_backup():
        """Create timestamped backup of database before any schema changes."""
        try:
            import shutil
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"commissions_AUTO_BACKUP_{timestamp}.db"
            shutil.copy2("commissions.db", backup_path)
            logging.info(f"Database backup created: {backup_path}")
            return backup_path
        except Exception as e:
            logging.error(f"Failed to create database backup: {e}")
            return None
    
    def get_current_schema():
        """Get current table schema from database."""
        try:
            with engine.begin() as conn:
                result = conn.execute(sqlalchemy.text("PRAGMA table_info(policies)")).fetchall()
                schema = {row[1]: row[2] for row in result}  # column_name: data_type
                logging.info(f"Current schema retrieved: {len(schema)} columns")
                return schema
        except Exception as e:
            logging.error(f"Failed to get current schema: {e}")
            return {}
    
    def ensure_schema_integrity():
        """Ensure existing schema is preserved and not overwritten."""
        try:
            # Check if table exists
            with engine.begin() as conn:
                result = conn.execute(sqlalchemy.text(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='policies'"
                )).fetchone()
                
                if result:
                    # Table exists - preserve its schema
                    current_schema = get_current_schema()
                    if current_schema:
                        logging.info(f"Preserving existing schema with {len(current_schema)} columns")
                        return True
                
                # Table doesn't exist - safe to create
                logging.info("Table doesn't exist - safe to create new schema")
                return False
        except Exception as e:
            logging.error(f"Schema integrity check failed: {e}")
            return False
    
    def safe_add_column(column_name, column_type="TEXT", default_value=""):
        """Safely add a column to the policies table."""
        try:
            # Create backup first
            backup_path = create_automatic_backup()
            if not backup_path:
                logging.error("Cannot add column - backup failed")
                return False
            
            with engine.begin() as conn:
                # Check if column already exists
                existing_schema = get_current_schema()
                if column_name in existing_schema:
                    logging.info(f"Column '{column_name}' already exists")
                    return True
                
                # Add the column
                sql = f'ALTER TABLE policies ADD COLUMN "{column_name}" {column_type} DEFAULT "{default_value}"'
                conn.execute(sqlalchemy.text(sql))
                logging.info(f"Column '{column_name}' added successfully")
                return True
                
        except Exception as e:
            logging.error(f"Failed to add column '{column_name}': {e}")
            return False
    
    def safe_rename_column(old_name, new_name):
        """Safely rename a column in the policies table."""
        try:
            # Create backup first
            backup_path = create_automatic_backup()
            if not backup_path:
                logging.error("Cannot rename column - backup failed")
                return False
            
            with engine.begin() as conn:
                # Check if old column exists
                existing_schema = get_current_schema()
                if old_name not in existing_schema:
                    logging.error(f"Source column '{old_name}' does not exist")
                    return False
                
                if new_name in existing_schema:
                    logging.info(f"Target column '{new_name}' already exists")
                    return True
                
                # SQLite doesn't support direct column rename, so we need to recreate the table
                # Get all data first
                df = pd.read_sql('SELECT * FROM policies', conn)
                
                # Rename column in DataFrame
                if old_name in df.columns:
                    df = df.rename(columns={old_name: new_name})
                    
                    # Create temporary table with new schema
                    df.to_sql('policies_temp', conn, if_exists='replace', index=False)
                    
                    # Drop old table and rename temp table
                    conn.execute(sqlalchemy.text('DROP TABLE policies'))
                    conn.execute(sqlalchemy.text('ALTER TABLE policies_temp RENAME TO policies'))
                    
                    logging.info(f"Column renamed from '{old_name}' to '{new_name}' successfully")
                    return True
                else:
                    logging.error(f"Column '{old_name}' not found in data")
                    return False
                    
        except Exception as e:
            logging.error(f"Failed to rename column '{old_name}' to '{new_name}': {e}")
            return False
    
    def check_schema_consistency():
        """Check if database schema is consistent and report any issues."""
        try:
            issues = []
            current_schema = get_current_schema()
            
            if not current_schema:
                issues.append("Cannot access table schema")
                return issues
            
            # Check for minimum required columns
            required_columns = ["Customer", "Policy Type", "Carrier Name", "Policy Number"]
            for col in required_columns:
                if col not in current_schema:
                    issues.append(f"Missing required column: {col}")
              # Log schema health
            if issues:
                logging.warning(f"Schema issues found: {issues}")
            else:
                logging.info("Schema consistency check passed")
            
            return issues
            
        except Exception as e:
            logging.error(f"Schema consistency check failed: {e}")
            return [f"Check failed: {e}"]
    
    def show_recovery_options():
        """Show recovery options UI for database restoration."""
        st.subheader("🏥 Database Recovery & Health Center")
        
        # Schema Health Dashboard
        st.markdown("### 📊 Schema Health Dashboard")
        issues = check_schema_consistency()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            current_schema = get_current_schema()
            st.metric("Total Columns", len(current_schema))
        
        with col2:
            if issues:
                st.metric("Schema Issues", len(issues), delta=f"-{len(issues)} problems")
            else:
                st.metric("Schema Health", "✅ Healthy", delta="0 issues")
        
        with col3:
            # Count backup files
            backup_files = [f for f in os.listdir(".") if f.startswith("commissions_") and f.endswith(".db")]
            st.metric("Available Backups", len(backup_files))
        
        # Display any issues
        if issues:
            st.error("⚠️ Schema Issues Detected:")
            for issue in issues:
                st.write(f"• {issue}")
        else:
            st.success("✅ Schema is healthy and consistent")
        
        # Backup Management
        st.markdown("### 💾 Backup Management")
        
        # List available backups
        if backup_files:
            st.write("**Available Backup Files:**")
            backup_info = []
            for backup_file in sorted(backup_files, reverse=True):
                try:
                    # Get file modification time
                    mod_time = os.path.getmtime(backup_file)
                    mod_time_str = datetime.datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")
                    file_size = os.path.getsize(backup_file) // 1024  # KB
                    backup_info.append({
                        "File": backup_file,
                        "Created": mod_time_str,
                        "Size (KB)": file_size
                    })
                except Exception as e:
                    logging.warning(f"Could not read backup file info for {backup_file}: {e}")
            
            if backup_info:
                backup_df = pd.DataFrame(backup_info)
                st.dataframe(backup_df, use_container_width=True)
                  # Restore option
                selected_backup = st.selectbox("Select backup to restore:", [""] + [info["File"] for info in backup_info], key="recovery_backup_select")
                if selected_backup:
                    st.warning(f"⚠️ You are about to replace the current database with '{selected_backup}'. This cannot be undone!")
                    if st.button("🔄 Restore Selected Backup", key="restore_backup_btn"):
                        try:
                            # Create emergency backup of current state first
                            current_backup = create_automatic_backup()
                            if current_backup:
                                st.info(f"Current database backed up to: {current_backup}")
                            
                            # Restore selected backup
                            import shutil
                            shutil.copy2(selected_backup, "commissions.db")
                            st.success(f"✅ Database restored from '{selected_backup}' successfully!")
                            st.info("Please restart the application to see the restored data.")
                            logging.info(f"Database restored from backup: {selected_backup}")
                        except Exception as e:
                            st.error(f"❌ Failed to restore backup: {e}")
                            logging.error(f"Backup restoration failed: {e}")
        else:
            st.info("No backup files found in current directory")
          
        # Manual Backup Creation
        st.markdown("### 🛡️ Manual Backup Creation")
        if st.button("Create Manual Backup Now", key="manual_backup_btn"):
            backup_path = create_automatic_backup()
            if backup_path:
                st.success(f"✅ Manual backup created: {backup_path}")
            else:
                st.error("❌ Failed to create manual backup")
    
    # ============================================================================
    # END PHASE 1: DATABASE PROTECTION FUNCTIONS
    # ============================================================================
    
    def monitor_schema_changes():
        """Monitor and log schema changes for audit trail."""
        try:
            current_schema = get_current_schema()
            schema_hash = str(hash(str(sorted(current_schema.keys()))))
            
            # Store schema fingerprint for change detection
            if "last_schema_hash" not in st.session_state:
                st.session_state.last_schema_hash = schema_hash
                logging.info(f"Schema monitoring initialized with {len(current_schema)} columns")
            elif st.session_state.last_schema_hash != schema_hash:
                logging.warning(f"Schema change detected! New fingerprint: {schema_hash}")
                st.session_state.last_schema_hash = schema_hash
                
                # Show schema change notification
                st.info("🔄 Schema change detected - database protection active")
            
            return current_schema
        except Exception as e:
            logging.error(f"Schema monitoring failed: {e}")
            return {}
    
    # ============================================================================
    # PHASE 2: PROTECTED DATABASE SCHEMA SETUP  
    # CRITICAL: This replaces the dangerous schema recreation code
    # Purpose: Preserve existing schema and prevent data loss
    # ============================================================================
    
    # Check if we need to preserve existing schema
    preserve_existing = ensure_schema_integrity()
    
    if not preserve_existing:
        # Safe to create new table - no existing schema to preserve
        logging.info("Creating new policies table with default schema")
        with engine.begin() as conn:
            conn.execute(sqlalchemy.text("""                CREATE TABLE IF NOT EXISTS policies (
                    "Customer" TEXT,
                    "Policy Type" TEXT,
                    "Carrier Name" TEXT,
                    "Policy Number" TEXT,
                    "Transaction Type" TEXT,
                    "Agency Estimated Comm/Revenue (CRM)" REAL,
                    "Policy Origination Date" TEXT,
                    "Effective Date" TEXT,
                    "Paid" TEXT,
                    "Calculated Commission" REAL,
                    "Client ID" TEXT,
                    "Transaction ID" TEXT
                )
            """))
    else:
        # Existing schema detected - preserve it completely
        logging.info("Existing schema detected - preserving user modifications")
        current_schema = get_current_schema()
        logging.info(f"Preserved schema contains {len(current_schema)} columns: {list(current_schema.keys())}")
        
        # Check schema health but don't force changes
        issues = check_schema_consistency()
        if issues:
            logging.warning(f"Schema health check found issues: {issues}")
            # Note: We don't auto-fix issues to prevent data loss
            # User can address issues through Admin Panel if needed
      # ============================================================================
    # END PHASE 2: PROTECTED DATABASE SCHEMA SETUP
    # ============================================================================
      # PHASE 4: Initialize monitoring and protection status
    # monitor_schema_changes()  # Temporarily disabled to fix startup issue
    # show_protection_status()  # Temporarily disabled to fix startup issue

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
        "Agent Paid Amount (STMT)": "Agent Paid Amount (STMT)",
        "PAST DUE": "PAST DUE",
        "FULL OR MONTHLY PMTS": "FULL OR MONTHLY PMTS",
        "NOTES": "NOTES"
    }
    all_data.rename(columns=rename_dict, inplace=True)

    # Debug checkbox
    show_debug = st.sidebar.checkbox("Show Debug Info")

    if show_debug:
        st.write("DEBUG: all_data shape:", all_data.shape)
        st.write("DEBUG: all_data columns:", all_data.columns.tolist())
        st.write("DEBUG: page selected:", page)

    st.title("Sales Commission Tracker")

    # --- Navigation Logic: Top Level ---
    # --- Dashboard (Home Page) ---
    if page == "Dashboard":
        # --- Dashboard (Home Page) ---
        st.subheader("Dashboard")
        st.metric("Total Transactions", len(all_data))
        if "Calculated Commission" in all_data.columns:
            st.metric("Total Commissions", f"${all_data['Calculated Commission'].sum():,.2f}")
        st.write("Welcome! Use the sidebar to navigate.")        # --- Client Search & Edit (clean selectbox style) ---
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
            
            # --- Calculate PAST DUE for each row using mapped columns ---
            agent_paid_col = get_mapped_column("Agent Paid Amount (STMT)")
            agent_comm_col = get_mapped_column("Agent Estimated Comm $") or get_mapped_column("Estimated Agent Comm (New 50% Renewal 25%)")
            
            if agent_paid_col and agent_comm_col and agent_paid_col in client_df.columns and agent_comm_col in client_df.columns:
                paid_amounts = pd.to_numeric(client_df[agent_paid_col], errors="coerce").fillna(0)
                commission_amounts = pd.to_numeric(client_df[agent_comm_col], errors="coerce").fillna(0)
                client_df["PAST DUE"] = commission_amounts - paid_amounts
            else:
                st.warning(f"Missing required columns for PAST DUE calculation. Looking for: {agent_paid_col}, {agent_comm_col}")
            
            # --- Show metrics side by side, spaced in 6 columns, shifted left ---
            col1, col2, col3, col4, col5, col6 = st.columns(6)            # Move metrics to col2 and col3, leaving col6 open for future data
            with col2:
                if agent_paid_col and agent_paid_col in client_df.columns:
                    paid_amounts = pd.to_numeric(client_df[agent_paid_col], errors="coerce")
                    total_paid = paid_amounts.sum()
                    st.metric(label="Total Paid Amount", value=f"${total_paid:,.2f}")
                else:
                    st.warning(f"No '{get_ui_field_name('Agent Paid Amount (STMT)')}' column found for this client.")

            with col3:
                due_date_col = get_mapped_column("Due Date")
                if (
                    agent_paid_col and agent_paid_col in client_df.columns
                    and due_date_col and due_date_col in client_df.columns
                    and agent_comm_col and agent_comm_col in client_df.columns
                ):
                    today = pd.to_datetime(datetime.datetime.today())
                    due_dates = pd.to_datetime(client_df[due_date_col], errors="coerce")
                    paid_amounts = pd.to_numeric(client_df[agent_paid_col], errors="coerce").fillna(0)
                    commission_amounts = pd.to_numeric(client_df[agent_comm_col], errors="coerce").fillna(0)
                    # Only consider rows past due and not fully paid
                    past_due_mask = (due_dates < today) & (paid_amounts < commission_amounts)
                    total_past_due = (commission_amounts - paid_amounts)[past_due_mask].sum()
                    if pd.isna(total_past_due):
                        total_past_due = 0.0
                    st.metric(label="Total Past Due", value=f"${total_past_due:,.2f}")
                else:
                    st.metric(label="Total Past Due", value="$0.00")

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
                remaining_df = all_data[all_data["Customer"].str.strip().str.lower() != selected_client.strip().lower()]
                updated_df = pd.concat([remaining_df, client_df], ignore_index=True)
                updated_df.to_sql('policies', engine, if_exists='replace', index=False)
                st.success("Client data updated!")    # --- Add New Policy Transaction ---
    elif page == "Add New Policy Transaction":
        st.subheader("Add New Policy Transaction")
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
                st.session_state["premium_sold_input_live"] = premium_sold_calc        # --- Live Premium Sold and Agency Estimated Comm/Revenue (CRM) outside the form ---
        if "premium_sold_input" not in st.session_state:
            st.session_state["premium_sold_input"] = 0.0
        st.subheader("Enter Premium Sold and see Agency Estimated Comm/Revenue (CRM):")
        premium_sold_val = st.number_input(
            "Premium Sold",
            min_value=-1000000.0,
            max_value=1000000.0,
            step=0.01,
            format="%.2f",
            key="premium_sold_input_live"
        )
        agency_revenue_val = round(premium_sold_val * 0.10, 2)
        st.number_input(
            "Agency Estimated Comm/Revenue (CRM) (10% of Premium Sold)",
            value=agency_revenue_val,
            disabled=True,
            format="%.2f",
            key="agency_revenue_display_live"
        )

        # --- The rest of the form ---
        with st.form("add_policy_form"):
            new_row = {}
            transaction_id_col = get_mapped_column("Transaction ID")
            auto_transaction_id = generate_transaction_id() if transaction_id_col and transaction_id_col in db_columns else None
            assigned_client_id = st.session_state.get("assigned_client_id", None)
            assigned_client_name = st.session_state.get("assigned_client_name", None)
            
            # Get mapped column names for form exclusions
            skip_fields = [
                get_mapped_column("Lead Source"),
                get_mapped_column("Producer"), 
                get_mapped_column("Agency Gross Paid"),
                get_mapped_column("Paid"),
                get_mapped_column("Gross Agency Comm %"),
                get_mapped_column("Agency Gross Comm"),
                get_mapped_column("Statement Date"),
                get_mapped_column("STMT DATE"),
                get_mapped_column("Items"),
                get_mapped_column("Agent Paid Amount (STMT)"),
                get_mapped_column("PAST DUE")
            ]
            # Remove None values and add original names as fallback
            skip_fields = [f for f in skip_fields if f] + [
                "Lead Source", "Producer", "Agency Gross Paid", "Paid",
                "Gross Agency Comm %", "Agency Gross Comm", "Statement Date",
                "STMT DATE", "Items", "Agent Paid Amount (STMT)", "PAST DUE"            ]
            
            for col in db_columns:
                if col in skip_fields:
                    continue  # Skip these fields in the form
                
                premium_sold_col = get_mapped_column("Premium Sold")
                agency_revenue_col = get_mapped_column("Agency Estimated Comm/Revenue (CRM)")
                client_id_col = get_mapped_column("Client ID")
                customer_col = get_mapped_column("Customer")
                transaction_type_col = get_mapped_column("Transaction Type")
                
                if col == premium_sold_col or col == "Premium Sold":
                    new_row[col] = premium_sold_val
                elif col == agency_revenue_col or col == "Agency Estimated Comm/Revenue (CRM)":
                    new_row[col] = agency_revenue_val
                elif col == transaction_id_col or col == "Transaction ID":
                    val = st.text_input(col, value=auto_transaction_id, disabled=True)
                    new_row[col] = auto_transaction_id
                elif col == client_id_col or col == "Client ID":
                    val = st.text_input(col, value=assigned_client_id if assigned_client_id else generate_client_id(), disabled=True)
                    new_row[col] = val
                elif col == customer_col or col == "Customer":
                    val = st.text_input(col, value=assigned_client_name if assigned_client_name else "")
                    new_row[col] = val
                elif "date" in col.lower() or col.lower() in ["x-date", "xdate", "stmt date", "statement date"]:
                    # Check if this is a known date field using mapping
                    date_fields = ["Policy Origination Date", "Effective Date", "X-Date", "X-DATE", "Statement Date", "STMT DATE"]
                    is_known_date = any(get_mapped_column(df) == col for df in date_fields) or col in date_fields
                    
                    if is_known_date:
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
                elif col == transaction_type_col or col == "Transaction Type":
                    val = st.selectbox(col, ["NEW", "NBS", "STL", "BoR", "END", "PCH", "RWL", "REWRITE", "CAN", "XCL"])
                    new_row[col] = val
                else:
                    val = st.text_input(col)
                    new_row[col] = val
            submitted = st.form_submit_button("Add Transaction")
        
        if submitted:
            # Auto-generate IDs if present
            client_id_col = get_mapped_column("Client ID")
            transaction_id_col = get_mapped_column("Transaction ID")
            
            if client_id_col and client_id_col in db_columns:
                new_row[client_id_col] = generate_client_id()
            if transaction_id_col and transaction_id_col in db_columns:
                new_row[transaction_id_col] = auto_transaction_id
            # Calculate commission if needed
            if "Calculated Commission" in db_columns:            new_row["Calculated Commission"] = calculate_commission(new_row)
            
            # --- Calculate Agent Estimated Comm $ for new rows using mapped columns ---
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
            
            # Calculate Agent Estimated Comm $ using mapped columns
            agent_est_comm_col = get_mapped_column("Agent Estimated Comm $")
            if agent_est_comm_col and agent_est_comm_col in db_columns:
                premium_col = get_mapped_column("Premium Sold")
                policy_comm_col = get_mapped_column("Policy Gross Comm %")
                agent_comm_col = get_mapped_column("Agent Comm (NEW 50% RWL 25%)")
                
                premium = new_row.get(premium_col or "Premium Sold", 0)
                pct = new_row.get(policy_comm_col or "Policy Gross Comm %", 0)
                agent_comm_pct = new_row.get(agent_comm_col or "Agent Comm (NEW 50% RWL 25%)", 0)
                
                p = parse_money(premium)
                pc = parse_percent(pct)
                ac = parse_percent(agent_comm_pct)
                new_row[agent_est_comm_col] = p * (pc / 100.0) * (ac / 100.0)
            
            # Note: Policy Balance Due is now calculated dynamically in reports, 
            # not stored in the database
            
            new_df = pd.DataFrame([new_row])
            new_df.to_sql('policies', engine, if_exists='append', index=False)
            st.success("New policy transaction added!")
            st.rerun()
    
    elif page == "Reports":
        st.subheader("Customizable Report")

        # --- Column selection ---
        st.markdown("**Select columns to include in your report:**")
        columns = all_data.columns.tolist()
        selected_columns = st.multiselect("Columns", columns, default=columns)

        # --- Date range filter (user can pick which date column) using mapped columns ---
        date_field_names = ["Effective Date", "Policy Origination Date", "Due Date", "X-Date", "X-DATE"]
        available_date_columns = []
        for field_name in date_field_names:
            mapped_col = get_mapped_column(field_name)
            if mapped_col and mapped_col in all_data.columns:
                available_date_columns.append(mapped_col)
            elif field_name in all_data.columns:
                available_date_columns.append(field_name)
        
        date_col = None
        if available_date_columns:
            date_col = st.selectbox("Select date column to filter by:", available_date_columns)
        if date_col:
            min_date = pd.to_datetime(all_data[date_col], errors="coerce").min()
            max_date = pd.to_datetime(all_data[date_col], errors="coerce").max()
            date_range = st.date_input(
                "Date range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                format="MM/DD/YYYY"
            )
            # Handle all possible return types for st.date_input
            if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
                start_date, end_date = date_range
            elif isinstance(date_range, (tuple, list)) and len(date_range) == 1:
                start_date = end_date = date_range[0]
            elif isinstance(date_range, (tuple, list)) and len(date_range) == 0:
                start_date = end_date = None
            else:
                start_date = end_date = date_range
            if start_date is not None and end_date is not None:
                mask = (pd.to_datetime(all_data[date_col], errors="coerce") >= pd.to_datetime(start_date)) & \
                       (pd.to_datetime(all_data[date_col], errors="coerce") <= pd.to_datetime(end_date))
                report_df = all_data.loc[mask, selected_columns]
            else:
                report_df = all_data[selected_columns]
        else:
            report_df = all_data[selected_columns]        # --- Optional: Filter by Customer using mapped column ---
        customer_col = get_mapped_column("Customer")
        if customer_col and customer_col in all_data.columns:
            st.markdown("**Filter by Customer:**")
            customers = ["All"] + sorted(all_data[customer_col].dropna().unique().tolist())
            selected_customer = st.selectbox("Customer", customers)
            if selected_customer != "All":
                report_df = report_df[report_df[customer_col] == selected_customer]        # --- Policy Balance Due dropdown filter using mapped columns ---
        balance_due_options = ["All", "YES", "NO"]
        selected_balance_due = st.selectbox("Policy Balance Due", balance_due_options)
        
        # Calculate Policy Balance Due if not present using mapped column names
        balance_due_col = get_mapped_column("Policy Balance Due")
        agent_paid_col = get_mapped_column("Agent Paid Amount (STMT)")
        agent_est_comm_col = get_mapped_column("Agent Estimated Comm $")
        
        target_balance_col = balance_due_col or "Policy Balance Due"
        target_paid_col = agent_paid_col or "Agent Paid Amount (STMT)"
        target_comm_col = agent_est_comm_col or "Agent Estimated Comm $"
        
        if target_balance_col not in report_df.columns and target_paid_col in report_df.columns and target_comm_col in report_df.columns:
            paid_amounts = pd.to_numeric(report_df[target_paid_col], errors="coerce").fillna(0)
            commission_amounts = pd.to_numeric(report_df[target_comm_col], errors="coerce").fillna(0)
            report_df[target_balance_col] = commission_amounts - paid_amounts
        
        # Ensure Policy Balance Due is numeric for filtering
        if target_balance_col in report_df.columns:
            report_df[target_balance_col] = pd.to_numeric(report_df[target_balance_col], errors="coerce").fillna(0)
        
        # Apply Balance Due filter
        if selected_balance_due != "All" and target_balance_col in report_df.columns:
            if selected_balance_due == "YES":
                report_df = report_df[report_df[target_balance_col] > 0]
            elif selected_balance_due == "NO":
                report_df = report_df[report_df[target_balance_col] <= 0]

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

        st.info("To print or save this report as PDF, use your browser's print feature (Ctrl+P or Cmd+P).")    # --- All Policies in Database ---
    elif page == "All Policies in Database":
        st.subheader("All Policies in Database")
        st.info("Tip: Use your browser's zoom-out (Ctrl -) to see more columns. Scroll horizontally for wide tables.")        # Reduce the height so the table fits better on the page and horizontal scroll bar is visible
        st.dataframe(format_currency_columns(format_dates_mmddyyyy(all_data)), use_container_width=True, height=350)
      # --- Edit Policies in Database ---
    elif page == "Edit Policies in Database":
        st.write("🔍 PAGE REACHED - Edit Policies in Database section is executing!")
        st.subheader("Edit Policies in Database")
        db_columns = all_data.columns.tolist()
        st.markdown("**Reorder columns by dragging the boxes below (no delete):**")
        order = streamlit_sortables.sort_items(
            items=db_columns,
            direction="horizontal",
            key="edit_db_col_order_sortable"
        )
        # --- Lock formula columns in the data editor using mapped columns ---
        formula_fields = ["Agent Estimated Comm $", "Agency Estimated Comm/Revenue (CRM)", "Agency Estimated Comm/Revenue (AZ)"]
        lock_cols = []
        for field in formula_fields:
            mapped_col = get_mapped_column(field)
            if mapped_col and mapped_col in db_columns:
                lock_cols.append(mapped_col)
            elif field.lower().replace(" ", "").replace("$", "") in [col.lower().replace(" ", "").replace("$", "") for col in db_columns]:
                # Fallback fuzzy matching
                for col in db_columns:
                    if field.lower().replace(" ", "").replace("$", "") == col.lower().replace(" ", "").replace("$", ""):
                        lock_cols.append(col)
                        break
        
        column_config = {}
        for col in lock_cols:
            column_config[col] = {
                "disabled": True,
                "help": "This column is automatically calculated and cannot be edited. See 'Why are some columns locked?' above."
            }
        edited_db_df = st.data_editor(
            format_currency_columns(format_dates_mmddyyyy(all_data[order].reset_index(drop=True))),
            column_config=column_config
        )
        # --- Info: Locked columns title always visible, explanation expandable below the button ---
        st.markdown("<b>Why are some columns locked?</b>", unsafe_allow_html=True)
        with st.expander("Locked Columns Explanation", expanded=False):
            st.markdown("""
**Which columns are locked and why?**

- <b>Agent Estimated Comm $</b> and <b>Agency Estimated Comm/Revenue (CRM)</b> are always automatically calculated by the app using the latest formulas. You cannot edit these columns directly.
- This ensures that commission calculations are always accurate and consistent for all policies.
- If you need to change the formula, you must update the code (ask your developer or Copilot).

**Formulas:**
- <b>Agent Estimated Comm $</b>: <code>Premium Sold * (Policy Gross Comm % / 100) * Agent Comm (NEW 50% RWL 25%)</code>
- <b>Agency Estimated Comm/Revenue (CRM)</b>: <code>Premium Sold * (Policy Gross Comm % / 100)</code>
            """, unsafe_allow_html=True)
        
        if st.button("Update Database with Edits and Column Order"):
            edited_db_df = edited_db_df[order]
            # --- Recalculate formula columns using mapped column names ---
            def parse_money_bd(val):
                import re
                if val is None:
                    return 0.0
                try:
                    return float(re.sub(r'[^0-9.-]', '', str(val)))
                except Exception:
                    return 0.0
            def parse_percent_bd(val):
                import re
                if val is None:
                    return 0.0
                try:
                    return float(re.sub(r'[^0-9.-]', '', str(val)))
                except Exception:
                    return 0.0
                    
            # Get mapped column names for calculations
            agency_est_comm_col = get_mapped_column("Agency Estimated Comm/Revenue (CRM)")
            premium_col = get_mapped_column("Premium Sold") 
            gross_comm_col = get_mapped_column("Policy Gross Comm %")
            agent_est_comm_col = get_mapped_column("Agent Estimated Comm $")
            agent_comm_pct_col = get_mapped_column("Agent Comm (NEW 50% RWL 25%)")
            
            # Fallback to fuzzy matching if mapping not found
            if not agency_est_comm_col:
                agency_est_comm_col = next((col for col in edited_db_df.columns if col.strip().lower() in ["agency estimated comm/revenue (crm)", "agency estimated comm/revenue (az)"]), None)
            if not premium_col:
                premium_col = next((col for col in edited_db_df.columns if col.strip().lower() == "premium sold".lower()), None)
            if not gross_comm_col:
                gross_comm_col = next((col for col in edited_db_df.columns if col.strip().lower() == "policy gross comm %".lower()), None)
            if not agent_est_comm_col:
                agent_est_comm_col = next((col for col in edited_db_df.columns if col.strip().lower() == "agent estimated comm $".lower()), None)
            if not agent_comm_pct_col:
                agent_comm_pct_col = next((col for col in edited_db_df.columns if col.strip().lower() in ["agent comm (new 50% rwl 25%)", "agent comm (new 50% rwl 25%) (%)"]), None)
            
            # Recalculate Agency Estimated Comm/Revenue (CRM)
            if agency_est_comm_col and premium_col and gross_comm_col:
                edited_db_df[agency_est_comm_col] = edited_db_df.apply(
                    lambda row: parse_money_bd(row[premium_col]) * (parse_percent_bd(row[gross_comm_col]) / 100.0), axis=1
                )
                st.info(f"Recalculated '{agency_est_comm_col}' for all rows.")
            else:
                st.warning("Could not find all required columns for Agency Estimated Comm/Revenue (CRM) recalculation.")
                
            # Recalculate Agent Estimated Comm $
            if agent_est_comm_col and premium_col and gross_comm_col and agent_comm_pct_col:
                edited_db_df[agent_est_comm_col] = edited_db_df.apply(
                    lambda row: parse_money_bd(row[premium_col]) * (parse_percent_bd(row[gross_comm_col]) / 100.0) * (parse_percent_bd(row[agent_comm_pct_col]) / 100.0), axis=1
                )
                st.info(f"Recalculated '{agent_est_comm_col}' for all rows.")
            else:
                st.warning("Could not find all required columns for Agent Estimated Comm $ recalculation.")
            
            # Note: Policy Balance Due is now calculated dynamically in reports,
            # not stored in the database, so no recalculation needed here
            
            edited_db_df.to_sql('policies', engine, if_exists='replace', index=False)
            import time
            time.sleep(0.5)  # Give DB a moment to update            all_data = pd.read_sql('SELECT * FROM policies', engine)
            st.success("Database updated with your edits and new column order! Data reloaded.")
            st.rerun()

    # --- Search & Filter ---    
    elif page == "Search & Filter":
        st.subheader("Search & Filter Policies")

        # Dropdown to select which column to search by (all headers)
        columns = all_data.columns.tolist()
        customer_col = get_mapped_column("Customer")
        default_index = columns.index(customer_col) if customer_col and customer_col in columns else (columns.index("Customer") if "Customer" in columns else 0)
        st.markdown(
            """
            <style>
            /* Highlight the selectbox for 'Search by column' */
            div[data-testid="stSelectbox"]:has(label:contains('Search by column')) > div[data-baseweb="select"] {
                background-color: #fff3b0 !important;
                border: 2px solid #e6a800 !important;
                border-radius: 6px !important;
            }
            /* Highlight the selectbox for 'Policy Balance Due' */
            div[data-testid="stSelectbox"]:has(label:contains('Policy Balance Due')) > div[data-baseweb="select"] {
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

        # Dropdown to filter by Policy Balance Due status
        balance_due_options = ["All", "YES", "NO"]
        selected_balance_due = st.selectbox("Policy Balance Due", balance_due_options)

        filtered_data = all_data.copy()

        # Apply search filter
        if search_text:
            filtered_data = filtered_data[filtered_data[search_column].astype(str).str.contains(search_text, case=False, na=False)]
            
        # Calculate Policy Balance Due if not present (using correct column names)
        if "Policy Balance Due" not in filtered_data.columns and "Agent Paid Amount (STMT)" in filtered_data.columns and "Agent Estimated Comm $" in filtered_data.columns:
            paid_amounts = pd.to_numeric(filtered_data["Agent Paid Amount (STMT)"], errors="coerce").fillna(0)
            commission_amounts = pd.to_numeric(filtered_data["Agent Estimated Comm $"], errors="coerce").fillna(0)
            filtered_data["Policy Balance Due"] = commission_amounts - paid_amounts

        # Apply Policy Balance Due filter
        if selected_balance_due != "All" and "Policy Balance Due" in filtered_data.columns:
            if selected_balance_due == "YES":
                filtered_data = filtered_data[filtered_data["Policy Balance Due"] > 0]
            elif selected_balance_due == "NO":
                filtered_data = filtered_data[filtered_data["Policy Balance Due"] <= 0]

        st.subheader("Filtered Policies")
        st.dataframe(format_currency_columns(format_dates_mmddyyyy(filtered_data)), use_container_width=True, height=400)

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
        )    # --- Admin Panel ---
    elif page == "Admin Panel":
        st.warning("⚠️ The Admin Panel is for administrative use only. Changes here can affect your entire database. Proceed with caution!")
        st.header("Admin Panel: Column Mapping & Header Editing")
        
        # Get all available UI fields from the centralized mapper
        all_ui_fields = list(column_mapper.default_ui_fields.keys())
        db_columns = all_data.columns.tolist()
          # Load current mapping from centralized system
        current_mapping = column_mapper._load_mapping()

        st.subheader("Current Column Mapping")
        # Always show current mapping
        if current_mapping:
            mapping_df = pd.DataFrame(list(current_mapping.items()), columns=["App Field", "Mapped To"])
            st.dataframe(mapping_df, use_container_width=True)
        else:
            st.info("No column mapping found yet.")

        # --- Enhanced Database Columns Display with Mapping Status ---
        st.subheader("Current Database Columns")
        st.info("These are the actual column names that exist in your database, with mapping status:")
        
        # Create enhanced database columns display using centralized mapping
        db_column_info = []
        for i, db_col in enumerate(db_columns, 1):
            # Check if this database column is mapped to any UI field
            mapped_ui_fields = []
            mapping_status = "❌ Not Mapped"
            
            # Check current mapping to see which UI fields point to this DB column
            for ui_field, mapped_db_col in current_mapping.items():
                if mapped_db_col == db_col:
                    mapped_ui_fields.append(ui_field)
            
            if mapped_ui_fields:
                mapping_status = f"✅ Mapped to: {', '.join(mapped_ui_fields)}"
            elif column_mapper.is_calculated_field(db_col):
                mapping_status = "🔢 Calculated Field"
            
            db_column_info.append({
                "Index": i,
                "Database Column Name": db_col,
                "Mapping Status": mapping_status,
                "Available for Mapping": "No" if mapped_ui_fields else "Yes"
            })
        
        # Display as interactive dataframe
        db_columns_df = pd.DataFrame(db_column_info)
        st.dataframe(
            db_columns_df, 
            use_container_width=True, 
            height=min(500, 40 + 40 * len(db_columns_df)),
            column_config={
                "Index": st.column_config.NumberColumn("Index", width="small"),
                "Database Column Name": st.column_config.TextColumn("Database Column Name", width="medium"),
                "Mapping Status": st.column_config.TextColumn("Mapping Status", width="large"),
                "Available for Mapping": st.column_config.TextColumn("Available for Mapping", width="small")
            }
        )
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total DB Columns", len(db_columns))
        with col2:
            mapped_count = len([info for info in db_column_info if info["Mapping Status"].startswith("✅")])
            st.metric("Mapped Columns", mapped_count)
        with col3:
            unmapped_count = len([info for info in db_column_info if info["Mapping Status"].startswith("❌")])
            st.metric("Unmapped Columns", unmapped_count)
        with col4:
            calculated_count = len([info for info in db_column_info if info["Mapping Status"].startswith("🔢")])
            st.metric("Calculated Fields", calculated_count)
        
        # Show mapping health
        mapping_health = (mapped_count / len(db_columns)) * 100 if db_columns else 0
        if mapping_health >= 80:
            st.success(f"✅ Mapping Health: {mapping_health:.1f}% - Excellent coverage")
        elif mapping_health >= 60:
            st.warning(f"⚠️ Mapping Health: {mapping_health:.1f}% - Good coverage")
        else:
            st.error(f"❌ Mapping Health: {mapping_health:.1f}% - Needs improvement")
        
        # Quick actions for unmapped columns
        unmapped_columns = [info["Database Column Name"] for info in db_column_info if info["Mapping Status"].startswith("❌")]
        if unmapped_columns:
            with st.expander("🔧 Quick Map Unmapped Columns", expanded=False):
                st.info(f"Found {len(unmapped_columns)} unmapped database columns. You can quickly map them here:")
                
                for unmapped_col in unmapped_columns[:5]:  # Show first 5 unmapped columns
                    col_map1, col_map2, col_map3 = st.columns([2, 2, 1])
                    with col_map1:
                        st.write(f"**{unmapped_col}**")
                    with col_map2:
                        # Get available UI fields for quick mapping
                        available_ui_fields = column_mapper.get_available_ui_fields()
                        suggested_ui = st.selectbox(
                            f"Map to UI field:",
                            ["(Select UI field)"] + available_ui_fields,
                            key=f"quick_map_{unmapped_col}"
                        )
                    with col_map3:
                        if suggested_ui and suggested_ui != "(Select UI field)":
                            if st.button("Map", key=f"quick_map_btn_{unmapped_col}"):
                                # Update mapping using centralized system
                                new_mapping = current_mapping.copy()
                                new_mapping[suggested_ui] = unmapped_col
                                result = column_mapper.save_mapping(new_mapping, db_columns)
                                if result["success"]:
                                    st.success(f"✅ Mapped '{suggested_ui}' to '{unmapped_col}'")
                                    st.rerun()
                                else:
                                    st.error(f"❌ Failed to save mapping: {result['errors']}")
                
                if len(unmapped_columns) > 5:
                    st.info(f"Showing first 5 of {len(unmapped_columns)} unmapped columns. Use the main mapping editor below for complete management.")
        
        st.markdown("---")

        # --- Enhanced mapping editor with validation ---
        st.subheader("Edit Column Mapping (One at a Time)")
        mapping_locked_file = "column_mapping.locked"
        mapping_locked = os.path.exists(mapping_locked_file)
        admin_override = st.checkbox("Admin Override (Unlock Mapping)", value=False, key="admin_override_mapping")
        
        if mapping_locked and not admin_override:
            st.warning("Column mapping is locked after first use. Enable Admin Override to make changes.")
        else:
            # Show mapping table with edit buttons
            edit_col = st.selectbox("Select UI Field to Edit", all_ui_fields, key="edit_mapping_select")
            current_db_col = column_mapper.get_db_column(edit_col, fallback_to_ui=False)
            current_display = current_db_col if current_db_col else "(Calculated/Virtual)"
            st.write(f"**Current Mapping for '{edit_col}':** {current_display}")
            
            # Get available database columns (not already mapped)
            available_db_cols = column_mapper.get_available_db_columns(db_columns)
            if current_db_col and current_db_col not in available_db_cols:
                available_db_cols.append(current_db_col)
            
            options = ["(Calculated/Virtual)"] + sorted(available_db_cols)
            current_index = 0
            if current_display in options:
                current_index = options.index(current_display)
                
            new_mapping = st.selectbox(f"Map '{edit_col}' to:", options, index=current_index, key="edit_mapping_new")
            
            # Show preview of proposed mapping
            proposed_mapping = current_mapping.copy()
            if new_mapping == "(Calculated/Virtual)":
                proposed_mapping[edit_col] = "(Calculated/Virtual)"
            else:
                proposed_mapping[edit_col] = new_mapping
                
            st.markdown("**Proposed Mapping:**")
            preview_df = pd.DataFrame(list(proposed_mapping.items()), columns=["App Field", "Mapped To"])
            st.dataframe(preview_df, use_container_width=True)
            
            # Validate the proposed mapping
            validation = column_mapper.validate_mapping(proposed_mapping, db_columns)
            
            if validation["errors"]:
                for error in validation["errors"]:
                    st.error(error)
            
            if validation["warnings"]:
                for warning in validation["warnings"]:
                    st.warning(warning)
              # Backup before save
            backup_path = "commissions_backup.db"
            backup_log_path = "commissions_backup_log.json"
            
            if st.button("Backup Database Before Mapping Change", key="backup_before_mapping"):
                import shutil, datetime
                shutil.copyfile("commissions.db", backup_path)
                now_str = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                backup_log = {}
                if os.path.exists(backup_log_path):
                    with open(backup_log_path, "r") as f:
                        backup_log = json.load(f)
                    backup_log["last_backup_time"] = now_str
                with open(backup_log_path, "w") as f:
                    json.dump(backup_log, f)
                st.success(f"Database backed up to {backup_path} at {now_str}")
            
            # Confirm and save mapping
            if st.button("Save Mapping Change", key="save_one_at_a_time_mapping"):
                if not validation["errors"]:
                    # Use centralized mapping to save
                    result = column_mapper.save_mapping(proposed_mapping, db_columns)
                    if result["success"]:
                        st.success("Mapping updated successfully!")
                        # Lock mapping if not admin override
                        if not admin_override:
                            with open(mapping_locked_file, "w") as f:
                                f.write("locked")                        # Show warnings if any
                        if result.get("warnings"):
                            for warning in result["warnings"]:
                                st.warning(warning)
                        st.rerun()
                    else:
                        for error in result["errors"]:
                            st.error(error)
                else:
                    st.error("Cannot save mapping due to validation errors above.")

        # --- Enhanced file upload mapping ---
        st.subheader("Upload File to Auto-Configure Mapping")
        uploaded_file = st.file_uploader("Upload a file to customize mapping", type=["xlsx", "xls", "csv", "pdf"], key="admin_upload")
        if uploaded_file:
            df = None
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
            if df is not None:
                df.columns = df.columns.str.strip()
                uploaded_columns = df.columns.tolist()
                new_mapping = {}
                current_mapping = column_mapper._load_mapping()
                
                for col in all_ui_fields:
                    current_db_col = current_mapping.get(col)
                    if isinstance(current_db_col, str) and current_db_col in uploaded_columns:
                        idx = uploaded_columns.index(current_db_col) + 1
                    else:
                        idx = 0
                    mapped = st.selectbox(
                        f"Map '{col}' to uploaded column:",
                        options=[""] + uploaded_columns,
                        index=idx,                        key=f"admin_map_{col}_panel"
                    )
                    if mapped:
                        new_mapping[col] = mapped
                
                if st.button("Save File-Based Mapping", key="admin_save_mapping"):
                    # Validate and save the new mapping using centralized system
                    result = column_mapper.save_mapping(new_mapping, db_columns)
                    if result["success"]:
                        st.success("Mapping saved from uploaded file!")
                        if result.get("warnings"):
                            for warning in result["warnings"]:
                                st.warning(warning)
                        st.rerun()
                    else:
                        for error in result["errors"]:
                            st.error(error)
                
                st.subheader("Uploaded File Columns")
                st.write(uploaded_columns)
                st.subheader("Database Columns")
                st.write(all_data.columns.tolist())

        # --- Add/Delete Columns Section ---
        st.subheader("Add or Delete Database Columns")
        db_columns = all_data.columns.tolist()        # Add Column
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
                    # PHASE 3: Use safe_add_column instead of direct SQL
                    column_name = st.session_state["pending_add_col"]
                    if safe_add_column(column_name):
                        st.success(f"Column '{column_name}' added safely with backup protection.")
                    else:
                        st.error(f"Failed to add column '{column_name}'. Check logs for details.")
                    st.session_state.pop("pending_add_col")
                    st.rerun()
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
            st.rerun()        # --- Header renaming section ---
        st.subheader("Rename Database Column Headers")
        db_columns = all_data.columns.tolist()
        
        with st.form("rename_single_header_form"):
            col_to_rename = st.selectbox("Select column to rename", [""] + db_columns, index=0, key="rename_col_select")
            suggested_new_name = "Agency Estimated Comm/Revenue (CRM)" if col_to_rename == "Agency Estimated Comm/Revenue (AZ)" else ""
            new_col_name = st.text_input("New column name", value=suggested_new_name, key="rename_col_new_name")
            rename_submitted = st.form_submit_button("Rename Column")

        if rename_submitted:
            if col_to_rename and new_col_name and new_col_name != col_to_rename:
                # PHASE 3: Use safe_rename_column instead of direct SQL
                if safe_rename_column(col_to_rename, new_col_name):
                    st.success(f"Renamed column '{col_to_rename}' to '{new_col_name}' safely with backup protection.")
                else:
                    st.error(f"Failed to rename column '{col_to_rename}' to '{new_col_name}'. Check logs for details.")
                st.rerun()
            elif not col_to_rename:
                st.info("Please select a column to rename.")
            else:
                st.info("Please enter a new name different from the current column name.")        # --- Enhanced Backup/Restore Section ---
        st.subheader("Enhanced Database Backup & Restore System")
        st.info("💡 **New Enhanced Backup System:** Creates timestamped backups instead of overwriting, with download/upload functionality and live tracking log.")
        
        # Enhanced backup tracking log
        enhanced_backup_log_path = "enhanced_backup_tracking.json"
        
        def load_enhanced_backup_log():
            """Load enhanced backup tracking log."""
            if os.path.exists(enhanced_backup_log_path):
                try:
                    with open(enhanced_backup_log_path, "r") as f:
                        return json.load(f)
                except Exception:
                    return {"backups": [], "actions": []}
            return {"backups": [], "actions": []}
        
        def save_enhanced_backup_log(log_data):
            """Save enhanced backup tracking log."""
            try:
                with open(enhanced_backup_log_path, "w") as f:
                    json.dump(log_data, f, indent=2)
                return True
            except Exception as e:
                st.error(f"Failed to save backup log: {e}")
                return False
        
        def log_backup_action(action_type, details):
            """Log backup action to enhanced tracking log."""
            log_data = load_enhanced_backup_log()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            action = {
                "timestamp": timestamp,
                "action": action_type,
                "details": details
            }
            log_data["actions"].append(action)
            # Keep only last 50 actions to prevent file from growing too large
            log_data["actions"] = log_data["actions"][-50:]
            save_enhanced_backup_log(log_data)
        
        # Enhanced backup creation
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🛡️ Create Timestamped Backup")
            backup_description = st.text_input(
                "Backup Description (optional)", 
                placeholder="e.g., Before column rename operation",
                key="backup_description"
            )
            
            if st.button("Create Enhanced Backup", type="primary"):
                import shutil
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"commissions_ENHANCED_BACKUP_{timestamp}.db"
                
                try:
                    # Create timestamped backup
                    shutil.copy2("commissions.db", backup_filename)
                    
                    # Get file size for tracking
                    file_size = os.path.getsize(backup_filename) // 1024  # KB
                    
                    # Update enhanced tracking log
                    log_data = load_enhanced_backup_log()
                    backup_info = {
                        "filename": backup_filename,
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "size_kb": file_size,
                        "description": backup_description if backup_description else "Manual backup"
                    }
                    log_data["backups"].append(backup_info)
                    
                    # Log the action
                    log_backup_action("CREATE_BACKUP", {
                        "filename": backup_filename,
                        "size_kb": file_size,
                        "description": backup_description or "Manual backup"
                    })
                    
                    if save_enhanced_backup_log(log_data):
                        st.success(f"✅ Enhanced backup created: `{backup_filename}` ({file_size} KB)")
                        st.info(f"📝 Description: {backup_description or 'Manual backup'}")
                    else:
                        st.warning("⚠️ Backup created but tracking log update failed")
                        
                except Exception as e:
                    st.error(f"❌ Failed to create enhanced backup: {e}")
                    log_backup_action("CREATE_BACKUP_FAILED", {"error": str(e)})
        
        with col2:
            st.markdown("#### 📥 Download Current Database")
            
            # Prepare database for download
            try:
                with open("commissions.db", "rb") as f:
                    db_data = f.read()
                
                download_filename = f"commissions_download_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                
                st.download_button(
                    label="📥 Download Current Database",
                    data=db_data,
                    file_name=download_filename,
                    mime="application/octet-stream",
                    help="Download the current database file to your computer",
                    use_container_width=True
                )
                
                db_size = len(db_data) // 1024  # KB
                st.caption(f"Database size: {db_size} KB")
                
            except Exception as e:
                st.error(f"❌ Failed to prepare database for download: {e}")

        # Enhanced backup management and restore
        st.markdown("---")
        st.markdown("#### 📋 Enhanced Backup Management & Restore")
        
        log_data = load_enhanced_backup_log()
        
        # Show enhanced backup list
        if log_data.get("backups"):
            st.markdown("**Available Enhanced Backups:**")
            
            # Create display dataframe
            backups_df = pd.DataFrame(log_data["backups"])
            backups_df = backups_df.sort_values("timestamp", ascending=False)  # Most recent first
            
            # Add file existence check
            backups_df["exists"] = backups_df["filename"].apply(lambda x: "✅" if os.path.exists(x) else "❌")
            
            # Display table
            st.dataframe(
                backups_df[["timestamp", "filename", "size_kb", "description", "exists"]].rename(columns={
                    "timestamp": "Created",
                    "filename": "Filename", 
                    "size_kb": "Size (KB)",
                    "description": "Description",
                    "exists": "Available"
                }),
                use_container_width=True,
                height=200
            )
            
            # Restore functionality
            col1, col2 = st.columns([2, 1])
            with col1:
                available_backups = [b["filename"] for b in log_data["backups"] if os.path.exists(b["filename"])]
                if available_backups:
                    selected_backup = st.selectbox(
                        "Select backup to restore:",
                        options=[""] + available_backups,
                        format_func=lambda x: f"{x} ({next((b['description'] for b in log_data['backups'] if b['filename'] == x), '')})" if x else "Select backup...",
                        key="enhanced_restore_backup"
                    )
                    
                    if selected_backup:
                        backup_info = next((b for b in log_data["backups"] if b["filename"] == selected_backup), None)
                        if backup_info:
                            st.warning(f"⚠️ **Restore '{selected_backup}'?**\n\n"
                                     f"Created: {backup_info['timestamp']}\n"
                                     f"Description: {backup_info['description']}\n"
                                     f"Size: {backup_info['size_kb']} KB\n\n"
                                     f"This will **replace** the current database and **cannot be undone**!")
            
            with col2:
                if st.button("🔄 Restore Selected Backup", type="secondary", disabled=not selected_backup):
                    try:
                        # Create emergency backup of current state
                        emergency_backup = create_automatic_backup()
                        if emergency_backup:
                            st.info(f"Current state backed up to: {emergency_backup}")
                        
                        # Restore selected backup
                        import shutil
                        shutil.copy2(selected_backup, "commissions.db")
                        
                        # Log the restore action
                        log_backup_action("RESTORE_BACKUP", {
                            "restored_from": selected_backup,
                            "description": backup_info['description'] if backup_info else "Unknown"
                        })
                        
                        st.success(f"✅ Database restored from '{selected_backup}' successfully!")
                        st.info("🔄 **Please refresh the page** to see the restored data.")
                        
                    except Exception as e:
                        st.error(f"❌ Failed to restore backup: {e}")
                        log_backup_action("RESTORE_BACKUP_FAILED", {
                            "filename": selected_backup,
                            "error": str(e)
                        })
                else:
                    st.info("Select a backup above to restore")
        else:
            st.info("No enhanced backups found. Create your first enhanced backup above!")

        # Upload database functionality
        st.markdown("---")
        st.markdown("#### 📤 Upload Database")
        
        uploaded_db = st.file_uploader(
            "Upload a database file to replace the current one",
            type=["db"],
            help="Upload a .db file to replace the current database. This will overwrite all current data!",
            key="upload_database"
        )
        
        if uploaded_db:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.warning("⚠️ **Upload New Database?**\n\n"
                          f"Filename: {uploaded_db.name}\n"
                          f"Size: {len(uploaded_db.getvalue()) // 1024} KB\n\n"
                          "This will **replace** the current database and **cannot be undone**!")
            
            with col2:
                if st.button("📤 Upload & Replace Database", type="secondary"):
                    try:
                        # Create emergency backup of current state
                        emergency_backup = create_automatic_backup()
                        if emergency_backup:
                            st.info(f"Current state backed up to: {emergency_backup}")
                        
                        # Save uploaded file
                        with open("commissions.db", "wb") as f:
                            f.write(uploaded_db.getvalue())
                        
                        # Log the upload action
                        log_backup_action("UPLOAD_DATABASE", {
                            "filename": uploaded_db.name,
                            "size_kb": len(uploaded_db.getvalue()) // 1024
                        })
                        
                        st.success(f"✅ Database uploaded and replaced successfully!")
                        st.info("🔄 **Please refresh the page** to see the uploaded data.")
                        
                    except Exception as e:
                        st.error(f"❌ Failed to upload database: {e}")
                        log_backup_action("UPLOAD_DATABASE_FAILED", {
                            "filename": uploaded_db.name,
                            "error": str(e)
                        })

        # Live tracking log display
        st.markdown("---")
        st.markdown("#### 📊 Live Backup Activity Log")
        
        if log_data.get("actions"):
            st.markdown("**Recent Backup Actions:**")
            
            # Show last 10 actions
            recent_actions = log_data["actions"][-10:]
            recent_actions.reverse()  # Most recent first
            
            for action in recent_actions:
                action_type = action["action"]
                timestamp = action["timestamp"]
                details = action.get("details", {})
                
                if action_type == "CREATE_BACKUP":
                    st.success(f"🛡️ **{timestamp}** - Backup created: `{details.get('filename', 'Unknown')}` ({details.get('size_kb', 0)} KB) - {details.get('description', 'No description')}")
                elif action_type == "RESTORE_BACKUP":
                    st.info(f"🔄 **{timestamp}** - Restored from: `{details.get('restored_from', 'Unknown')}` - {details.get('description', 'No description')}")
                elif action_type == "UPLOAD_DATABASE":
                    st.info(f"📤 **{timestamp}** - Database uploaded: `{details.get('filename', 'Unknown')}` ({details.get('size_kb', 0)} KB)")
                elif "FAILED" in action_type:
                    st.error(f"❌ **{timestamp}** - {action_type}: {details.get('error', 'Unknown error')}")
                else:
                    st.write(f"📝 **{timestamp}** - {action_type}: {details}")
        else:
            st.info("No backup actions recorded yet.")

        # Legacy backup section (maintained for compatibility)
        st.markdown("---") 
        st.markdown("#### 🔄 Legacy Backup System (Compatibility)")
        st.caption("This is the original backup system, maintained for compatibility with existing workflows.")
        
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
            if st.button("Legacy Backup Database", help="Creates commissions_backup.db (overwrites existing)"):
                import shutil
                import datetime
                try:
                    import pytz
                    eastern = pytz.timezone("US/Eastern")
                    now_eastern = datetime.datetime.now(eastern)
                except ImportError:
                    now_eastern = datetime.datetime.now()
                shutil.copyfile("commissions.db", backup_path)
                now_str = now_eastern.strftime("%m/%d/%Y %I:%M:%S %p %Z")
                backup_log["last_backup_time"] = now_str
                with open(backup_log_path, "w") as f:
                    json.dump(backup_log, f)
                st.success(f"Legacy backup created: {backup_path} at {now_str}")
                last_backup_time = now_str
        with col2:
            if st.button("Restore from Legacy Backup"):
                import shutil
                if os.path.exists(backup_path):
                    shutil.copyfile(backup_path, "commissions.db")
                    st.success("Database restored from legacy backup. Please restart the app.")
                else:
                    st.error("No legacy backup file found. Please create a backup first.")        # Show last backup time
        if last_backup_time:
            st.info(f"Last legacy backup: {last_backup_time}")
        else:
            st.info("No legacy backup has been made yet.")

        # --- DATABASE PROTECTION & RECOVERY CENTER ---
        st.markdown("---")
        st.markdown("## 🛡️ Database Protection & Recovery Center")
        show_recovery_options()

        # --- Formula Documentation Section ---
        st.subheader("Current Formula Logic in App")
        st.markdown("""
**Below are the formulas/calculations currently used in the app. To change a formula, you must edit the code in `commission_app.py`.**

| Field/Column                                 | Formula/Logic                                                                                                 |
|----------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| Client ID                                   | Auto-generated if not provided. Used to uniquely identify clients.                                           |
| Transaction ID                              | Auto-generated if not provided. Used to uniquely identify transactions.                                      |
| Customer                                    | Client name. Entered by user or selected from existing clients.                                              |
| Carrier Name                                | Name of insurance carrier.                                                                                   |
| Policy Type                                 | Type of policy (e.g., Auto, Home, etc.).                                                                     |
| Policy Number                               | Policy number as provided by carrier.                                                                        |
| Transaction Type                            | Type of transaction (e.g., NEW, RWL, END, etc.).                                                            |
| Agent Comm (NEW 50% RWL 25%)                | Calculated: If Transaction Type is 'NEW', then `Premium Sold * 0.50`; if 'RWL' or 'RENEWAL', then `Premium Sold * 0.25`; else 0. |
| Policy Origination Date                     | Date policy was originally written. Stored as MM/DD/YYYY.                                                    |
| Effective Date                              | Policy effective date. Stored as MM/DD/YYYY.                                                                |
| X-DATE                                      | X-date (expiration date or cross-sell date). Stored as MM/DD/YYYY.                                          |
| NEW BIZ CHECKLIST COMPLETE                  | Yes/No or date. Used for tracking new business checklist completion.                                         |
| Premium Sold                                | Entered or calculated as `New/Revised Premium - Existing Premium`.                                           |
| Policy Gross Comm %                         | Entered as percent. Used in commission calculations.                                                         |
| STMT DATE                                   | Statement date. Stored as MM/DD/YYYY.                                                                       |
| Agency Estimated Comm/Revenue (CRM)         | Calculated: `Premium Sold * (Policy Gross Comm % / 100)`                                                    |
| Agency Comm Received (STMT)                 | Entered or imported. Used for reconciliation.                                                                |
| Agent Estimated Comm $                      | Calculated: `Premium Sold * (Policy Gross Comm % / 100) * Agent Comm (NEW 50% RWL 25%)`.                        |
| Agent Paid Amount (STMT)                   | Entered or imported. Used to track payments received.                                                        |
| BALANCE DUE                                 | Calculated: `[Agent Estimated Comm $] - [Agent Paid Amount (STMT)]`.                                        |
| FULL OR MONTHLY PMTS                        | Indicates payment frequency (full or monthly).                                                               |
| NOTES                                       | Freeform notes for the policy/transaction.                                                                   |

**Other Calculations/Logic:**
- Total Paid Amount: Sum of 'Agent Paid Amount (STMT)' for selected client or filtered rows.
- Total Balance Due: Sum of 'BALANCE DUE' for overdue, underpaid policies.
- Add New Policy Transaction: Date fields are entered as MM/DD/YYYY, stored as text.
- Edit Policies in Database: 'BALANCE DUE' recalculated for all rows on update.
- Reports/Search: If 'BALANCE DUE' not present, calculated as `[Agent Comm (NEW 50% RWL 25%)] - [Paid Amount]`.
- Manual Reconcile Table: Obsolete columns ('Math Effect: Commission Paid', 'Math Effect: Agency Commission Received') have been removed.
- Manual Reconcile Table: 'Test Mapping (Preview Manual Reconcile Table)' button shows mapping and preview of manual entries table.
""")
        st.info("To change a formula, edit the relevant function or calculation in the code. If you need help, ask your developer or Copilot.")

    # --- Tools ---
    elif page == "Tools":
        st.subheader("Tools")
        st.info("🚧 Tools page - Stage 6")    # --- Accounting ---
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
                pass  # Ignore if already exists        # --- Load manual entries from DB if session state is empty ---
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
            total_paid = sum(float(row.get("Amount Paid", 0)) for row in st.session_state["manual_commission_rows"])
            total_received = sum(float(row.get("Agency Comm Received (STMT)", 0)) for row in st.session_state["manual_commission_rows"])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Entries", total_entries)
            with col2:
                st.metric("Total Amount Paid", f"${total_paid:,.2f}")
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
                                # Debug: what transaction IDs are we trying to delete?
                        
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
                        key="reconcile_statement_date"
                    )
                with col2:
                    statement_description = st.text_input(
                        "Statement Description (optional)",
                        placeholder="e.g., Monthly Commission Statement - December 2024",
                        key="reconcile_description"                    )
                
                # Calculate totals for the statement
                total_commission_paid = sum(float(row.get("Amount Paid", 0)) for row in st.session_state["manual_commission_rows"])
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
                        # Save to commission_payments table
                        with engine.begin() as conn:
                            conn.execute(sqlalchemy.text('''
                                INSERT INTO commission_payments 
                                (policy_number, customer, payment_amount, statement_date, payment_timestamp, statement_details)
                                VALUES (:policy_number, :customer, :payment_amount, :statement_date, :payment_timestamp, :statement_details)
                            '''), {
                                "policy_number": f"BULK_STATEMENT_{statement_date.strftime('%Y%m%d')}",
                                "customer": statement_description if statement_description else f"Commission Statement - {statement_date.strftime('%m/%d/%Y')}",
                                "payment_amount": total_agency_received,
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
                            
                            # Use centralized mapping to ensure field consistency
                            transaction_id_col = get_mapped_column("Transaction ID")
                            customer_col = get_mapped_column("Customer")
                            policy_type_col = get_mapped_column("Policy Type") 
                            policy_number_col = get_mapped_column("Policy Number")
                            effective_date_col = get_mapped_column("Effective Date")
                            transaction_type_col = get_mapped_column("Transaction Type")
                            stmt_date_col = get_mapped_column("STMT DATE")
                            transaction_date_col = get_mapped_column("Transaction Date")
                            agency_comm_col = get_mapped_column("Agency Comm Received (STMT)")
                            agent_paid_col = get_mapped_column("Agent Paid Amount (STMT)")
                            client_id_col = get_mapped_column("Client ID")
                            
                            # Populate with reconciliation data using flexible transaction types
                            if transaction_id_col:
                                # Generate new unique transaction ID for main DB to avoid conflicts
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
                            if transaction_date_col:
                                new_transaction[transaction_date_col] = statement_date.strftime('%m/%d/%Y')
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

        if selected_policy and selected_policy != "Select...":
            # Get all rows for this policy, using only real database data
            policy_rows = all_data[all_data["Policy Number"] == selected_policy].copy()
            # Define the original ledger columns
            ledger_columns = [
                "Transaction ID",
                "Transaction Date",
                "Description",
                "Credit (Commission Owed)",
                "Debit (Paid to Agent)",
                "Transaction Type"
            ]

            # --- Always include all ledger columns, filling missing with empty values ---            import numpy as np
            if not policy_rows.empty:
                # --- Ledger construction using mapped column names ---
                # Get mapped column names for credits and debits
                credit_col = get_mapped_column("Agent Estimated Comm $") or "Agent Estimated Comm $"
                debit_col = get_mapped_column("Agent Paid Amount (STMT)") or "Agent Paid Amount (STMT)"
                transaction_id_col = get_mapped_column("Transaction ID") or "Transaction ID"
                transaction_date_col = get_mapped_column("Transaction Date") or "Transaction Date"
                stmt_date_col = get_mapped_column("STMT DATE") or "STMT DATE"
                description_col = get_mapped_column("Description") or "Description"
                transaction_type_col = get_mapped_column("Transaction Type") or "Transaction Type"
                
                # Build ledger_df with correct mapping
                ledger_df = pd.DataFrame()
                ledger_df["Transaction ID"] = policy_rows[transaction_id_col] if transaction_id_col in policy_rows.columns else ""
                # Transaction Date: preserve as-is from DB, including blanks/nulls
                # Check for both mapped transaction date columns
                if transaction_date_col in policy_rows.columns:
                    ledger_df["Transaction Date"] = policy_rows[transaction_date_col]
                elif stmt_date_col in policy_rows.columns:
                    ledger_df["Transaction Date"] = policy_rows[stmt_date_col]
                else:
                    ledger_df["Transaction Date"] = ""
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
                # Sort by Transaction Date (oldest first), fallback to index order if not present
                if "Transaction Date" in ledger_df.columns:
                    try:
                        ledger_df = ledger_df.sort_values("Transaction Date", ascending=True)
                    except Exception:
                        ledger_df = ledger_df.copy()
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

                st.markdown("### Policy Ledger (Editable)")

                # --- Ensure Transaction Date is present for all rows, especially the first row ---
                # Only fill with placeholder if the column is missing entirely
                if "Transaction Date" not in ledger_df.columns:
                    ledger_df["Transaction Date"] = ""

                # Ensure Credit and Debit columns are numeric
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
                edited_ledger_df = edited_ledger_df[ledger_columns]

                # --- Test Mapping (Preview Policy Ledger) Button and Expander ---
                if st.button("Test Mapping (Preview Policy Ledger)", key="test_mapping_policy_ledger_btn") or st.session_state.get("show_policy_ledger_mapping_preview", False):
                    st.session_state["show_policy_ledger_mapping_preview"] = True
                    def get_policy_ledger_column_mapping(col, val):
                        mapping = {
                            "Transaction ID": "transaction_id",
                            "Transaction Date": "STMT DATE",  # Maps to STMT DATE in database
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
                    st.rerun()

    # --- Help ---
    elif page == "Help":
        st.subheader("Help & Documentation")
        st.markdown("""
        ### Welcome to the Sales Commission Tracker!
        
        This application helps you manage and track sales commissions for insurance policies. Below is a guide to help you navigate the system:
        
        #### 📊 **Dashboard**
        - View overall metrics and summary statistics
        - Quick client search and edit functionality
        - Total transactions and commission calculations
        
        #### 📝 **Add New Policy Transaction**
        - Add new insurance policies to the database
        - Automatic commission calculation based on policy type and revenue
        - Auto-generated Client ID and Transaction ID
        
        #### 📋 **Reports**
        - Generate customizable reports with selected columns
        - Filter by date ranges and specific criteria
        - Export capabilities for further analysis
        
        #### 📁 **All Policies in Database**
        - View all policies in the system
        - Pagination for easy browsing
        - Quick overview of all transactions
        
        #### ✏️ **Edit Policies in Database**
        - Search and edit existing policies
        - Bulk editing capabilities
        - Real-time updates to the database
        
        #### 🔍 **Search & Filter**
        - Advanced filtering by multiple criteria
        - Search by customer, policy type, carrier, etc.
        - Export filtered results
        
        #### ⚙️ **Admin Panel**
        - Manage database structure and columns
        - Backup and restore functionality
        - Column mapping and customization
        - Formula documentation
        
        #### 💰 **Accounting**
        - Reconcile commission statements
        - Track payments and outstanding balances
        - Manual entry and file upload options
        - Payment history and audit trails
        
        #### 📑 **Policy Revenue Ledger**
        - Detailed ledger view of all transactions
        - Edit individual entries
        - Calculate totals and balances
        - Granular search and filtering
        
        #### 🆘 **Need More Help?**
        - Contact your system administrator
        - Check the documentation files in the project folder
        - Use the debug checkbox in the sidebar for troubleshooting
        """)    # --- Policy Revenue Ledger Reports (Simple Implementation) ---
    elif page == "Policy Revenue Ledger Reports":
        st.subheader("Policy Revenue Ledger Reports")
        st.success("📊 Generate customizable reports for policy summaries with Balance Due calculations and export capabilities.")
        
        # DEBUG: Add diagnostic information
        st.write(f"DEBUG: all_data shape: {all_data.shape}")
        st.write(f"DEBUG: all_data columns: {list(all_data.columns)}")
        st.write(f"DEBUG: all_data empty check: {all_data.empty}")
        
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
            
            st.success("✅ Enhanced Policy Revenue Ledger Reports with Templates & Export Parameters!")    # ============================================================================
    # PHASE 4: RECOVERY SYSTEM & MONITORING
    # Purpose: Comprehensive monitoring, recovery UI, and health checks
    # ============================================================================
    
    def show_protection_status():
        """Show current protection system status."""
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🛡️ Protection Status")
        
        # Check if protection is active
        current_schema = get_current_schema()
        if current_schema:
            st.sidebar.success("✅ Database Protected")
            st.sidebar.write(f"Columns: {len(current_schema)}")
        else:
            st.sidebar.error("❌ Protection Error")
        
        # Show last backup
        backup_files = [f for f in os.listdir(".") if f.startswith("commissions_") and f.endswith(".db")]
        if backup_files:
            latest_backup = max(backup_files, key=os.path.getmtime)
            backup_time = os.path.getmtime(latest_backup)
            backup_time_str = datetime.datetime.fromtimestamp(backup_time).strftime("%m/%d %H:%M")
            st.sidebar.write(f"Latest backup: {backup_time_str}")
        else:
            st.sidebar.write("No backups found")
      # ============================================================================
    # END PHASE 4: RECOVERY SYSTEM & MONITORING
    # ============================================================================
    
    # Show the recovery options UI in the sidebar
    show_protection_status()

# Call main function
main()
