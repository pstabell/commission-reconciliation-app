-- EMERGENCY: Clean up from 1,188 records back to 425
-- The system has created ~3x duplicates of everything!

-- 1. Confirm the disaster
SELECT 'CURRENT DISASTER:' as status;
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT "Transaction ID") as unique_transactions,
    COUNT(*) - COUNT(DISTINCT "Transaction ID") as duplicate_records
FROM policies;

-- 2. See how bad the duplication is
SELECT 'Duplication severity:' as status;
WITH dup_counts AS (
    SELECT 
        "Transaction ID",
        COUNT(*) as copies
    FROM policies
    GROUP BY "Transaction ID"
)
SELECT 
    copies,
    COUNT(*) as transaction_ids_with_this_many_copies,
    copies * COUNT(*) as total_records
FROM dup_counts
GROUP BY copies
ORDER BY copies;

-- 3. Check demo user specifically
SELECT 'Demo user records:' as status;
SELECT 
    user_email,
    COUNT(*) as record_count,
    COUNT(DISTINCT "Transaction ID") as unique_transactions
FROM policies
WHERE user_email ILIKE '%demo%'
GROUP BY user_email;

-- 4. NUCLEAR OPTION - Remove ALL duplicates keeping only one of each Transaction ID
-- This will get you back to ~425 unique records
WITH duplicates_to_remove AS (
    SELECT _id
    FROM (
        SELECT 
            _id,
            "Transaction ID",
            ROW_NUMBER() OVER (
                PARTITION BY "Transaction ID" 
                ORDER BY 
                    -- Keep the most recently edited version
                    updated_at DESC
            ) as rn
        FROM policies
    ) ranked
    WHERE rn > 1
)
DELETE FROM policies
WHERE _id IN (SELECT _id FROM duplicates_to_remove);

-- 5. Verify we're back to normal
SELECT 'AFTER CLEANUP:' as status;
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT "Transaction ID") as unique_transactions
FROM policies;

-- 6. Verify demo user has correct count
SELECT 'Demo user after cleanup:' as status;
SELECT 
    COUNT(*) as demo_records
FROM policies
WHERE user_email ILIKE '%demo@agentcommission%';