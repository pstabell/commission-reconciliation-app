import streamlit as st
import pandas as pd

# Function to calculate commissions based on 'New 50% Renewal 25%' rule
def calculate_commission(row):
    if row["NEW/RWL"] in ["NEW", "NBS", "STL", "BoR"]:  
        return row["Agency Revenue"] * 0.50  # Always 50% for these categories
    elif row["NEW/RWL"] in ["END", "PCH"]:
        return row["Agency Revenue"] * 0.50 if row["Policy Origination Date"] == row["Effective Date"] else row["Agency Revenue"] * 0.25
    elif row["NEW/RWL"] in ["RWL", "REWRITE"]:
        return row["Agency Revenue"] * 0.25  # Standard renewals
    elif row["NEW/RWL"] in ["CAN", "XCL"]:
        return 0  # No commission for cancellations
    else:
        return row["Agency Revenue"] * 0.25  # Default renewal rate

# Streamlit app setup
st.title("Sales Commission Reconciliation App")

# File upload section
uploaded_file = st.file_uploader("Upload your sales commission spreadsheet", type=["xlsx", "xls", "csv"])

if uploaded_file:
    # Load file into a DataFrame
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file, engine="openpyxl", header=0)  # `header=0` means first row is the header
    elif uploaded_file.name.endswith(".xls"):
        df = pd.read_excel(uploaded_file, engine="xlrd", header=1)
    else:
        df = pd.read_csv(uploaded_file)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Apply commission calculations
    df["Calculated Commission"] = df.apply(calculate_commission, axis=1)

    # Display the processed data
    st.subheader("Data with Calculated Commissions")
    st.write(df)

    # Allow editing
    st.subheader("Edit Data")
    edited_df = st.data_editor(df)

    # Export results
    st.subheader("Download Results")
    st.download_button(
        label="Download as CSV",
        data=edited_df.to_csv(index=False),
        file_name="reconciled_commissions.csv",
        mime="text/csv"
    )