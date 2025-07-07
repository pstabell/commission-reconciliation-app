#!/usr/bin/env python3
"""
Verify that the search functionality now works correctly for reconciliation transactions.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from supabase import create_client
import pandas as pd

# Load environment variables
load_dotenv()

def verify_search_fix():
    """Test the fixed search functionality."""
    
    # Get Supabase credentials
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        print("ERROR: Missing Supabase credentials.")
        return
    
    try:
        # Connect to Supabase
        supabase = create_client(url, key)
        
        # Load all data
        response = supabase.table('policies').select("*").execute()
        if not response.data:
            print("No data found.")
            return
            
        all_data = pd.DataFrame(response.data)
        print(f"Loaded {len(all_data)} records.")
        
        # Test search terms
        test_searches = [
            "-STMT-",
            "RD84L6D",
            "Thomas Barboun",
            "F266CCX-STMT-20240630"
        ]
        
        # Updated search columns (with spaces, not underscores)
        search_columns = ['Customer', 'Policy Number', 'Transaction ID', 'Client ID']
        
        print("\nTesting search functionality with corrected column names:")
        print(f"Search columns: {search_columns}")
        print(f"Available columns: {list(all_data.columns)}")
        
        for search_term in test_searches:
            print(f"\n--- Searching for: '{search_term}' ---")
            
            # Search across multiple columns (mimicking the app's search)
            mask = pd.Series(False, index=all_data.index)
            
            for col in search_columns:
                if col in all_data.columns:
                    mask |= all_data[col].astype(str).str.contains(search_term, case=False, na=False)
                    # Check individual column matches
                    col_matches = all_data[col].astype(str).str.contains(search_term, case=False, na=False).sum()
                    if col_matches > 0:
                        print(f"  Found {col_matches} matches in column: {col}")
                else:
                    print(f"  WARNING: Column '{col}' not found in data!")
            
            search_results = all_data[mask]
            print(f"  Total matches found: {len(search_results)}")
            
            if not search_results.empty:
                print("  Sample results:")
                for _, row in search_results.head(3).iterrows():
                    print(f"    - Transaction ID: {row['Transaction ID']} | Customer: {row['Customer']}")
        
        # Specifically test reconciliation transaction detection
        print("\n--- Testing reconciliation transaction detection ---")
        reconciliation_types = ['-STMT-', '-VOID-', '-ADJ-']
        
        for suffix in reconciliation_types:
            count = all_data['Transaction ID'].astype(str).str.contains(suffix, na=False).sum()
            print(f"  {suffix} transactions: {count}")
            
            if count > 0:
                sample = all_data[all_data['Transaction ID'].astype(str).str.contains(suffix, na=False)]
                print(f"    Sample IDs: {sample['Transaction ID'].head(3).tolist()}")
                
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_search_fix()