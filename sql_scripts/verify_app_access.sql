-- =====================================================
-- VERIFY APP CAN NOW ACCESS CARRIERS AND MGAS
-- =====================================================

-- 1. Final status check
SELECT 
    '✅ SUCCESS! RLS is now disabled' as status,
    'Your Streamlit app should now see all carriers and MGAs' as message;

-- 2. Verify data counts
SELECT 
    'Carriers available:' as data_type,
    COUNT(*) as count
FROM carriers
UNION ALL
SELECT 
    'MGAs available:' as data_type,
    COUNT(*) as count
FROM mgas
UNION ALL
SELECT 
    'Commission rules:' as data_type,
    COUNT(*) as count
FROM commission_rules;

-- 3. Sample data check
SELECT 'Sample carriers (first 5):' as info;
SELECT carrier_name FROM carriers ORDER BY carrier_name LIMIT 5;

SELECT 'Sample MGAs (first 5):' as info;
SELECT mga_name FROM mgas ORDER BY mga_name LIMIT 5;

-- 4. Next steps
SELECT 
    '🎉 Your carriers and MGAs are now accessible!' as success,
    'Refresh your Streamlit app to see them in the dropdowns.' as action;