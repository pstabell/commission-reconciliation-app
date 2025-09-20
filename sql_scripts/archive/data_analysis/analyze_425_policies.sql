-- Analyze the 425 policies we have

-- 1. Transaction Type breakdown
SELECT 'Transaction Types:' as check;
SELECT 
    COALESCE("Transaction Type", 'NULL') as type, 
    COUNT(*) as count
FROM policies
GROUP BY "Transaction Type"
ORDER BY count DESC;

-- 2. Check for STMT in Transaction ID
SELECT 'STMT transactions by ID pattern:' as check;
SELECT COUNT(*) as stmt_pattern_count
FROM policies
WHERE "Transaction ID" LIKE '%STMT%'
   OR "Transaction ID" LIKE '%-STMT-%';

-- 3. Unique Policy Numbers vs Total Transactions
SELECT 'Policy consolidation check:' as check;
SELECT 
    COUNT(DISTINCT "Policy Number") as unique_policies,
    COUNT(*) as total_transactions,
    COUNT(*) - COUNT(DISTINCT "Policy Number") as duplicate_policy_numbers
FROM policies;

-- 4. Recent activity - last 48 hours
SELECT 'Recent updates (48hr):' as check;
SELECT 
    DATE_TRUNC('hour', updated_at) as hour,
    COUNT(*) as changes
FROM policies
WHERE updated_at > NOW() - INTERVAL '48 hours'
GROUP BY hour
ORDER BY hour DESC;

-- 5. Sample of most recent transactions
SELECT 'Latest 5 transactions:' as check;
SELECT 
    "Transaction ID",
    "Transaction Type",
    "Customer",
    LEFT("Policy Number", 20) as policy_num_start,
    updated_at
FROM policies
ORDER BY updated_at DESC
LIMIT 5;

-- 6. The real question - were there ever 466?
SELECT 'Database-wide count:' as check;
SELECT 
    (SELECT COUNT(*) FROM policies) as policies_table,
    (SELECT COUNT(*) FROM deleted_policies) as deleted_table,
    (SELECT COUNT(*) FROM audit_logs) as audit_entries;