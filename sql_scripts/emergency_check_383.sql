-- EMERGENCY: Investigate why we dropped to 383 records from 425

-- 1. Current exact count
SELECT 'CURRENT STATUS:' as check;
SELECT COUNT(*) as total_records FROM policies;

-- 2. Check for any deletion activity
SELECT 'Recent deletions?' as check;
SELECT 
    schemaname,
    tablename,
    n_tup_del as total_deletions,
    n_tup_ins as total_insertions,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables 
WHERE tablename = 'policies';

-- 3. Group by user to see if records are missing for specific users
SELECT 'Records by user:' as check;
SELECT 
    user_email,
    COUNT(*) as record_count
FROM policies
GROUP BY user_email
ORDER BY user_email;

-- 4. Check for specific missing policies
SELECT 'Key policies check:' as check;
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM policies WHERE "Customer" = 'Katie Oyster') THEN 'Katie Oyster: EXISTS'
        ELSE 'Katie Oyster: MISSING'
    END as katie_status,
    CASE 
        WHEN EXISTS (SELECT 1 FROM policies WHERE "Customer" = 'Lee Hopper') THEN 'Lee Hopper: EXISTS'
        ELSE 'Lee Hopper: MISSING'
    END as lee_status,
    CASE 
        WHEN EXISTS (SELECT 1 FROM policies WHERE "Customer" = 'Perfect Lanais LLC') THEN 'Perfect Lanais: EXISTS'
        ELSE 'Perfect Lanais: MISSING'
    END as perfect_status;

-- 5. Count by transaction type
SELECT 'Transaction types:' as check;
SELECT 
    "Transaction Type",
    COUNT(*) as count
FROM policies
GROUP BY "Transaction Type"
ORDER BY count DESC;

-- 6. Check for any filters that might be hiding records
SELECT 'Check for NULL user_emails:' as check;
SELECT COUNT(*) as null_user_emails
FROM policies
WHERE user_email IS NULL OR user_email = '';

-- 7. Recent activity
SELECT 'Last 10 updated records:' as check;
SELECT 
    "Transaction ID",
    "Customer",
    updated_at
FROM policies
ORDER BY updated_at DESC
LIMIT 10;