import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
import pdfplumber
import os
import json
import sqlalchemy
import datetime
import io
import uuid
import random
import string
import streamlit_sortables as sortables

# --- Aggressive but safe CSS to maximize app/table/table width and make scrollbars fatter ---
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

# --- Utility: Format all date columns as MM/DD/YYYY for display ---
def format_dates_mmddyyyy(df):
    date_cols = [col for col in df.columns if "date" in col.lower() or col.lower() in ["x-date", "xdate"]]
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%m/%d/%Y")
        except Exception:
            pass
    return df

def format_currency(val):
    try:
        val = float(val)
        return f"${val:,.2f}"
    except (ValueError, TypeError):
        return val

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

st.title("Sales Commission Tracker")  # Changed title here

# --- Sidebar Navigation ---
show_debug = st.sidebar.checkbox("Show Debug Info", value=False)
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Reports",
        "All Policies in Database",
        "Edit Policies in Database",  # Moved up
        "Add New Policy Transaction",
        "Upload & Reconcile",
        "Search & Filter",
        "Admin Panel",
        "Accounting",
        "Help"
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
    # Add more mappings as needed
}
all_data.rename(columns=rename_dict, inplace=True)

if show_debug:
    st.write("DEBUG: all_data shape:", all_data.shape)
    st.write("DEBUG: all_data columns:", all_data.columns.tolist())
    st.write("DEBUG: page selected:", page)
    st.dataframe(format_currency_columns(all_data))

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
        if "Paid Amount" in client_df.columns and "Estimated Agent Comm (New 50% Renewal 25%)" in client_df.columns:
            paid_amounts = pd.to_numeric(client_df["Paid Amount"], errors="coerce").fillna(0)
            commission_amounts = pd.to_numeric(client_df["Estimated Agent Comm (New 50% Renewal 25%)"], errors="coerce").fillna(0)
            client_df["PAST DUE"] = commission_amounts - paid_amounts
        else:
            st.warning("Missing 'Paid Amount' or 'Estimated Agent Comm (New 50% Renewal 25%)' column for PAST DUE calculation.")

        # --- Show metrics side by side, spaced in 6 columns, shifted left ---
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        # Move metrics to col2 and col3, leaving col6 open for future data
        with col2:
            if "Paid Amount" in client_df.columns:
                paid_amounts = pd.to_numeric(client_df["Paid Amount"], errors="coerce")
                total_paid = paid_amounts.sum()
                st.metric(label="Total Paid Amount", value=f"${total_paid:,.2f}")
            else:
                st.warning("No 'Paid Amount' column found for this client.")

        with col3:
            if (
                "Paid Amount" in client_df.columns
                and "Due Date" in client_df.columns
                and "Estimated Agent Comm (New 50% Renewal 25%)" in client_df.columns
            ):
                today = pd.to_datetime(datetime.date.today())
                due_dates = pd.to_datetime(client_df["Due Date"], errors="coerce")
                paid_amounts = pd.to_numeric(client_df["Paid Amount"], errors="coerce").fillna(0)
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
            st.success("Client data updated!")

# --- Reports ---
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
        new_df = pd.DataFrame([new_row])
        new_df.to_sql('policies', engine, if_exists='append', index=False)
        st.success("New policy transaction added!")

