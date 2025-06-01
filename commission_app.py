import streamlit as st
import pandas as pd
import pdfplumber
import os
import json
import sqlalchemy
import datetime
import io
import streamlit_authenticator as stauth

# --- User credentials ---
names = ['Patrick Stabell', 'Elena Stabell']
usernames = ['pstabell', 'estabell']
passwords = ['05112007Abc!', '05112007Abc!']
hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    'sales_commissions_app', 'abcdef', cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error('Username/password is incorrect')
if authentication_status == None:
    st.warning('Please enter your username and password')
if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    # --- Place your main app code below this line ---
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

    st.set_page_config(layout="wide")

    st.title("Sales Commission Tracker")  # Changed title here

    # --- Sidebar Navigation ---
    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Reports",  # Changed from "Accounting Reports"
            "All Policies in Database",
            "Add New Client/Policy",
            "Upload & Reconcile",
            "Edit Policies in Database",
            "Search & Filter",
            "Admin Panel",
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
                "Calculated Commission" REAL
            )
        """))

    all_data = pd.read_sql('SELECT * FROM policies', engine)

    # --- Dashboard (Home Page) ---
    if page == "Dashboard":
        st.subheader("Dashboard")
        st.metric("Total Policies", len(all_data))
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
            if "Paid Amount" in client_df.columns and "New 50% Renewal 25%" in client_df.columns:
                paid_amounts = pd.to_numeric(client_df["Paid Amount"], errors="coerce").fillna(0)
                commission_amounts = pd.to_numeric(client_df["New 50% Renewal 25%"], errors="coerce").fillna(0)
                client_df["PAST DUE"] = commission_amounts - paid_amounts
            else:
                st.warning("Missing 'Paid Amount' or 'New 50% Renewal 25%' column for PAST DUE calculation.")

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
                    and "New 50% Renewal 25%" in client_df.columns
                ):
                    today = pd.to_datetime(datetime.date.today())
                    due_dates = pd.to_datetime(client_df["Due Date"], errors="coerce")
                    paid_amounts = pd.to_numeric(client_df["Paid Amount"], errors="coerce").fillna(0)
                    commission_amounts = pd.to_numeric(client_df["New 50% Renewal 25%"], errors="coerce").fillna(0)
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
                max_value=max_date
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
        if "PAST DUE" not in report_df.columns and "Paid Amount" in report_df.columns and "New 50% Renewal 25%" in report_df.columns:
            paid_amounts = pd.to_numeric(report_df["Paid Amount"], errors="coerce").fillna(0)
            commission_amounts = pd.to_numeric(report_df["New 50% Renewal 25%"], errors="coerce").fillna(0)
            report_df["PAST DUE"] = commission_amounts - paid_amounts
        # Apply Past Due filter
        if selected_past_due != "All" and "PAST DUE" in report_df.columns:
            if selected_past_due == "YES":
                report_df = report_df[report_df["PAST DUE"] > 0]
            elif selected_past_due == "NO":
                report_df = report_df[report_df["PAST DUE"] <= 0]

        st.markdown("**Report Preview:**")
        st.dataframe(report_df)

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
        st.dataframe(all_data)

    # --- Add New Client/Policy ---
    elif page == "Add New Client/Policy":
        st.subheader("Add New Client/Policy")
        with st.form("add_policy_form"):
            customer_name = st.text_input("Customer Name")
            policy_type = st.text_input("Policy Type")
            carrier_name = st.text_input("Carrier Name")
            policy_number = st.text_input("Policy Number")
            new_rwl = st.selectbox("NEW/RWL", ["NEW", "NBS", "STL", "BoR", "END", "PCH", "RWL", "REWRITE", "CAN", "XCL"])
            agency_revenue = st.number_input("Agency Revenue", min_value=0.0, step=0.01)
            policy_orig_date = st.date_input("Policy Origination Date")
            effective_date = st.date_input("Effective Date")
            paid = st.selectbox("Paid", ["No", "Yes"])
            submitted = st.form_submit_button("Add Policy")
        if submitted:
            row = {
                "Customer Name": customer_name,
                "Policy Type": policy_type,
                "Carrier Name": carrier_name,
                "Policy Number": policy_number,
                "NEW/RWL": new_rwl,
                "Agency Revenue": agency_revenue,
                "Policy Origination Date": str(policy_orig_date),
                "Effective Date": str(effective_date),
                "Paid": paid
            }
            row["Calculated Commission"] = calculate_commission(row)
            new_df = pd.DataFrame([row])
            new_df.to_sql('policies', engine, if_exists='append', index=False)
            st.success("New client/policy added!")

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
                st.write("Extracted DataFrame preview:", df.head(5))
                header_row = st.number_input(
                    "Which row contains the column headers? (0 = first row)", min_value=0, max_value=min(10, len(df)-1), value=0
                )
                df.columns = df.iloc[header_row]
                df = df[(header_row+1):].reset_index(drop=True)
                df.columns = df.columns.str.strip()
                st.write("Columns after header set:", df.columns.tolist())
                st.write(df.head())
            df.columns = df.columns.str.strip()
            st.write("Columns found:", df.columns.tolist())
            mapping_file = "column_mapping.json"
            default_columns = [
                "Customer Name", "Policy Type", "Carrier Name", "Policy Number", "NEW/RWL",
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
            edited_df = st.data_editor(df)
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
        edited_db_df = st.data_editor(all_data.reset_index(drop=True))
        if st.button("Update Database with Edits"):
            edited_db_df.to_sql('policies', engine, if_exists='replace', index=False)
            st.success("Database updated with your edits!")

    # --- Search & Filter ---
    elif page == "Search & Filter":
        st.subheader("Search & Filter Policies")

        # Dropdown to select which column to search by (all headers)
        search_column = st.selectbox("Search by column:", all_data.columns.tolist())
        search_text = st.text_input(f"Search for value in '{search_column}':")

        # Dropdown to filter by Past Due status
        past_due_options = ["All", "YES", "NO"]
        selected_past_due = st.selectbox("Past Due", past_due_options)

        filtered_data = all_data.copy()

        # Apply search filter
        if search_text:
            filtered_data = filtered_data[filtered_data[search_column].astype(str).str.contains(search_text, case=False, na=False)]

        # Calculate PAST DUE if not present
        if "PAST DUE" not in filtered_data.columns and "Paid Amount" in filtered_data.columns and "New 50% Renewal 25%" in filtered_data.columns:
            paid_amounts = pd.to_numeric(filtered_data["Paid Amount"], errors="coerce").fillna(0)
            commission_amounts = pd.to_numeric(filtered_data["New 50% Renewal 25%"], errors="coerce").fillna(0)
            filtered_data["PAST DUE"] = commission_amounts - paid_amounts

        # Apply Past Due filter
        if selected_past_due != "All" and "PAST DUE" in filtered_data.columns:
            if selected_past_due == "YES":
                filtered_data = filtered_data[filtered_data["PAST DUE"] > 0]
            elif selected_past_due == "NO":
                filtered_data = filtered_data[filtered_data["PAST DUE"] <= 0]

        st.subheader("Filtered Policies")
        st.dataframe(filtered_data, use_container_width=True, height=400)  # Increased height so first row is always visible

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
        if "admin_warning_ack" not in st.session_state or not st.session_state["admin_warning_ack"]:
            st.warning("⚠️ The Admin Panel is for administrative use only. Changes here can affect your entire database. Proceed with caution!")
            if st.button("I Understand, Continue to Admin Panel"):
                st.session_state["admin_warning_ack"] = True
            else:
                st.stop()
        st.header("Admin Panel: Column Mapping & Header Editing")
        mapping_file = "column_mapping.json"
        default_columns = [
            "Customer Name", "Policy Type", "Carrier Name", "Policy Number", "NEW/RWL",
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
            if st.warning("Are you sure you want to add this column? This action cannot be undone from the app."):
                confirm_add = st.button("Continue", key="confirm_add_col")
                cancel_add = st.button("Cancel", key="cancel_add_col")
                if confirm_add:
                    with engine.begin() as conn:
                        conn.execute(sqlalchemy.text(f'ALTER TABLE policies ADD COLUMN "{new_col_name}" TEXT'))
                    st.success(f"Column '{new_col_name}' added.")
                    st.experimental_rerun()
                elif cancel_add:
                    st.info("Add column cancelled.")
        elif add_col_submitted and new_col_name in db_columns:
            st.warning(f"Column '{new_col_name}' already exists.")

        # Delete Column
        with st.form("delete_column_form"):
            col_to_delete = st.selectbox("Select column to delete", db_columns)
            delete_col_submitted = st.form_submit_button("Delete Column")
        if delete_col_submitted and col_to_delete:
            if st.warning("⚠️ Deleting a column is permanent and cannot be undone. Are you sure you want to continue?"):
                confirm_del = st.button("Continue", key="confirm_del_col")
                cancel_del = st.button("Cancel", key="cancel_del_col")
                if confirm_del:
                    with engine.begin() as conn:
                        # Get current columns except the one to delete
                        remaining_cols = [col for col in db_columns if col != col_to_delete]
                        cols_str = ", ".join([f'"{col}"' for col in remaining_cols])
                        # Rename old table
                        conn.execute(sqlalchemy.text('ALTER TABLE policies RENAME TO policies_old'))
                        # Create new table without the deleted column
                        df_temp = pd.read_sql('SELECT * FROM policies_old', conn)
                        df_temp = df_temp[remaining_cols]
                        df_temp.to_sql('policies', conn, if_exists='replace', index=False)
                        conn.execute(sqlalchemy.text('DROP TABLE policies_old'))
                    st.success(f"Column '{col_to_delete}' deleted.")
                    st.experimental_rerun()
                elif cancel_del:
                    st.info("Delete column cancelled.")

        # --- Reorder Columns Section ---
        st.subheader("Reorder Database Columns")
        db_columns = all_data.columns.tolist()
        new_order = st.multiselect(
            "Select and order columns as you want them to appear in the database (drag to reorder):",
            db_columns,
            default=db_columns
        )
        if st.button("Apply New Column Order"):
            if set(new_order) == set(db_columns):
                with engine.begin() as conn:
                    df_temp = pd.read_sql('SELECT * FROM policies', conn)
                    df_temp = df_temp[new_order]
                    conn.execute(sqlalchemy.text('ALTER TABLE policies RENAME TO policies_old'))
                    df_temp.to_sql('policies', conn, if_exists='replace', index=False)
                    conn.execute(sqlalchemy.text('DROP TABLE policies_old'))
                st.success("Column order updated.")
                st.experimental_rerun()
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
                if st.warning("Are you sure you want to rename these columns?"):
                    confirm_rename = st.button("Continue", key="confirm_rename_col")
                    cancel_rename = st.button("Cancel", key="cancel_rename_col")
                    if confirm_rename:
                        with engine.begin() as conn:
                            for old, new in rename_dict.items():
                                conn.execute(sqlalchemy.text(f'ALTER TABLE policies RENAME COLUMN "{old}" TO "{new}"'))
                        st.success(f"Renamed columns: {rename_dict}")
                        st.experimental_rerun()
                    elif cancel_rename:
                        st.info("Rename columns cancelled.")
            else:
                st.info("No changes made to column names.")

    # --- Help ---
    elif page == "Help":
        with st.expander("❓ Help / Instructions", expanded=True):
            st.markdown("""
    ### How to Use This App

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

    **4. Add New Client/Policy**
    - Use the form to manually add a new client or policy to your database.

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
            """)
    st.markdown("""
        <style>
        /* Make scrollbars thicker and easier to grab */
        ::-webkit-scrollbar {
            width: 18px;
            height: 18px;
        }
        ::-webkit-scrollbar-thumb {
            background: #b0b0b0;
            border-radius: 9px;
            border: 4px solid #f0f0f0;
        }
        ::-webkit-scrollbar-track {
            background: #f0f0f0;
            border-radius: 9px;
        }
        /* For Firefox */
        html {
            scrollbar-width: thick;
            scrollbar-color: #b0b0b0 #f0f0f0;
        }
        </style>
    """, unsafe_allow_html=True)