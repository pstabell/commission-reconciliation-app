import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.title("Test Policies Table Insert")

# Get Supabase client
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

if st.button("Test Insert with More Fields"):
    try:
        # Test with correct column names from database
        test_data = {
            "Transaction ID": "TEST789",
            "Customer": "Test Customer",
            "Policy Number": "TEST-POLICY-003",
            "Policy Type": "Auto",
            "Effective Date": "06/30/2024",
            "Transaction Type": "NEW",
            "STMT DATE": "06/30/2024",
            "Agency Comm Received (STMT)": 100.50,  # Correct column name
            "Agent Paid Amount (STMT)": 50.25,  # Correct column name
            "Client ID": "ABC123"
        }
        
        st.write("Attempting to insert:")
        st.json(test_data)
        
        result = supabase.table('policies').insert(test_data).execute()
        st.success("Insert successful!")
        st.write("Result:", result.data)
        
    except Exception as e:
        st.error(f"Insert failed: {e}")
        st.code(str(e))
        
        # Try to get more details about the error
        if hasattr(e, 'message'):
            st.error(f"Error message: {e.message}")
        if hasattr(e, 'details'):
            st.error(f"Error details: {e.details}")

# Show current table structure
if st.button("Show Table Columns"):
    try:
        # Get one row to see column names
        result = supabase.table('policies').select("*").limit(1).execute()
        if result.data:
            st.write("Column names in policies table:")
            st.write(list(result.data[0].keys()))
        else:
            st.write("No data in table to show columns")
    except Exception as e:
        st.error(f"Error fetching columns: {e}")