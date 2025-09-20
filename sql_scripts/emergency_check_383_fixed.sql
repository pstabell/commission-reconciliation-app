-- EMERGENCY: Investigate why we dropped to 383 records from 425

-- 1. Current exact count
SELECT 'CURRENT STATUS:' as check, COUNT(*) as total_records FROM policies;

-- 2. Total unfiltered count (no WHERE clause)
SELECT 'TOTAL IN DATABASE:' as check, COUNT(*) as total_unfiltered FROM policies;

-- 3. Group by user to see distribution
SELECT 'Records by user email:' as check_type;
SELECT 
    user_email,
    COUNT(*) as record_count,
    COUNT(DISTINCT "Transaction ID") as unique_transactions
FROM policies
GROUP BY user_email
ORDER BY record_count DESC;

-- 4. Check for specific missing policies
SELECT 'Key customers check:' as check_type;
SELECT 
    "Customer",
    COUNT(*) as transaction_count
FROM policies
WHERE "Customer" IN ('Katie Oyster', 'Katie Oster', 'Lee Hopper', 'Lee Hope May', 
                     'Perfect Lanais LLC', 'Pinnacle Investments LLC', 'Orion Investments LLC')
GROUP BY "Customer"
ORDER BY "Customer";

-- 5. Count by transaction type
SELECT 'Transaction types:' as check_type;
SELECT 
    "Transaction Type",
    COUNT(*) as count
FROM policies
GROUP BY "Transaction Type"
ORDER BY count DESC;

-- 6. Check for records without proper user assignment
SELECT 'Records with NULL/empty user_email:' as check_type;
SELECT COUNT(*) as count
FROM policies
WHERE user_email IS NULL OR user_email = '';

-- 7. Check for records without user_id
SELECT 'Records with NULL user_id:' as check_type;
SELECT COUNT(*) as count
FROM policies
WHERE user_id IS NULL;

-- 8. Recent activity (last 24 hours)
SELECT 'Records updated in last 24 hours:' as check_type;
SELECT COUNT(*) as count
FROM policies
WHERE updated_at > NOW() - INTERVAL '24 hours';

-- 9. Sample of recent records
SELECT 'Last 10 updated records:' as check_type;
SELECT 
    "Transaction ID",
    LEFT("Customer", 30) as customer,
    user_email,
    updated_at
FROM policies
ORDER BY updated_at DESC
LIMIT 10;

-- 10. Check for duplicate Transaction IDs again
SELECT 'Duplicate Transaction IDs:' as check_type;
SELECT COUNT(*) as duplicate_count
FROM (
    SELECT "Transaction ID"
    FROM policies
    GROUP BY "Transaction ID"
    HAVING COUNT(*) > 1
) dup;