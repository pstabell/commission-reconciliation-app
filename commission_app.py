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

# --- Aggressive but safe CSS to maximize app/table width and make scrollbars fatter ---
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
    st.dataframe(all_data)

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

    # --- Past Due dropdown filter ---
    past_due_options = ["All", "YES", "NO"]
    selected_past_due = st.selectbox("Past Due", past_due_options)
    # Calculate PAST DUE if not present
    if "PAST DUE" not in report_df.columns and "Paid Amount" in report_df.columns and "Estimated Agent Comm (New 50% Renewal 25%)" in report_df.columns:
        paid_amounts = pd.to_numeric(report_df["Paid Amount"], errors="coerce").fillna(0)
        commission_amounts = pd.to_numeric(report_df["Estimated Agent Comm (New 50% Renewal 25%)"], errors="coerce").fillna(0)
        report_df["PAST DUE"] = commission_amounts - paid_amounts
    # Apply Past Due filter
    if selected_past_due != "All" and "PAST DUE" in report_df.columns:
        if selected_past_due == "YES":
            report_df = report_df[report_df["PAST DUE"] > 0]
        elif selected_past_due == "NO":
            report_df = report_df[report_df["PAST DUE"] <= 0]

    st.markdown("**Report Preview:**")
    st.dataframe(format_dates_mmddyyyy(report_df), use_container_width=True, height=max(400, 40 + 40 * len(report_df)))

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
    st.dataframe(format_dates_mmddyyyy(all_data), use_container_width=True, height=900)

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
    edited_db_df = st.data_editor(format_dates_mmddyyyy(all_data.reset_index(drop=True)))
    if st.button("Update Database with Edits"):
        edited_db_df.to_sql('policies', engine, if_exists='replace', index=False)
        st.success("Database updated with your edits!")

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
        /* Highlight the selectbox for 'Past Due' */
        div[data-testid="stSelectbox"]:has(label:contains('Past Due')) > div[data-baseweb="select"] {
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

    # Dropdown to filter by Past Due status
    past_due_options = ["All", "YES", "NO"]
    selected_past_due = st.selectbox("Past Due", past_due_options)

    filtered_data = all_data.copy()

    # Apply search filter
    if search_text:
        filtered_data = filtered_data[filtered_data[search_column].astype(str).str.contains(search_text, case=False, na=False)]

    # Calculate PAST DUE if not present
    if "PAST DUE" not in filtered_data.columns and "Paid Amount" in filtered_data.columns and "Estimated Agent Comm (New 50% Renewal 25%)" in filtered_data.columns:
        paid_amounts = pd.to_numeric(filtered_data["Paid Amount"], errors="coerce").fillna(0)
        commission_amounts = pd.to_numeric(filtered_data["Estimated Agent Comm (New 50% Renewal 25%)"], errors="coerce").fillna(0)
        filtered_data["PAST DUE"] = commission_amounts - paid_amounts

    # Apply Past Due filter
    if selected_past_due != "All" and "PAST DUE" in filtered_data.columns:
        if selected_past_due == "YES":
            filtered_data = filtered_data[filtered_data["PAST DUE"] > 0]
        elif selected_past_due == "NO":
            filtered_data = filtered_data[filtered_data["PAST DUE"] <= 0]

    st.subheader("Filtered Policies")
    st.dataframe(format_dates_mmddyyyy(filtered_data), use_container_width=True, height=400)  # Increased height so first row is always visible

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
        col_to_delete = st.selectbox("Select column to delete", db_columns)
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

    # --- Reorder Columns Section ---
    st.subheader("Reorder Database Columns")
    db_columns = all_data.columns.tolist()
    new_order = []
    remaining_cols = db_columns.copy()
    for i in range(len(db_columns)):
        col = st.selectbox(
            f"Column for position {i+1}",
            options=remaining_cols,
            key=f"reorder_col_{i}"
        )
        new_order.append(col)
        remaining_cols.remove(col)

    if st.button("Apply New Column Order"):
        if set(new_order) == set(db_columns):
            with engine.begin() as conn:
                df_temp = pd.read_sql('SELECT * FROM policies', conn)
                df_temp = df_temp[new_order]
                conn.execute(sqlalchemy.text('ALTER TABLE policies RENAME TO policies_old'))
                df_temp.to_sql('policies', engine, if_exists='replace', index=False)
                conn.execute(sqlalchemy.text('DROP TABLE policies_old'))
            st.success("Column order updated.")
            st.rerun()
        else:
            st.warning("Please include all columns in the new order.")

    # --- Header renaming section (at the bottom) ---
    st.subheader("Rename Database Column Headers")
    new_headers = {}
    with st.form("rename_headers_form"):
        for col in db_columns:
            new_name = st.text_input(f"Rename '{col}' to:", value=col, key=f"rename_{col}")
            new_headers[col] = new_name
        submitted = st.form_submit_button("Rename Columns")

    if submitted:
        # Only rename if the name actually changed
        rename_dict = {old: new for old, new in new_headers.items() if old != new and new}
        if rename_dict:
            with engine.begin() as conn:
                for old, new in rename_dict.items():
                    conn.execute(sqlalchemy.text(f'ALTER TABLE policies RENAME COLUMN \"{old}\" TO \"{new}\"'))
            st.success(f"Renamed columns: {rename_dict}")
            st.rerun()
        else:
            st.info("No changes made to column names.")

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

# --- Accounting ---
elif page == "Accounting":
    st.subheader("Commission Reconciliation")

    st.markdown("""
    **Review all policies with a nonzero PAST DUE balance.**
    - Only policies with a PAST DUE amount not equal to $0.00 are shown.
    """)

    # Calculate PAST DUE if not present
    if "PAST DUE" not in all_data.columns and "Paid Amount" in all_data.columns and "Estimated Agent Comm (New 50% Renewal 25%)" in all_data.columns:
        paid_amounts = pd.to_numeric(all_data["Paid Amount"], errors="coerce").fillna(0)
        commission_amounts = pd.to_numeric(all_data["Estimated Agent Comm (New 50% Renewal 25%)"], errors="coerce").fillna(0)
        all_data["PAST DUE"] = commission_amounts - paid_amounts

    if "PAST DUE" in all_data.columns:
        past_due_numeric = pd.to_numeric(all_data["PAST DUE"], errors="coerce").fillna(0)
        nonzero_df = all_data[past_due_numeric.abs() > 0.01].copy()
        st.dataframe(format_dates_mmddyyyy(nonzero_df), use_container_width=True, height=max(400, 40 + 40 * len(nonzero_df)))
        total_past_due = past_due_numeric[past_due_numeric.abs() > 0.01].sum()
        st.metric("Total PAST DUE", f"${total_past_due:,.2f}")
        st.info("Only policies with a nonzero PAST DUE balance are shown.")
    else:
        st.warning("No 'PAST DUE' column found or not enough data to calculate it.")

# --- Help ---
elif page == "Help":
    with st.expander("❓ Help / Instructions", expanded=True):
        st.markdown("""
### How to Use This App

**For code backup & restore instructions, see the `GIT_GUIDE.md` file in your project folder.**

**1. Dashboard (Home Page)**
- See total policies and total commissions.
- Search for a client using a clean dropdown (Filter by Customer).
- View and edit all policies for a selected client, with a blank row at the bottom to add endorsements or new transactions.
- "Total Paid Amount" and "Total Past Due" are shown side by side at the top for the selected client.
- "Total Past Due" now reflects the true balance due for all overdue, underpaid policies.
- Click "Update This Client's Data" to save any changes or new entries for that client.

**2. Reports**
- Create customizable reports by selecting columns, filtering by any available date column (including X-DATE), and filtering by customer.
- Download reports as CSV or Excel.
- Use your browser's print feature (Ctrl+P or Cmd+P) to print or save as PDF.

**3. All Policies in Database**
- View the entire database of policies and commissions in a single table.
- **Tip:** Use your browser's zoom-out (Ctrl -) to see more columns. Scroll horizontally for wide tables.

**4. Add New Policy Transaction**
- Use the form to manually add a new policy transaction to your database.

**5. Upload & Reconcile**
- Upload new commission statements or sales reports (Excel, CSV, or PDF).
- Map columns and reconcile commissions before saving to the database.
- Edit uploaded data before saving.
- Download reconciled data as CSV or Excel before saving.
- Save to database with one click.

**6. Edit Policies in Database**
- Edit any policy already in your database and save changes for all records at once.

**7. Search & Filter**
- Search and filter policies by customer name, policy number, carrier, or paid status.
- View and export filtered results.

**8. Admin Panel**
- Always see your current column mapping.
- Upload a file (Excel, CSV, or PDF) to preview its columns and customize how they map to your database columns.
- Save mapping for future uploads.
- See all columns in your uploaded file and your database.
- Rename your database column headers at the bottom of the Admin Panel.

---
**Tips:**
- Add a 'Paid' column and mark policies as 'Yes' when paid to track outstanding commissions.
- Use the Admin Panel to update column mappings or rename database columns if your file format changes.
- For best results, close Excel files before importing to avoid permission errors.
- Always use the Dashboard for quick client lookup, editing, and adding new transactions.
- **For maximum table width:** Use your browser's zoom-out (Ctrl -) and scroll horizontally for wide tables. The sidebar will always take up some space.
        """)