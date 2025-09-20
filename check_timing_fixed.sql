-- CHECK WHEN DUPLICATES WERE CREATED (FIXED)

-- 1. Simple breakdown: Today vs Older
WITH duplicates AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC
        ) as rn
    FROM policies
),
categorized AS (
    SELECT 
        CASE 
            WHEN DATE(updated_at) = CURRENT_DATE THEN 'Today'
            WHEN DATE(updated_at) = CURRENT_DATE - INTERVAL '1 day' THEN 'Yesterday'
            WHEN DATE(updated_at) >= CURRENT_DATE - INTERVAL '7 days' THEN 'This Week'
            ELSE 'Older'
        END as when_created,
        "Transaction Type"
    FROM duplicates
    WHERE rn > 1
)
SELECT 
    when_created,
    COUNT(*) as duplicate_count,
    STRING_AGG(DISTINCT "Transaction Type", ', ') as transaction_types
FROM categorized
GROUP BY when_created
ORDER BY 
    CASE when_created
        WHEN 'Today' THEN 1
        WHEN 'Yesterday' THEN 2
        WHEN 'This Week' THEN 3
        ELSE 4
    END;

-- 2. Simpler count - just today vs not today
WITH duplicates AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC
        ) as rn
    FROM policies
)
SELECT 
    CASE 
        WHEN DATE(updated_at) = CURRENT_DATE THEN 'Created Today'
        ELSE 'Older Duplicates'
    END as category,
    COUNT(*) as count
FROM duplicates
WHERE rn > 1
GROUP BY 
    CASE 
        WHEN DATE(updated_at) = CURRENT_DATE THEN 'Created Today'
        ELSE 'Older Duplicates'
    END
ORDER BY category;

-- 3. Show recent duplicate examples
WITH duplicates AS (
    SELECT 
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
    updated_at::timestamp as duplicate_created_at,
    "Transaction Type",
    LEFT("Customer", 30) as customer
FROM duplicates
WHERE rn > 1 
  AND updated_at > NOW() - INTERVAL '24 hours'
ORDER BY updated_at DESC
LIMIT 10;

-- 4. Final count after removing ALL duplicates
SELECT COUNT(*) as current_total FROM policies;

WITH duplicates AS (
    SELECT 
        _id,
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC
        ) as rn
    FROM policies
)
SELECT COUNT(*) as after_removing_all_duplicates
FROM policies
WHERE _id NOT IN (
    SELECT _id FROM duplicates WHERE rn > 1
);