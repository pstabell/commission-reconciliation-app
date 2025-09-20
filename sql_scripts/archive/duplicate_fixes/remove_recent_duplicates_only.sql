-- TARGETED DUPLICATE REMOVAL - Only Recent Duplicates from Edit Bug
-- This focuses on duplicates created in the last 24 hours

-- STEP 1: Check duplicates created TODAY only
WITH recent_duplicates AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC  -- Keep the oldest
        ) as rn
    FROM policies
    WHERE updated_at > CURRENT_DATE  -- Only today's updates
)
SELECT 
    COUNT(*) as todays_duplicates_to_remove
FROM recent_duplicates
WHERE rn > 1;

-- STEP 2: Show what was edited today that created duplicates
WITH recent_activity AS (
    SELECT 
        "Customer",
        "Policy Number",
        COUNT(*) as count,
        MIN(updated_at) as first_update,
        MAX(updated_at) as last_update
    FROM policies
    WHERE updated_at > CURRENT_DATE
    GROUP BY "Customer", "Policy Number"
    HAVING COUNT(*) > 1
)
SELECT * FROM recent_activity
ORDER BY count DESC
LIMIT 10;

-- STEP 3: More precise duplicate check - same transaction with recent edits
WITH duplicate_pairs AS (
    SELECT 
        p1."Transaction ID" as original_id,
        p2."Transaction ID" as duplicate_id,
        p1."Customer",
        p1."Policy Number",
        p1."Transaction Type",
        p1.updated_at as original_date,
        p2.updated_at as duplicate_date
    FROM policies p1
    JOIN policies p2 ON 
        p1."Customer" = p2."Customer" 
        AND p1."Policy Number" = p2."Policy Number"
        AND p1."Transaction Type" = p2."Transaction Type"
        AND p1."Premium Sold" = p2."Premium Sold"
        AND p1."Effective Date" = p2."Effective Date"
        AND p1._id < p2._id  -- Ensure we only get each pair once
    WHERE p2.updated_at > CURRENT_DATE  -- Duplicate created today
      AND p1.updated_at < p2.updated_at  -- Original is older
)
SELECT COUNT(*) as edit_bug_duplicates FROM duplicate_pairs;

-- STEP 4: DELETE only the recent duplicates from the Edit bug
WITH duplicates_to_remove AS (
    SELECT p2._id
    FROM policies p1
    JOIN policies p2 ON 
        p1."Customer" = p2."Customer" 
        AND p1."Policy Number" = p2."Policy Number"
        AND p1."Transaction Type" = p2."Transaction Type"
        AND p1."Premium Sold" = p2."Premium Sold"
        AND p1."Effective Date" = p2."Effective Date"
        AND p1._id < p2._id
    WHERE p2.updated_at > CURRENT_DATE
      AND p1.updated_at < p2.updated_at
)
DELETE FROM policies 
WHERE _id IN (SELECT _id FROM duplicates_to_remove);

-- STEP 5: Final verification
SELECT COUNT(*) as final_count FROM policies;