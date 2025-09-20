-- Find and remove duplicate transactions created by the Edit bug

-- 1. Find duplicates created in the last hour
SELECT 'Recently created duplicates:' as check;
WITH recent_duplicates AS (
    SELECT 
        p1."Transaction ID" as original_id,
        p2."Transaction ID" as duplicate_id,
        p1."Customer",
        p1."Policy Number",
        p1."Premium Sold",
        p1.updated_at as original_updated,
        p2.updated_at as duplicate_updated
    FROM policies p1
    JOIN policies p2 ON 
        p1."Customer" = p2."Customer" 
        AND p1."Policy Number" = p2."Policy Number"
        AND p1."Premium Sold" = p2."Premium Sold"
        AND p1."Effective Date" = p2."Effective Date"
        AND p1."Transaction ID" != p2."Transaction ID"
    WHERE p2.updated_at > NOW() - INTERVAL '1 hour'
        AND p1.updated_at < p2.updated_at
)
SELECT COUNT(*) as duplicate_count FROM recent_duplicates;

-- 2. Show sample of duplicates
WITH recent_duplicates AS (
    SELECT 
        p1."Transaction ID" as original_id,
        p2."Transaction ID" as duplicate_id,
        p1."Customer",
        p1."Policy Number",
        p2.updated_at as duplicate_updated
    FROM policies p1
    JOIN policies p2 ON 
        p1."Customer" = p2."Customer" 
        AND p1."Policy Number" = p2."Policy Number"
        AND p1."Premium Sold" = p2."Premium Sold"
        AND p1."Effective Date" = p2."Effective Date"
        AND p1."Transaction ID" != p2."Transaction ID"
    WHERE p2.updated_at > NOW() - INTERVAL '1 hour'
        AND p1.updated_at < p2.updated_at
)
SELECT * FROM recent_duplicates LIMIT 10;

-- 3. DELETE the duplicates (keeping the original)
-- IMPORTANT: Review the sample above before running this!
WITH duplicates_to_delete AS (
    SELECT p2._id
    FROM policies p1
    JOIN policies p2 ON 
        p1."Customer" = p2."Customer" 
        AND p1."Policy Number" = p2."Policy Number"
        AND p1."Premium Sold" = p2."Premium Sold"
        AND p1."Effective Date" = p2."Effective Date"
        AND p1."Transaction ID" != p2."Transaction ID"
    WHERE p2.updated_at > NOW() - INTERVAL '1 hour'
        AND p1.updated_at < p2.updated_at
)
DELETE FROM policies 
WHERE _id IN (SELECT _id FROM duplicates_to_delete);

-- 4. Verify the count is back to normal
SELECT 'Final count after cleanup:' as check;
SELECT COUNT(*) as total_policies FROM policies;