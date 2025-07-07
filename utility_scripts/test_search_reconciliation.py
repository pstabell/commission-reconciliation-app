#!/usr/bin/env python3
"""
Test script to search for reconciliation transactions in the database.
This will help understand why searching for "-STMT-" returns no results.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from supabase import create_client
import pandas as pd

# Load environment variables
load_dotenv()

def test_reconciliation_search():
    """Test searching for reconciliation transactions."""
    
    # Get Supabase credentials
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        print("ERROR: Missing Supabase credentials. Please check your .env file.")
        return
    
    try:
        # Connect to Supabase
        supabase = create_client(url, key)
        print("Connected to Supabase successfully.")
        
        # Load all data
        print("\nLoading all policies data...")
        response = supabase.table('policies').select("*").execute()
        
        if not response.data:
            print("No data found in policies table.")
            return
            
        df = pd.DataFrame(response.data)
        print(f"Loaded {len(df)} records.")
        
        # Print column names
        print("\nColumn names in database:")
        for col in df.columns:
            print(f"  - {col}")
        
        # Find the Transaction ID column
        transaction_id_cols = []
        for col in df.columns:
            if 'transaction' in col.lower() and 'id' in col.lower():
                transaction_id_cols.append(col)
        
        if not transaction_id_cols:
            print("\nERROR: No Transaction ID column found!")
            # Try to find any column containing transaction IDs
            print("\nSearching all columns for -STMT- pattern...")
            for col in df.columns:
                if df[col].astype(str).str.contains('-STMT-', na=False).any():
                    print(f"Found -STMT- in column: {col}")
                    sample = df[df[col].astype(str).str.contains('-STMT-', na=False)][col].head()
                    print(f"Sample values: {sample.tolist()}")
            return
        
        print(f"\nFound Transaction ID column(s): {transaction_id_cols}")
        
        # Search for reconciliation patterns
        for tid_col in transaction_id_cols:
            print(f"\nSearching in column: {tid_col}")
            
            # Convert to string and search
            df[tid_col] = df[tid_col].astype(str)
            
            # Count different patterns
            stmt_count = df[tid_col].str.contains('-STMT-', na=False).sum()
            void_count = df[tid_col].str.contains('-VOID-', na=False).sum()
            adj_count = df[tid_col].str.contains('-ADJ-', na=False).sum()
            
            print(f"  -STMT- transactions: {stmt_count}")
            print(f"  -VOID- transactions: {void_count}")
            print(f"  -ADJ- transactions: {adj_count}")
            
            # Show samples if found
            if stmt_count > 0:
                print("\n  Sample -STMT- transactions:")
                stmt_df = df[df[tid_col].str.contains('-STMT-', na=False)]
                for _, row in stmt_df.head(5).iterrows():
                    print(f"    - {row[tid_col]} | Customer: {row.get('Customer', 'N/A')}")
            
            # Search for the specific known transaction
            known_id = "RD84L6D-STMT-20240630"
            print(f"\n  Searching for known transaction: {known_id}")
            exact_match = df[df[tid_col] == known_id]
            contains_match = df[df[tid_col].str.contains(known_id, na=False)]
            
            if not exact_match.empty:
                print(f"  Found exact match! Customer: {exact_match.iloc[0].get('Customer', 'N/A')}")
            elif not contains_match.empty:
                print(f"  Found partial match! Transaction ID: {contains_match.iloc[0][tid_col]}")
            else:
                print("  No match found for known transaction.")
                
                # Try searching without case sensitivity
                case_insensitive = df[df[tid_col].str.upper() == known_id.upper()]
                if not case_insensitive.empty:
                    print(f"  Found case-insensitive match! Actual ID: {case_insensitive.iloc[0][tid_col]}")
        
        # Try direct text search
        print("\n\nPerforming direct text search for '-STMT-' across all string columns...")
        string_cols = df.select_dtypes(include=['object']).columns
        for col in string_cols:
            if df[col].astype(str).str.contains('-STMT-', na=False, regex=False).any():
                count = df[col].astype(str).str.contains('-STMT-', na=False, regex=False).sum()
                print(f"  Found {count} matches in column: {col}")
                
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_reconciliation_search()