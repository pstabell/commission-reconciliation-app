-- Investigate where the 41 transactions could have gone - FIXED

-- 1. First, see what columns audit_logs has
SELECT 'Audit_logs columns:' as check;
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'audit_logs';

-- 2. Check for soft delete or status columns in policies
SELECT 'Policies table - status/delete columns:' as check;
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'policies'
  AND (column_name ILIKE '%delete%' 
       OR column_name ILIKE '%removed%'
       OR column_name ILIKE '%archived%'
       OR column_name ILIKE '%active%'
       OR column_name ILIKE '%status%'
       OR column_name ILIKE '%hidden%');

-- 3. Count by Transaction Type to understand the 425
SELECT 'Breakdown by Transaction Type:' as check;
SELECT 
    COALESCE("Transaction Type", 'NULL') as trans_type, 
    COUNT(*) as count
FROM policies
GROUP BY "Transaction Type"
ORDER BY count DESC;

-- 4. Look for reconciliation entries (STMT)
SELECT 'Reconciliation transactions:' as check;
SELECT COUNT(*) as stmt_count
FROM policies
WHERE "Transaction Type" = 'STMT' 
   OR "Transaction ID" LIKE '%-STMT-%'
   OR "Notes" ILIKE '%reconcil%';

-- 5. Check when the most recent policies were added
SELECT 'Most recent policy additions:' as check;
SELECT 
    "Transaction ID",
    "Customer",
    "Transaction Type",
    "Premium Sold",
    updated_at
FROM policies
ORDER BY updated_at DESC
LIMIT 10;

-- 6. Total unique policy numbers (maybe duplicates were consolidated?)
SELECT 'Unique vs Total policies:' as check;
SELECT 
    COUNT(DISTINCT "Policy Number") as unique_policy_numbers,
    COUNT(*) as total_transactions
FROM policies;