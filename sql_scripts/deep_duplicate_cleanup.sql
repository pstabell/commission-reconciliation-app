-- DEEP DUPLICATE CLEANUP - Remove duplicates based on business logic, not just Transaction ID

-- 1. Current total
SELECT COUNT(*) as current_total FROM policies;

-- 2. Find all duplicates based on business keys (not Transaction ID)
WITH duplicates AS (
    SELECT 
        _id,
        "Transaction ID",
        "Customer",
        "Policy Number",
        "Transaction Type",
        "Effective Date",
        COALESCE("Premium Sold", 0) as premium,
        ROW_NUMBER() OVER (
            PARTITION BY 
                "Customer",
                "Policy Number",
                "Transaction Type",
                "Effective Date",
                COALESCE("Premium Sold", 0)
            ORDER BY 
                "Transaction ID"  -- Keep the first one alphabetically
        ) as rn
    FROM policies
)
SELECT 
    'Duplicates to remove:' as info,
    COUNT(*) as count
FROM duplicates
WHERE rn > 1;

-- 3. Preview what we'll remove
WITH duplicates AS (
    SELECT 
        _id,
        "Transaction ID",
        "Customer",
        "Policy Number",
        "Transaction Type",
        "Effective Date",
        ROW_NUMBER() OVER (
            PARTITION BY 
                "Customer",
                "Policy Number",
                "Transaction Type",
                "Effective Date",
                COALESCE("Premium Sold", 0)
            ORDER BY 
                "Transaction ID"
        ) as rn
    FROM policies
)
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Transaction Type",
    CASE WHEN rn = 1 THEN 'KEEP' ELSE 'REMOVE' END as action
FROM duplicates
WHERE "Customer" = 'Perfect Lanais LLC'
ORDER BY "Customer", "Policy Number", "Transaction Type", "Effective Date", rn;

-- 4. REMOVE the duplicates
WITH duplicates_to_remove AS (
    SELECT _id
    FROM (
        SELECT 
            _id,
            ROW_NUMBER() OVER (
                PARTITION BY 
                    "Customer",
                    "Policy Number",
                    "Transaction Type",
                    "Effective Date",
                    COALESCE("Premium Sold", 0)
                ORDER BY 
                    "Transaction ID"
            ) as rn
        FROM policies
    ) d
    WHERE rn > 1
)
DELETE FROM policies
WHERE _id IN (SELECT _id FROM duplicates_to_remove);

-- 5. Final count
SELECT COUNT(*) as final_count FROM policies;

-- 6. Verify Perfect Lanais now has correct count
SELECT 
    "Customer",
    COUNT(*) as transaction_count
FROM policies
WHERE "Customer" IN ('Perfect Lanais LLC', 'Deborah Cordette', 'Quantum 26 Enterprises, Inc.')
GROUP BY "Customer"
ORDER BY "Customer";