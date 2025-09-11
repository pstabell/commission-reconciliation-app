-- =====================================================
-- FIX COMMISSION RULES ACCESS - DISABLE RLS
-- =====================================================

-- 1. Check current RLS status on commission_rules
SELECT 
    'Current status:' as info,
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables 
WHERE tablename = 'commission_rules';

-- 2. DISABLE RLS on commission_rules table
ALTER TABLE commission_rules DISABLE ROW LEVEL SECURITY;

-- 3. Verify RLS is now disabled
SELECT 
    'After fix:' as info,
    tablename,
    rowsecurity as rls_enabled,
    CASE 
        WHEN rowsecurity THEN '🔒 Still blocked'
        ELSE '🔓 Fixed! Rules should now be visible'
    END as status
FROM pg_tables 
WHERE tablename = 'commission_rules';

-- 4. Confirm you can see your rules
SELECT 
    '✅ You have ' || COUNT(*) || ' commission rules ready to use!' as success
FROM commission_rules;

-- 5. Show sample rules to confirm
SELECT 
    c.carrier_name,
    cr.policy_type,
    cr.new_rate || '% / ' || cr.renewal_rate || '%' as rates
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
ORDER BY c.carrier_name
LIMIT 5;