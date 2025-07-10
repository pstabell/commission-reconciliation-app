#!/usr/bin/env python3
"""
Migration script to rename the checklist column.

This script renames "New Biz Checklist Complete" to "Policy Checklist Complete"
to match the UI naming convention.

Run this script to update your database schema.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

def get_supabase_client() -> Client:
    """Initialize Supabase client."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        raise ValueError("Please set SUPABASE_URL and SUPABASE_ANON_KEY in your .env file")
    
    return create_client(url, key)

def rename_checklist_column():
    """Rename the checklist column in the policies table."""
    supabase = get_supabase_client()
    
    print("Renaming checklist column in policies table...")
    
    try:
        # Note: Supabase doesn't support ALTER TABLE through the client library
        # You'll need to run this SQL command in the Supabase SQL editor:
        
        sql_command = """
-- Rename the column from "New Biz Checklist Complete" to "Policy Checklist Complete"
ALTER TABLE policies 
RENAME COLUMN "New Biz Checklist Complete" TO "Policy Checklist Complete";
"""
        
        print("\nPlease run the following SQL command in your Supabase SQL editor:")
        print("=" * 80)
        print(sql_command)
        print("=" * 80)
        
        print("\nAlternatively, you can use the Supabase Dashboard:")
        print("1. Go to your Supabase project")
        print("2. Navigate to Table Editor > policies")
        print("3. Find the column 'New Biz Checklist Complete'")
        print("4. Click on the column header dropdown")
        print("5. Select 'Edit column'")
        print("6. Change the name to 'Policy Checklist Complete'")
        print("7. Click 'Save'")
        
        # Test if we can query the table
        result = supabase.table('policies').select("*").limit(1).execute()
        print(f"\nCurrent policies table has {len(result.data)} test record(s)")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: The Supabase client library doesn't support ALTER TABLE commands.")
        print("Please rename the column manually using the SQL command above.")

if __name__ == "__main__":
    rename_checklist_column()