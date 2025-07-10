#!/usr/bin/env python3
"""
Migration script to add policy tracking fields for renewal chains.

This script adds two new fields to the policies table:
- Prior Policy Number: Links to the previous policy number in a renewal chain
- Original Effective Date: Maintains the original policy inception date through renewals

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

def add_policy_tracking_fields():
    """Add policy tracking fields to the policies table."""
    supabase = get_supabase_client()
    
    print("Adding policy tracking fields to policies table...")
    
    try:
        # Note: Supabase doesn't support ALTER TABLE through the client library
        # You'll need to run these SQL commands in the Supabase SQL editor:
        
        sql_commands = """
-- Add Prior Policy Number field to track renewal chains
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS "Prior Policy Number" TEXT;

-- Add Original Effective Date to maintain inception date through renewals  
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS "Original Effective Date" TEXT;

-- Add indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_prior_policy_number 
ON policies("Prior Policy Number");

CREATE INDEX IF NOT EXISTS idx_original_effective_date 
ON policies("Original Effective Date");

-- Add comment to explain the fields
COMMENT ON COLUMN policies."Prior Policy Number" 
IS 'Links to the previous policy number in a renewal chain';

COMMENT ON COLUMN policies."Original Effective Date" 
IS 'Maintains the original policy inception date through renewals';
"""
        
        print("\nPlease run the following SQL commands in your Supabase SQL editor:")
        print("=" * 80)
        print(sql_commands)
        print("=" * 80)
        
        print("\nAlternatively, you can use the Supabase Dashboard:")
        print("1. Go to your Supabase project")
        print("2. Navigate to Table Editor > policies")
        print("3. Click 'Add column' and add:")
        print("   - Column name: 'Prior Policy Number', Type: text, Nullable: Yes")
        print("   - Column name: 'Original Effective Date', Type: text, Nullable: Yes")
        
        # Test if we can query the table
        result = supabase.table('policies').select("*").limit(1).execute()
        print(f"\nCurrent policies table has {len(result.data)} test record(s)")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: The Supabase client library doesn't support ALTER TABLE commands.")
        print("Please add the columns manually using the SQL commands above.")

if __name__ == "__main__":
    add_policy_tracking_fields()