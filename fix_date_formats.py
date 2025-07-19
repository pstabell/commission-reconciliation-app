#!/usr/bin/env python3
"""
Script to fix date formats in the database from DD/MM/YYYY to YYYY-MM-DD
"""

import os
import sys
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

def get_supabase_client() -> Client:
    """Initialize and return Supabase client."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("Supabase credentials not found in environment variables")
    
    return create_client(url, key)

def convert_date_format(date_str):
    """Convert date from DD/MM/YYYY to YYYY-MM-DD format."""
    if not date_str or pd.isna(date_str):
        return None
    
    # Skip if already in correct format
    if isinstance(date_str, str) and len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
        try:
            # Validate it's a proper date
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except:
            pass
    
    # Try to parse DD/MM/YYYY format
    try:
        if isinstance(date_str, str) and '/' in date_str:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            return date_obj.strftime('%Y-%m-%d')
    except:
        pass
    
    # Try other common formats
    try:
        # If it's already a datetime object
        if hasattr(date_str, 'strftime'):
            return date_str.strftime('%Y-%m-%d')
    except:
        pass
    
    print(f"Warning: Could not parse date: {date_str}")
    return date_str

def fix_transaction_dates():
    """Fix all date fields in the transactions table."""
    try:
        supabase = get_supabase_client()
        
        print("Fetching all transactions...")
        # Fetch all transactions
        response = supabase.table('transactions').select("*").execute()
        transactions = response.data
        
        if not transactions:
            print("No transactions found.")
            return
        
        print(f"Found {len(transactions)} transactions to process.")
        
        # Date columns to fix
        date_columns = [
            'Effective Date',
            'Transaction Date',
            'Commission Received Date',
            'Agent Paid Date',
            'Policy Origination Date'
        ]
        
        updated_count = 0
        error_count = 0
        
        for trans in transactions:
            try:
                updates = {}
                trans_id = trans.get('_id')
                
                # Check each date column
                for col in date_columns:
                    if col in trans and trans[col]:
                        old_value = trans[col]
                        new_value = convert_date_format(old_value)
                        
                        if new_value and new_value != old_value:
                            updates[col] = new_value
                            print(f"Transaction {trans_id}: {col} changing from '{old_value}' to '{new_value}'")
                
                # Update the transaction if there are changes
                if updates:
                    response = supabase.table('transactions').update(updates).eq('_id', trans_id).execute()
                    updated_count += 1
                    print(f"✓ Updated transaction {trans_id}")
                
            except Exception as e:
                error_count += 1
                print(f"✗ Error updating transaction {trans.get('_id')}: {str(e)}")
                continue
        
        print(f"\nSummary:")
        print(f"- Total transactions processed: {len(transactions)}")
        print(f"- Transactions updated: {updated_count}")
        print(f"- Errors: {error_count}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def main():
    """Main function."""
    print("=== Date Format Migration Script ===")
    print("This will convert all dates from DD/MM/YYYY to YYYY-MM-DD format")
    print()
    
    # Confirm before proceeding
    response = input("Do you want to proceed? (yes/no): ")
    if response.lower() != 'yes':
        print("Migration cancelled.")
        return
    
    print("\nStarting migration...")
    fix_transaction_dates()
    print("\nMigration complete!")

if __name__ == "__main__":
    main()