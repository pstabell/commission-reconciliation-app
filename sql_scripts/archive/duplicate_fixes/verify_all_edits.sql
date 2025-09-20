-- Verify all edited records

-- 1. Check Katie's records (original: Katie Oster)
SELECT 
    'Katie records:' as check;
SELECT 
    "Customer",
    "Policy Number",
    "Transaction ID"
FROM policies
WHERE "Policy Number" = '443939914'
   OR "Customer" LIKE '%Katie%'
   OR "Customer" LIKE '%Oster%'
   OR "Customer" LIKE '%Oyster%'
ORDER BY "Customer";

-- 2. Summary
SELECT 
    'Edit Summary:' as status;
SELECT 
    "Policy Number",
    "Customer",
    CASE 
        WHEN "Customer" = 'Katie Oyster' THEN '✅ Edit Saved'
        WHEN "Customer" = 'Lee Hopper' THEN '✅ Edit Saved'
        WHEN "Customer" = 'Pinnacle Investments LLC' THEN '✅ Edit Saved'
        ELSE 'Original'
    END as edit_status
FROM policies
WHERE "Policy Number" IN ('443939914', 'GD0031606030', '3AA823427')
ORDER BY "Policy Number";