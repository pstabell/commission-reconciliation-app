-- CHECK IF ENTIRE DATASET WAS DUPLICATED

-- 1. How many Transaction IDs have exactly 2 copies?
WITH duplicate_analysis AS (
    SELECT 
        "Transaction ID",
        COUNT(*) as copies
    FROM policies
    GROUP BY "Transaction ID"
)
SELECT 
    CASE 
        WHEN copies = 1 THEN 'Single (no duplicate)'
        WHEN copies = 2 THEN 'Exactly 2 copies'
        WHEN copies = 3 THEN 'Exactly 3 copies'
        WHEN copies = 4 THEN 'Exactly 4 copies'
        ELSE '5+ copies'
    END as status,
    COUNT(*) as transaction_ids,
    SUM(copies) as total_records
FROM duplicate_analysis
GROUP BY 
    CASE 
        WHEN copies = 1 THEN 'Single (no duplicate)'
        WHEN copies = 2 THEN 'Exactly 2 copies'
        WHEN copies = 3 THEN 'Exactly 3 copies'
        WHEN copies = 4 THEN 'Exactly 4 copies'
        ELSE '5+ copies'
    END
ORDER BY status;

-- 2. When were the duplicates created?
WITH first_and_duplicates AS (
    SELECT 
        "Transaction ID",
        MIN(updated_at) as first_update,
        MAX(updated_at) as last_update,
        COUNT(*) as copies
    FROM policies
    GROUP BY "Transaction ID"
    HAVING COUNT(*) > 1
)
SELECT 
    DATE_TRUNC('minute', last_update) as duplicate_created_at,
    COUNT(*) as duplicates_created_this_minute
FROM first_and_duplicates
WHERE DATE(last_update) = CURRENT_DATE
GROUP BY DATE_TRUNC('minute', last_update)
ORDER BY duplicate_created_at DESC
LIMIT 10;

-- 3. Show Katie's policy specifically
SELECT 
    _id,
    "Transaction ID",
    "Customer",
    updated_at
FROM policies
WHERE "Policy Number" = '443939914'
ORDER BY "Transaction ID", updated_at;