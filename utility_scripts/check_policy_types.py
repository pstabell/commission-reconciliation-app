#!/usr/bin/env python3
"""
Script to check policy type counts in the database.
This will query the transactions table to count different policy types.
"""

import os
from supabase import create_client
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

def get_supabase_client():
    """Get Supabase client."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        print("ERROR: Missing Supabase credentials. Please check your .env file.")
        return None
    return create_client(url, key)

def check_policy_types():
    """Check policy type counts in the database."""
    # Get Supabase client
    supabase = get_supabase_client()
    if not supabase:
        return
    
    print("Connecting to Supabase...")
    
    try:
        # Query all transactions to get policy types
        print("\nFetching all transactions from database...")
        response = supabase.table('transactions').select('*').execute()
        
        if response.data:
            # Convert to DataFrame for easier analysis
            df = pd.DataFrame(response.data)
            print(f"\nTotal transactions found: {len(df)}")
            
            # Check if policy_type column exists
            if 'policy_type' in df.columns:
                # Count policy types
                policy_type_counts = df['policy_type'].value_counts(dropna=False)
                
                print("\n=== POLICY TYPE COUNTS ===")
                print(policy_type_counts.to_string())
                
                # Check specifically for HOME and AUTO
                print("\n=== SPECIFIC POLICY TYPE CHECKS ===")
                home_count = len(df[df['policy_type'] == 'HOME'])
                auto_count = len(df[df['policy_type'] == 'AUTO'])
                
                print(f"HOME policy count: {home_count}")
                print(f"AUTO policy count: {auto_count}")
                
                # Check for any variations (case-insensitive)
                print("\n=== CASE-INSENSITIVE CHECKS ===")
                if 'policy_type' in df.columns:
                    df['policy_type_upper'] = df['policy_type'].fillna('').str.upper()
                    home_variations = df[df['policy_type_upper'].str.contains('HOME', na=False)]
                    auto_variations = df[df['policy_type_upper'].str.contains('AUTO', na=False)]
                    
                    print(f"Transactions containing 'HOME' (any case): {len(home_variations)}")
                    print(f"Transactions containing 'AUTO' (any case): {len(auto_variations)}")
                
                # Show unique policy types
                print("\n=== ALL UNIQUE POLICY TYPES ===")
                unique_types = df['policy_type'].unique()
                for pt in sorted(unique_types, key=lambda x: (x is None, x)):
                    if pt is None:
                        print("None (null values)")
                    else:
                        print(f"'{pt}'")
                        
                # Check for nulls
                null_count = df['policy_type'].isna().sum()
                print(f"\nNull/empty policy_type count: {null_count}")
                
            else:
                print("\nWARNING: 'policy_type' column not found in transactions table!")
                print("Available columns:", list(df.columns))
                
        else:
            print("\nNo transactions found in database.")
            
    except Exception as e:
        print(f"\nError querying database: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_policy_types()