# --- Upload & Reconcile ---
elif page == "Upload & Reconcile":
    st.subheader("Upload and Reconcile Data")
    uploaded_file = st.file_uploader(
        "Upload your sales commission spreadsheet or PDF report",
        type=["xlsx", "xls", "csv", "pdf"]
    )
    pdf_type = None
    if uploaded_file and uploaded_file.name.endswith(".pdf"):
        pdf_type = st.radio(
            "What type of PDF are you uploading?",
            ("Sales Report (A-I only)", "Commission Statement (all columns)")
        )
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
        if pdf_type == "Sales Report (A-I only)":
            df = df.iloc[:, :9]
            df["NEW/RWL"] = "NEW"
        st.write("Extracted DataFrame preview:", format_dates_mmddyyyy(df.head(5)))
        header_row = st.number_input(
            "Which row contains the column headers? (0 = first row)", min_value=0, max_value=min(10, len(df)-1), value=0
        )
        df.columns = df.iloc[header_row]
        df = df[(header_row+1):].reset_index(drop=True)
        df.columns = df.columns.str.strip()
        st.write("Columns after header set:", df.columns.tolist())
        st.write(format_dates_mmddyyyy(df.head()))
        df.columns = df.columns.str.strip()
        st.write("Columns found:", df.columns.tolist())
        mapping_file = "column_mapping.json"
        default_columns = [
            "Customer", "Policy Type", "Carrier Name", "Policy Number", "NEW/RWL",
            "Agency Revenue", "Policy Origination Date", "Effective Date"
        ]
        if os.path.exists(mapping_file):
            with open(mapping_file, "r") as f:
                column_mapping = json.load(f)
        else:
            column_mapping = {}
        uploaded_columns = df.columns.tolist()
        mapped_columns = []
        for col in default_columns:
            mapped = column_mapping.get(col)
            if mapped not in uploaded_columns:
                mapped = st.selectbox(
                    f"Map '{col}' to uploaded column:",
                    options=[""] + uploaded_columns,
                    key=f"map_{col}"
                )
            mapped_columns.append(mapped or col)
        if st.button("Save column mapping for future uploads"):
            for i, col in enumerate(default_columns):
                column_mapping[col] = mapped_columns[i]
            with open(mapping_file, "w") as f:
                json.dump(column_mapping, f)
            st.success("Column mapping saved!")
        df = df.rename(columns={v: k for k, v in column_mapping.items() if v in df.columns})
        if pdf_type == "Sales Report (A-I only)":
            for col in ["Agency Revenue", "Policy Origination Date", "Effective Date"]:
                if col not in df.columns:
                    df[col] = ""
        required_columns = ["NEW/RWL", "Agency Revenue", "Policy Origination Date", "Effective Date"]
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            st.error(f"Missing columns: {missing}")
            st.stop()
        df["Calculated Commission"] = df.apply(calculate_commission, axis=1)
        st.subheader("Edit Data")
        edited_df = st.data_editor(format_dates_mmddyyyy(df))
        st.subheader("Download Results")
        st.download_button(
            label="Download as CSV",
            data=edited_df.to_csv(index=False),
            file_name="reconciled_commissions.csv",
            mime="text/csv"
        )
        # --- Download as Excel ---
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            edited_df.to_excel(writer, index=False, sheet_name='Reconciled Commissions')
        st.download_button(
            label="Download Report as Excel",
            data=output.getvalue(),
            file_name="reconciled_commissions.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        if st.button("Save to Database"):
            edited_df.to_sql('policies', engine, if_exists='append', index=False)
            st.success("Data saved to database!")

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
        edited_db_df.to_sql('policies', engine, if_exists='replace', index=False)
        st.success("Database updated with your edits and new column order!")

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
                        commission_paid = st.number_input("Commission Paid", min_value=0.0, step=0.01, format="%.2f", key="recon_comm_paid_input")
                        agency_comm_received = st.number_input("Agency Commission Received $", min_value=0.0, step=0.01, format="%.2f", key="recon_agency_comm_received_input")
                        statement_date = st.date_input("Statement Date", value=None, format="MM/DD/YYYY", key="recon_stmt_date_input")
                        if st.button("Add Entry", key="recon_add_entry_btn"):
                            # Force Statement Date to MM/DD/YYYY string or blank
                            if statement_date is None or statement_date == "":
                                stmt_date_str = ""
                            elif isinstance(statement_date, datetime.date):
                                stmt_date_str = statement_date.strftime("%m/%d/%Y")
                            else:
                                try:
                                    stmt_date_str = pd.to_datetime(statement_date).strftime("%m/%d/%Y")
                                except Exception:
                                    stmt_date_str = ""
                            # Add entry to session state (now includes Transaction Type)
                            st.session_state["manual_commission_rows"].append({
                                "Customer": selected_customer,
                                "Policy Type": selected_policy_type,
                                "Policy Number": selected_policy_number,
                                "Effective Date": selected_effective_date,
                                "Transaction Type": transaction_type,
                                "Commission Paid": commission_paid,
                                "Agency Commission Received $": agency_comm_received,
                                "Statement Date": stmt_date_str
                            })
                            st.success("Entry added. You can review and edit below.")

    # --- Show, edit, and delete manual entries ---
    if st.session_state["manual_commission_rows"]:
        # Always display Statement Date as MM/DD/YYYY or blank
        display_rows = []
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
            # Ensure Agency Commission Received $ is present for all rows
            if "Agency Commission Received $" not in display_row:
                display_row["Agency Commission Received $"] = 0.0
            # Ensure Transaction Type is present for all rows (for legacy rows)
            if "Transaction Type" not in display_row:
                display_row["Transaction Type"] = ""
            display_rows.append(display_row)
        df_manual = pd.DataFrame(display_rows)
        # Move 'Delete' column to the first position
        cols = df_manual.columns.tolist()
        if 'Delete' in cols:
            cols.insert(0, cols.pop(cols.index('Delete')))
            df_manual = df_manual[cols]
        edited_df = st.data_editor(df_manual, use_container_width=True, key="manual_comm_rows_editor")

        # --- Show totals row at the bottom ---
        if not df_manual.empty:
            # Only sum numeric columns
            numeric_cols = [col for col in df_manual.columns if df_manual[col].dtype in [float, int] or pd.api.types.is_numeric_dtype(df_manual[col])]
            # Exclude 'Delete' column from totals
            numeric_cols = [col for col in numeric_cols if col != 'Delete']
            totals = {col: df_manual[col].apply(pd.to_numeric, errors='coerce').sum() for col in numeric_cols}
            # Build a totals row with blank for non-numeric columns
            totals_row = {col: (totals[col] if col in totals else "") for col in df_manual.columns}
            # Label the first non-delete column as 'TOTAL'
            for col in df_manual.columns:
                if col != 'Delete':
                    totals_row[col] = 'TOTAL'
                    break
            # Show totals row below the table
            st.markdown("**Totals for all manual entries below:**")
            st.dataframe(pd.DataFrame([totals_row]), use_container_width=True, height=50)

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

        # --- Clear manual entries ---
        if st.button("Clear Manual Entries", key="clear_manual_entries_btn"):
            st.session_state["manual_commission_rows"] = []
            st.success("All manual entries cleared.")

        # --- Use manual entries for reconciliation ---
        if st.button("Use Manual Entries for Reconciliation", key="use_manual_entries_btn"):
            st.session_state["reconcile_with_manual_entries"] = True
            st.success("Manual entries ready for reconciliation.")

        # --- Payment/Reconciliation History Viewer ---
        st.markdown("---")
        st.markdown("### Payment/Reconciliation History")
        payment_history = pd.read_sql('SELECT * FROM commission_payments ORDER BY payment_timestamp DESC', engine)
        if not payment_history.empty:
            payment_history["statement_date"] = pd.to_datetime(payment_history["statement_date"], errors="coerce").dt.strftime("%m/%d/%Y").fillna("")
            payment_history["payment_timestamp"] = pd.to_datetime(payment_history["payment_timestamp"], errors="coerce").dt.strftime("%m/%d/%Y %I:%M %p").fillna("")
            st.dataframe(payment_history, use_container_width=True, height=250)
        else:
            st.info("No payment/reconciliation history found.")
