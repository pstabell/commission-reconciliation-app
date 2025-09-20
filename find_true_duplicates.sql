-- FIND TRUE DUPLICATES BASED ON TRANSACTION ID PATTERNS
-- Since all show updated today, let's use Transaction ID patterns

-- 1. Analyze Transaction ID format to find duplicates
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Transaction Type",
    updated_at
FROM policies
WHERE "Policy Number" IN (
    SELECT "Policy Number"
    FROM policies
    GROUP BY "Policy Number"
    HAVING COUNT(*) > 2
)
ORDER BY "Policy Number", "Transaction ID"
LIMIT 30;

-- 2. Look for Transaction IDs that might be duplicates (e.g., ABC123 vs ABC123_2)
WITH id_analysis AS (
    SELECT 
        "Transaction ID",
        "Customer",
        "Policy Number",
        "Transaction Type",
        CASE 
            WHEN "Transaction ID" LIKE '%\_2' ESCAPE '\' THEN 'Possible Duplicate'
            WHEN "Transaction ID" LIKE '%\_copy' ESCAPE '\' THEN 'Possible Duplicate'
            WHEN "Transaction ID" LIKE '%(2)' THEN 'Possible Duplicate'
            WHEN "Transaction ID" LIKE '%\_dup%' ESCAPE '\' THEN 'Possible Duplicate'
            ELSE 'Original'
        END as id_status
    FROM policies
)
SELECT 
    id_status,
    COUNT(*) as count
FROM id_analysis
GROUP BY id_status;

-- 3. Find groups where we have multiple transactions for same policy/type/date
WITH transaction_groups AS (
    SELECT 
        "Customer",
        "Policy Number",
        "Transaction Type",
        "Effective Date",
        COUNT(*) as duplicate_count,
        ARRAY_AGG("Transaction ID" ORDER BY "Transaction ID") as transaction_ids,
        ARRAY_AGG("Premium Sold" ORDER BY "Transaction ID") as premiums,
        ARRAY_AGG("Total Agent Comm" ORDER BY "Transaction ID") as commissions
    FROM policies
    GROUP BY "Customer", "Policy Number", "Transaction Type", "Effective Date"
    HAVING COUNT(*) > 1
)
SELECT 
    LEFT("Customer", 30) as customer,
    LEFT("Policy Number", 20) as policy,
    "Transaction Type",
    duplicate_count,
    transaction_ids[1] as first_id,
    transaction_ids[2] as second_id,
    premiums[1] = premiums[2] as same_premium,
    commissions[1] = commissions[2] as same_commission
FROM transaction_groups
ORDER BY duplicate_count DESC, "Customer", "Policy Number"
LIMIT 20;

-- 4. Final recommendation: Count of definite duplicates
WITH definite_duplicates AS (
    SELECT 
        p1."Transaction ID" as keep_id,
        p2."Transaction ID" as remove_id
    FROM policies p1
    JOIN policies p2 ON 
        p1."Customer" = p2."Customer"
        AND p1."Policy Number" = p2."Policy Number" 
        AND p1."Transaction Type" = p2."Transaction Type"
        AND p1."Effective Date" = p2."Effective Date"
        AND p1."Premium Sold" = p2."Premium Sold"
        AND p1."Total Agent Comm" = p2."Total Agent Comm"
        AND p1."Transaction ID" < p2."Transaction ID"  -- Keep the first one alphabetically
)
SELECT 
    COUNT(*) as definite_duplicates_to_remove,
    537 - COUNT(*) as final_count_after_removal
FROM definite_duplicates;