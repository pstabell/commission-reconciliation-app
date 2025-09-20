-- FINAL VERIFICATION - Ensure we have exactly 425 records with no duplicates

-- 1. Total count
SELECT 
    '1. TOTAL RECORD COUNT' as check_type,
    COUNT(*) as count,
    CASE 
        WHEN COUNT(*) = 425 THEN '✅ CORRECT' 
        ELSE '❌ INCORRECT - Expected 425' 
    END as status
FROM policies;

-- 2. Check for ANY duplicate Transaction IDs
SELECT 
    '2. DUPLICATE CHECK' as check_type,
    COUNT(*) as duplicate_transaction_ids,
    CASE 
        WHEN COUNT(*) = 0 THEN '✅ NO DUPLICATES' 
        ELSE '❌ DUPLICATES FOUND' 
    END as status
FROM (
    SELECT "Transaction ID"
    FROM policies
    GROUP BY "Transaction ID"
    HAVING COUNT(*) > 1
) dup;

-- 3. Show any remaining duplicates (should be none)
SELECT 
    "Transaction ID",
    COUNT(*) as occurrences,
    STRING_AGG("Customer", ', ' ORDER BY "Customer") as customers
FROM policies
GROUP BY "Transaction ID"
HAVING COUNT(*) > 1
LIMIT 5;

-- 4. Verify our edited records are correct
SELECT 
    '4. EDITED RECORDS CHECK' as check_type;

SELECT 
    "Policy Number",
    "Transaction ID",
    "Customer",
    CASE 
        WHEN "Customer" IN ('Katie Oyster', 'Lee Hopper') THEN '✅ Correctly Edited'
        WHEN "Customer" IN ('Katie Ostor', 'Katie Oystor', 'Lee Hope May') THEN '❌ Old/Incorrect Version'
        ELSE 'Not an edited record'
    END as edit_status
FROM policies
WHERE "Policy Number" IN ('443939914', 'GD0031606030')
ORDER BY "Policy Number", "Transaction ID";

-- 5. Summary by customer (top 10)
SELECT 
    '5. CUSTOMER TRANSACTION COUNTS' as check_type;

SELECT 
    "Customer",
    COUNT(*) as transaction_count,
    CASE 
        WHEN "Customer" = 'Perfect Lanais LLC' AND COUNT(*) = 13 THEN '✅'
        WHEN "Customer" = 'Deborah Cordette' AND COUNT(*) = 11 THEN '✅'
        ELSE ''
    END as expected
FROM policies
GROUP BY "Customer"
ORDER BY COUNT(*) DESC
LIMIT 10;