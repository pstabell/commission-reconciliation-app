-- SAFE DUPLICATE REMOVAL APPROACH
-- Let's be very conservative and only remove obvious duplicates

-- 1. First, let's see what your transaction count SHOULD be
-- Count unique combinations that represent real transactions
WITH unique_transactions AS (
    SELECT DISTINCT
        "Customer",
        "Policy Number",
        "Transaction Type",
        "Effective Date",
        "Premium Sold"
    FROM policies
)
SELECT 
    COUNT(*) as unique_transaction_count,
    537 as current_total,
    537 - COUNT(*) as duplicates_to_remove
FROM unique_transactions;

-- 2. Identify EXACT duplicates (everything identical except maybe Transaction ID)
WITH ranked_transactions AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY 
                "Customer",
                "Policy Number", 
                "Transaction Type",
                "Effective Date",
                "Premium Sold",
                "Total Agent Comm"
            ORDER BY 
                CASE 
                    WHEN "Transaction ID" NOT LIKE '%\_2' ESCAPE '\' 
                     AND "Transaction ID" NOT LIKE '%(2)' 
                     AND "Transaction ID" NOT LIKE '%copy%' 
                    THEN 0 
                    ELSE 1 
                END,
                "Transaction ID"
        ) as rn
    FROM policies
)
SELECT 
    'Duplicates to remove:' as info,
    COUNT(*) as count
FROM ranked_transactions
WHERE rn > 1;

-- 3. Show what we'll keep vs remove
WITH ranked_transactions AS (
    SELECT 
        "Transaction ID",
        "Customer",
        "Policy Number",
        "Transaction Type",
        ROW_NUMBER() OVER (
            PARTITION BY 
                "Customer",
                "Policy Number", 
                "Transaction Type",
                "Effective Date",
                "Premium Sold",
                "Total Agent Comm"
            ORDER BY "Transaction ID"
        ) as rn
    FROM policies
)
SELECT 
    CASE WHEN rn = 1 THEN 'KEEP' ELSE 'REMOVE' END as action,
    "Transaction ID",
    LEFT("Customer", 30) as customer,
    LEFT("Policy Number", 15) as policy,
    "Transaction Type"
FROM ranked_transactions
WHERE ("Customer", "Policy Number") IN (
    SELECT "Customer", "Policy Number"
    FROM policies
    GROUP BY "Customer", "Policy Number"
    HAVING COUNT(*) > 2
)
ORDER BY "Customer", "Policy Number", rn
LIMIT 30;

-- 4. CONSERVATIVE REMOVAL - Only remove if ALL fields match
WITH exact_duplicates AS (
    SELECT 
        _id,
        ROW_NUMBER() OVER (
            PARTITION BY 
                "Customer",
                "Policy Number", 
                "Transaction Type",
                "Effective Date",
                "Premium Sold",
                "Total Agent Comm",
                "Broker Name",
                "Company Name"
            ORDER BY "Transaction ID"  -- Keep the one with simpler ID
        ) as rn
    FROM policies
)
DELETE FROM policies
WHERE _id IN (
    SELECT _id 
    FROM exact_duplicates 
    WHERE rn > 1
);

-- 5. Check final count
SELECT COUNT(*) as final_count FROM policies;