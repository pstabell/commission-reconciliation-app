-- Final verification of what we have

-- 1. Absolute total in policies table
SELECT 'Total policies:' as check, COUNT(*) as count FROM policies;

-- 2. Check reconciliations table (might have been counted separately)
SELECT 'Total reconciliations:' as check, COUNT(*) as count FROM reconciliations;

-- 3. Any other tables that might have policy-like data
SELECT 'Tables that might contain policy data:' as check;
SELECT table_name, 
       (SELECT COUNT(*) FROM information_schema.columns 
        WHERE columns.table_name = tables.table_name 
        AND column_name LIKE '%policy%') as policy_columns
FROM information_schema.tables
WHERE table_schema = 'public'
  AND (table_name LIKE '%polic%' 
       OR table_name LIKE '%transact%'
       OR table_name LIKE '%commiss%')
ORDER BY policy_columns DESC;

-- 4. The Edit bug theory - look for recent duplicates that might have been cleaned
SELECT 'Check for recent duplicate patterns:' as check;
SELECT 
    "Customer",
    "Policy Number",
    COUNT(*) as transaction_count
FROM policies
GROUP BY "Customer", "Policy Number"
HAVING COUNT(*) > 3
ORDER BY transaction_count DESC
LIMIT 10;

-- 5. Summary of what we know
SELECT 'Summary:' as check;
WITH summary AS (
    SELECT 
        COUNT(*) as total_policies,
        COUNT(DISTINCT "Policy Number") as unique_policies,
        COUNT(DISTINCT "Customer") as unique_customers,
        COUNT(DISTINCT "Transaction ID") as unique_transactions
    FROM policies
)
SELECT * FROM summary;