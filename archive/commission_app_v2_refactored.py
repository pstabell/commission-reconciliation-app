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
st.write(':green[App started - debug message]')

def apply_css():
    """Apply custom CSS styling to the Streamlit app."""
    with st.container():
        st.markdown(
            """
            <style>
            /* Remove default padding and maximize main block width */
            .main .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            max-width: 100vw;
            width: 100vw;
        }
        /* Make tables and editors use full width */
        .stDataFrame, .stDataEditor {
            width: 100vw !important;
            min-width: 100vw !important;
        }
        /* Reduce sidebar width slightly for more main area */
        section[data-testid="stSidebar"] {
            min-width: 220px !important;
            max-width: 240px !important;
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
    """Format date columns in MM/DD/YYYY format."""
    date_columns = ["Policy Origination Date", "Effective Date", "X-Date", "X-DATE", "Statement Date", "STMT DATE"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            df[col] = df[col].dt.strftime("%m/%d/%Y")
    return df

CURRENCY_COLUMNS = [
    "Premium Sold",    "Agency Comm Received (STMT)",
    "Gross Premium Paid",
    "Agency Gross Comm",
    "Agent Paid Amount (STMT)",
    "Estimated Agent Comm",
    "Estimated Agent Comm (New 50% Renewal 25%)",
    "Policy Balance Due"  # Updated to use the new calculated column
]

def format_currency_columns(df):
    for col in CURRENCY_COLUMNS:
        if col in df.columns:
            df[col] = df[col].apply(format_currency)
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

    import pdfplumber
    import os
    import json
    import datetime
    import io
    import uuid
    import random
    import string
    import streamlit_sortables as sortables
    import re

    # Apply CSS styling
    apply_css()    # --- Page Selection ---
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
        st.write("Welcome! Use the sidebar to navigate.")

        # --- Client Search & Edit (clean selectbox style) ---
        st.markdown("### Search and Edit a Client")
        if "Customer" in all_data.columns:
            customers = ["Select a client..."] + sorted(all_data["Customer"].dropna().unique().tolist())
            selected_client = st.selectbox("Filter by Customer:", customers)
        else:
            selected_client = None

        if selected_client and selected_client != "Select a client...":
            client_df = all_data[all_data["Customer"].str.strip().str.lower() == selected_client.strip().lower()].reset_index(drop=True)
            st.write(f"Showing policies for **{selected_client}**:")
            
            # --- Calculate PAST DUE for each row ---
            if "Agent Paid Amount (STMT)" in client_df.columns and "Estimated Agent Comm (New 50% Renewal 25%)" in client_df.columns:
                paid_amounts = pd.to_numeric(client_df["Agent Paid Amount (STMT)"], errors="coerce").fillna(0)
                commission_amounts = pd.to_numeric(client_df["Estimated Agent Comm (New 50% Renewal 25%)"], errors="coerce").fillna(0)
                client_df["PAST DUE"] = commission_amounts - paid_amounts
            else:
                st.warning("Missing 'Agent Paid Amount (STMT)' or 'Estimated Agent Comm (New 50% Renewal 25%)' column for PAST DUE calculation.")
            
            # --- Show metrics side by side, spaced in 6 columns, shifted left ---
            col1, col2, col3, col4, col5, col6 = st.columns(6)

            # Move metrics to col2 and col3, leaving col6 open for future data
            with col2:
                if "Agent Paid Amount (STMT)" in client_df.columns:
                    paid_amounts = pd.to_numeric(client_df["Agent Paid Amount (STMT)"], errors="coerce")
                    total_paid = paid_amounts.sum()
                    st.metric(label="Total Paid Amount", value=f"${total_paid:,.2f}")
                else:
                    st.warning("No 'Agent Paid Amount (STMT)' column found for this client.")

            with col3:
                if (
                    "Agent Paid Amount (STMT)" in client_df.columns
                    and "Due Date" in client_df.columns
                    and "Estimated Agent Comm (New 50% Renewal 25%)" in client_df.columns
                ):
                    today = pd.to_datetime(datetime.datetime.today())
                    due_dates = pd.to_datetime(client_df["Due Date"], errors="coerce")
                    paid_amounts = pd.to_numeric(client_df["Agent Paid Amount (STMT)"], errors="coerce").fillna(0)
                    commission_amounts = pd.to_numeric(client_df["Estimated Agent Comm (New 50% Renewal 25%)"], errors="coerce").fillna(0)
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
                st.session_state["premium_sold_input_live"] = premium_sold_calc

        # --- Live Premium Sold and Agency Revenue outside the form ---
        if "premium_sold_input" not in st.session_state:
            st.session_state["premium_sold_input"] = 0.0
        st.subheader("Enter Premium Sold and see Agency Revenue:")
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
                    "Agent Paid Amount (STMT)",
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
                agent_comm_pct = new_row.get("Agent Comm (New 50% RWL 25%)", 0)
                p = parse_money(premium)
                pc = parse_percent(pct)
                ac = parse_percent(agent_comm_pct)
                new_row["Agent Estimated Comm $"] = p * (pc / 100.0) * (ac / 100.0)
            
            # Note: Policy Balance Due is now calculated dynamically in reports, 
            # not stored in the database
            
            new_df = pd.DataFrame([new_row])
            new_df.to_sql('policies', engine, if_exists='append', index=False)
            st.success("New policy transaction added!")
            st.rerun()    # --- Reports ---
    elif page == "Reports":
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
            report_df = all_data[selected_columns]

        # --- Optional: Filter by Customer ---
        if "Customer" in all_data.columns:
            st.markdown("**Filter by Customer:**")
            customers = ["All"] + sorted(all_data["Customer"].dropna().unique().tolist())
            selected_customer = st.selectbox("Customer", customers)
            if selected_customer != "All":
                report_df = report_df[report_df["Customer"] == selected_customer]

        # --- Policy Balance Due dropdown filter ---
        balance_due_options = ["All", "YES", "NO"]
        selected_balance_due = st.selectbox("Policy Balance Due", balance_due_options)
        
        # Calculate Policy Balance Due if not present (using correct column names)
        if "Policy Balance Due" not in report_df.columns and "Agent Paid Amount (STMT)" in report_df.columns and "Agent Estimated Comm $" in report_df.columns:
            paid_amounts = pd.to_numeric(report_df["Agent Paid Amount (STMT)"], errors="coerce").fillna(0)
            commission_amounts = pd.to_numeric(report_df["Agent Estimated Comm $"], errors="coerce").fillna(0)
            report_df["Policy Balance Due"] = commission_amounts - paid_amounts
        
        # Ensure Policy Balance Due is numeric for filtering
        if "Policy Balance Due" in report_df.columns:
            report_df["Policy Balance Due"] = pd.to_numeric(report_df["Policy Balance Due"], errors="coerce").fillna(0)
        
        # Apply Balance Due filter
        if selected_balance_due != "All" and "Policy Balance Due" in report_df.columns:
            if selected_balance_due == "YES":
                report_df = report_df[report_df["Policy Balance Due"] > 0]
            elif selected_balance_due == "NO":
                report_df = report_df[report_df["Policy Balance Due"] <= 0]

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
        st.info("Tip: Use your browser's zoom-out (Ctrl -) to see more columns. Scroll horizontally for wide tables.")
        # Reduce the height so the table fits better on the page and horizontal scroll bar is visible
        st.dataframe(format_currency_columns(format_dates_mmddyyyy(all_data)), use_container_width=True, height=350)    # --- Edit Policies in Database ---
    elif page == "Edit Policies in Database":
        st.subheader("Edit Policies in Database")
        db_columns = all_data.columns.tolist()
        st.markdown("**Reorder columns by dragging the boxes below (no delete):**")
        order = streamlit_sortables.sort_items(
            items=db_columns,
            direction="horizontal",
            key="edit_db_col_order_sortable"
        )
        # --- Lock formula columns in the data editor ---
        lock_cols = [
            col for col in db_columns if col.strip().lower() in [
                "agent estimated comm $", "agency estimated comm/revenue (crm)", "agency estimated comm/revenue (az)"
            ]
        ]
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
            # --- Recalculate Agent Estimated Comm $ for all rows before saving ---
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
            # Recalculate Agency Estimated Comm/Revenue (CRM)
            agency_est_comm_col = next((col for col in edited_db_df.columns if col.strip().lower() in ["agency estimated comm/revenue (crm)", "agency estimated comm/revenue (az)"]), None)
            premium_col = next((col for col in edited_db_df.columns if col.strip().lower() == "premium sold".lower()), None)
            gross_comm_col = next((col for col in edited_db_df.columns if col.strip().lower() == "policy gross comm %".lower()), None)
            if agency_est_comm_col and premium_col and gross_comm_col:
                edited_db_df[agency_est_comm_col] = edited_db_df.apply(
                    lambda row: parse_money_bd(row[premium_col]) * (parse_percent_bd(row[gross_comm_col]) / 100.0), axis=1
                )
                st.info(f"Recalculated '{agency_est_comm_col}' for all rows.")
            else:
                st.warning("Could not find all required columns for Agency Estimated Comm/Revenue (CRM) recalculation.")
            # Recalculate Agent Estimated Comm $
            agent_est_comm_col = next((col for col in edited_db_df.columns if col.strip().lower() == "agent estimated comm $".lower()), None)
            agent_comm_pct_col = next(
                (col for col in edited_db_df.columns if col.strip().lower() in ["agent comm (new 50% rwl 25%)", "agent comm (new 50% rwl 25%) (%)"]),
                None
            )
            if agent_est_comm_col and premium_col and gross_comm_col and agent_comm_pct_col:
                edited_db_df[agent_est_comm_col] = edited_db_df.apply(
                    lambda row: parse_money_bd(row[premium_col]) * (parse_percent_bd(row[gross_comm_col]) / 100.0) * (parse_percent_bd(row[agent_comm_pct_col]) / 100.0), axis=1
                )
                st.info(f"Recalculated '{agent_est_comm_col}' for all rows.")
            else:                st.warning("Could not find all required columns for Agent Estimated Comm $ recalculation.")
            
            # Note: Policy Balance Due is now calculated dynamically in reports,
            # not stored in the database, so no recalculation needed here
            
            edited_db_df.to_sql('policies', engine, if_exists='replace', index=False)
            import time
            time.sleep(0.5)  # Give DB a moment to update
            all_data = pd.read_sql('SELECT * FROM policies', engine)
            st.success("Database updated with your edits and new column order! Data reloaded.")
            st.rerun()    # --- Search & Filter ---
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

        # --- One-at-a-time, foolproof mapping editor ---
        st.subheader("Edit Column Mapping (One at a Time)")
        db_columns = all_data.columns.tolist()
        mapping_locked_file = "column_mapping.locked"
        mapping_locked = os.path.exists(mapping_locked_file)
        admin_override = st.checkbox("Admin Override (Unlock Mapping)", value=False, key="admin_override_mapping")
        if mapping_locked and not admin_override:
            st.warning("Column mapping is locked after first use. Enable Admin Override to make changes.")
        else:
            # Show mapping table with edit buttons
            edit_col = st.selectbox("Select UI Field to Edit", [col for col in default_columns], key="edit_mapping_select")
            current_mapping = column_mapping.get(edit_col, "(Not Mapped)")
            st.write(f"**Current Mapping for '{edit_col}':** {current_mapping}")
            # Only allow DB columns not already mapped, or mark as calculated/virtual
            already_mapped = set(column_mapping.values())
            available_db_cols = [col for col in db_columns if col not in already_mapped or col == current_mapping]
            options = ["(Calculated/Virtual)"] + available_db_cols
            new_mapping = st.selectbox(f"Map '{edit_col}' to:", options, index=options.index(current_mapping) if current_mapping in options else 0, key="edit_mapping_new")
            # Show preview of proposed mapping
            proposed_mapping = column_mapping.copy()
            if new_mapping == "(Calculated/Virtual)":
                if edit_col in proposed_mapping:
                    proposed_mapping.pop(edit_col)
            else:
                proposed_mapping[edit_col] = new_mapping
            st.markdown("**Proposed Mapping:**")
            preview_df = pd.DataFrame(list(proposed_mapping.items()), columns=["App Field", "Mapped To"])
            st.dataframe(preview_df, use_container_width=True)
            # Check for one-to-one mapping
            if len(set(proposed_mapping.values())) < len(proposed_mapping.values()):
                st.error("Duplicate database column mapping detected! Each UI field must map to a unique DB column.")
            unmapped = [col for col in default_columns if col not in proposed_mapping]
            if unmapped:
                st.warning(f"Unmapped UI fields: {', '.join(unmapped)}. Mark as Calculated/Virtual if not needed.")
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
                if len(set(proposed_mapping.values())) < len(proposed_mapping.values()):
                    st.error("Cannot save: Duplicate database column mapping detected!")
                elif unmapped:
                    st.error("Cannot save: All UI fields must be mapped or marked as Calculated/Virtual.")
                else:
                    # Save mapping
                    with open(mapping_file, "w") as f:
                        json.dump(proposed_mapping, f)
                    st.success("Mapping updated!")
                    # Lock mapping if not admin override
                    if not admin_override:
                        with open(mapping_locked_file, "w") as f:
                            f.write("locked")
                    st.rerun()

        # --- Column mapping customization as before ---
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
                for col in default_columns:
                    current_mapping_val = column_mapping.get(col)
                    if isinstance(current_mapping_val, str) and current_mapping_val is not None and current_mapping_val in uploaded_columns:
                        idx = uploaded_columns.index(current_mapping_val) + 1
                    else:
                        idx = 0
                    mapped = st.selectbox(
                        f"Map '{col}' to uploaded column:",
                        options=[""] + uploaded_columns,
                        index=idx,
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

        # --- Header renaming section ---
        st.subheader("Rename Database Column Headers")
        db_columns = all_data.columns.tolist()
        with st.form("rename_single_header_form"):
            col_to_rename = st.selectbox("Select column to rename", [""] + db_columns, index=0, key="rename_col_select")
            suggested_new_name = "Agency Estimated Comm/Revenue (CRM)" if col_to_rename == "Agency Estimated Comm/Revenue (AZ)" else ""
            new_col_name = st.text_input("New column name", value=suggested_new_name, key="rename_col_new_name")
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

        # --- Publish Offline Changes Section ---
        st.markdown("---")
        st.subheader("Publish Offline Changes")
        st.info("If you have edited the backup database file (`commissions_backup.db`) offline, click the button below to publish those changes to the live database. This will overwrite all current data in the hosted database (`commissions.db`). **This action cannot be undone!** Make sure you have a backup if needed.")

        # Load last publish time from backup log
        publish_log_path = "commissions_backup_log.json"
        last_publish_time = None
        if os.path.exists(publish_log_path):
            try:
                with open(publish_log_path, "r") as f:
                    publish_log = json.load(f)
                    last_publish_time = publish_log.get("last_publish_time")
            except Exception:
                last_publish_time = None

        col1, col2 = st.columns([2, 3])
        with col1:
            if st.button("Publish Offline Changes (Replace Live Database with Backup)", key="publish_offline_changes"):
                import shutil
                try:
                    shutil.copyfile(backup_path, "commissions.db")
                    # Save publish timestamp in US/Eastern
                    try:
                        import pytz
                        eastern = pytz.timezone("US/Eastern")
                        now_eastern = datetime.datetime.now(eastern)
                    except ImportError:
                        now_eastern = datetime.datetime.now()
                    now_str = now_eastern.strftime("%m/%d/%Y %I:%M:%S %p %Z")
                    # Update log file
                    publish_log = {}
                    if os.path.exists(publish_log_path):
                        try:
                            with open(publish_log_path, "r") as f:
                                publish_log = json.load(f)
                        except Exception:
                            publish_log = {}
                    publish_log["last_publish_time"] = now_str
                    with open(publish_log_path, "w") as f:
                        json.dump(publish_log, f)
                    st.success("Offline changes published! The live database has been replaced with the backup.")
                    # Optionally reload data
                    all_data = pd.read_sql('SELECT * FROM policies', engine)
                    last_publish_time = now_str
                except Exception as e:
                    st.error(f"Failed to publish offline changes: {e}")
        with col2:
            if last_publish_time:
                st.info(f"Last published: {last_publish_time}")
            else:
                st.info("No publish action has been performed yet.")

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
                        key="reconcile_description"
                    )
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
                                "Policy Number": row.get("Policy Number", ""),                                "Effective Date": row.get("Effective Date", ""),
                                "Transaction Type": row.get("Transaction Type", ""),
                                "Commission Paid": row.get("Amount Paid", 0),
                                "Agency Comm Received (STMT)": row.get("Agency Comm Received (STMT)", 0),
                                "Client ID": row.get("Client ID", ""),
                                "Transaction ID": row.get("Transaction ID", "")
                            })
                        
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
                                    "transaction_type": row.get("Transaction Type", ""),                                    "commission_paid": float(row.get("Amount Paid", 0)),
                                    "agency_commission_received": float(row.get("Agency Comm Received (STMT)", 0)),
                                    "statement_date": statement_date.strftime('%Y-%m-%d')
                                })
                        
                        # Clear the manual entries after successful reconciliation
                        st.session_state["manual_commission_rows"] = []
                        
                        st.success(f"✅ Commission statement reconciled and saved to history! Statement date: {statement_date.strftime('%m/%d/%Y')}")
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

            # --- Always include all ledger columns, filling missing with empty values ---
            import numpy as np
            if not policy_rows.empty:
                # --- Ledger construction using correct formula columns ---
                # Always use Agent Estimated Comm $ for Credit (Commission Owed) and Agent Paid Amount (STMT) for Debit (Paid to Agent)
                # If these columns are missing, fill with blank/zero
                credit_col = "Agent Estimated Comm $"
                debit_col = "Agent Paid Amount (STMT)"
                
                # Build ledger_df with correct mapping
                ledger_df = pd.DataFrame()
                ledger_df["Transaction ID"] = policy_rows["Transaction ID"] if "Transaction ID" in policy_rows.columns else ""
                # Transaction Date: preserve as-is from DB, including blanks/nulls
                # Check for both "Transaction Date" and "STMT DATE" columns
                if "Transaction Date" in policy_rows.columns:
                    ledger_df["Transaction Date"] = policy_rows["Transaction Date"]
                elif "STMT DATE" in policy_rows.columns:
                    ledger_df["Transaction Date"] = policy_rows["STMT DATE"]
                else:
                    ledger_df["Transaction Date"] = ""
                ledger_df["Description"] = policy_rows["Description"] if "Description" in policy_rows.columns else ""
                
                # Credit (Commission Owed) from Agent Estimated Comm $
                if credit_col in policy_rows.columns:
                    ledger_df["Credit (Commission Owed)"] = policy_rows[credit_col]
                else:
                    ledger_df["Credit (Commission Owed)"] = 0.0
                # Debit (Paid to Agent) from Agent Paid Amount (STMT)
                if debit_col in policy_rows.columns:
                    ledger_df["Debit (Paid to Agent)"] = policy_rows[debit_col]
                else:
                    ledger_df["Debit (Paid to Agent)"] = 0.0
                ledger_df["Transaction Type"] = policy_rows["Transaction Type"] if "Transaction Type" in policy_rows.columns else ""
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
                # Show policy-level details (single row, editable)
                policy_detail_cols = [
                    c for c in [
                        "Customer", "Client ID", "Policy Number", "Policy Type", "Carrier Name", 
                        "Effective Date", "Policy Origination Date", "Policy Gross Comm %", 
                        "Agent Comm (NEW 50% RWL 25%)", "X-DATE"
                    ] if c in policy_rows.columns
                ]
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
        - Use the debug checkbox in the sidebar for troubleshooting        """)    # --- Policy Revenue Ledger Reports (Simple Implementation) ---
    elif page == "Policy Revenue Ledger Reports":
        st.subheader("Policy Revenue Ledger Reports")
        st.info("🚧 Customizable reports for policy summaries with Balance Due calculations.")
        
        if all_data.empty:
            st.warning("No policy data loaded. Please check database connection or import data.")
        else:
            # Simple data processing - AGGREGATE BY POLICY NUMBER
            # This ensures one row per policy with totals from all transactions
            working_data = all_data.copy()
            
            # Group by Policy Number and aggregate the data
            if "Policy Number" in working_data.columns and not working_data.empty:
                # Define aggregation rules
                agg_dict = {}
                
                # For descriptive fields, take the first value (they should be the same for all transactions of the same policy)
                descriptive_fields = ["Customer", "Policy Type", "Carrier Name", "Effective Date", 
                                    "Policy Origination Date", "X-DATE", "Client ID"]
                for field in descriptive_fields:
                    if field in working_data.columns:
                        agg_dict[field] = 'first'
                
                # For monetary fields, sum all transactions for each policy
                monetary_fields = ["Agent Estimated Comm $", "Agent Paid Amount (STMT)", 
                                 "Agency Revenue", "Premium Sold", "Policy Gross Comm %"]
                for field in monetary_fields:
                    if field in working_data.columns:
                        # Convert to numeric first, then sum
                        working_data[field] = pd.to_numeric(working_data[field], errors='coerce').fillna(0)
                        agg_dict[field] = 'sum'
                
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
                    financial_cols = ["Customer", "Policy Number", "Agency Revenue", "Agent Estimated Comm $", "Agent Paid Amount (STMT)", "Policy Balance Due"]
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
                    st.caption(caption_text)
                      # Enhanced export with custom filename
                    export_col1, export_col2, export_col3 = st.columns(3)
                    with export_col1:
                        custom_filename = st.text_input(
                            "Custom Export Filename (optional)",
                            placeholder="Leave blank for auto-generated name"
                        )
                    
                    with export_col2:
                        filename = custom_filename if custom_filename else f"policy_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        csv_filename = filename if filename.endswith('.csv') else filename + '.csv'
                        
                        csv_data = working_data[valid_columns].to_csv(index=False)
                        st.download_button(
                            "📄 Export Selected Columns as CSV",
                            csv_data,
                            csv_filename,
                            "text/csv"
                        )
                    
                    with export_col3:
                        excel_filename = filename if filename.endswith('.xlsx') else filename + '.xlsx'
                        
                        # Create Excel file in memory
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                            working_data[valid_columns].to_excel(writer, sheet_name='Policy Revenue Report', index=False)
                        excel_buffer.seek(0)
                        
                        st.download_button(
                            "� Export All Rows as Excel",
                            excel_buffer.getvalue(),
                            excel_filename,
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                else:
                    st.warning("Selected columns are not available in the current data.")
            else:
                if not selected_columns:
                    st.info("Please select columns to display the report.")
                else:
                    st.warning("No data available for report generation.")
            
            st.success("✅ Enhanced Policy Revenue Ledger Reports with Templates!")

    # --- DEBUG: Fallback UI if page is not handled
    else:
        st.warning(f"Page '{page}' is not yet implemented in the refactored version.")

# Call main function
main()
