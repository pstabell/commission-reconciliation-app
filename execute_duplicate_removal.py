#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase URL and service key
supabase_url = os.getenv('SUPABASE_URL')
service_key = os.getenv('SUPABASE_SERVICE_KEY')

if not supabase_url or not service_key:
    print("Error: Missing SUPABASE_URL or SUPABASE_SERVICE_KEY")
    sys.exit(1)

# Extract project ref from URL
project_ref = supabase_url.split('//')[1].split('.')[0]

print(f"Connected to Supabase project: {project_ref}")
print("\nSTEP 1: Analyzing duplicates...")

# SQL to check duplicates
check_sql = """
-- Check how many duplicates we have
WITH duplicates AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC
        ) as rn
    FROM policies
)
SELECT COUNT(*) as duplicate_count
FROM duplicates
WHERE rn > 1;
"""

print("\nTo execute the duplicate removal, please:")
print("1. Go to your Supabase dashboard")
print("2. Navigate to SQL Editor")
print("3. Run the following SQL:\n")

# Print the full cleanup SQL
cleanup_sql = """
-- STEP 1: Check what will be deleted
WITH duplicates AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC  -- Keep the oldest
        ) as rn
    FROM policies
)
SELECT COUNT(*) as will_delete
FROM duplicates
WHERE rn > 1;

-- STEP 2: Show sample of what will be deleted (first 20)
WITH duplicates AS (
    SELECT 
        "Transaction ID",
        "Customer",
        "Policy Number",
        "Transaction Type",
        updated_at,
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC
        ) as rn
    FROM policies
)
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Transaction Type",
    updated_at,
    'WILL DELETE' as status
FROM duplicates
WHERE rn > 1
ORDER BY "Customer", "Policy Number"
LIMIT 20;

-- STEP 3: DELETE duplicates keeping the oldest of each group
WITH duplicates AS (
    SELECT 
        _id,
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC
        ) as rn
    FROM policies
)
DELETE FROM policies
WHERE _id IN (
    SELECT _id 
    FROM duplicates 
    WHERE rn > 1
);

-- STEP 4: Verify final count
SELECT COUNT(*) as final_count FROM policies;
"""

print(cleanup_sql)

print("\n" + "="*60)
print("IMPORTANT: This will remove duplicate transactions")
print("keeping only the OLDEST version of each duplicate set.")
print("Expected result: Transaction count should return to ~425")
print("="*60)