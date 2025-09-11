-- =====================================================
-- CHECK WHAT CARRIERS AND MGAs YOU ALREADY HAVE
-- =====================================================

-- 1. Count carriers
SELECT COUNT(*) as carrier_count FROM carriers;

-- 2. List all existing carriers
SELECT 
    carrier_name,
    status,
    created_at
FROM carriers
ORDER BY carrier_name;

-- 3. List all existing MGAs (you have 16)
SELECT 
    mga_name,
    status,
    created_at
FROM mgas
ORDER BY mga_name;

-- 4. Check which carriers from our insert list are MISSING
WITH needed_carriers AS (
    SELECT * FROM (VALUES 
        ('AAA'),
        ('Allrisk'),
        ('American Integrity'),
        ('American Traditions'),
        ('Progressive'),
        ('Citizens'),
        ('Mercury'),
        ('State Farm')
    ) AS t(carrier_name)
)
SELECT 
    nc.carrier_name as missing_carrier
FROM needed_carriers nc
LEFT JOIN carriers c ON nc.carrier_name = c.carrier_name
WHERE c.carrier_name IS NULL
ORDER BY nc.carrier_name;

-- 5. Summary - Can you see the data?
SELECT 
    'You CAN see carriers/MGAs in the database!' as status,
    'The issue might be in the Streamlit app connection' as possible_issue;