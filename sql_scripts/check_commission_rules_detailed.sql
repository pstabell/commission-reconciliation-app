-- =====================================================
-- CHECK COMMISSION RULES - DETAILED ANALYSIS
-- =====================================================

-- 1. Check RLS status on commission_rules table
SELECT 
    'Commission Rules RLS Status:' as check,
    tablename,
    rowsecurity as rls_enabled,
    CASE 
        WHEN rowsecurity THEN '🔒 RLS ENABLED'
        ELSE '🔓 RLS DISABLED'
    END as status
FROM pg_tables 
WHERE tablename = 'commission_rules'
    AND schemaname = 'public';

-- 2. Count ALL commission rules in database
SELECT 
    'Total commission rules in database:' as info,
    COUNT(*) as count
FROM commission_rules;

-- 3. Check if rules have user_email values
SELECT 
    'Rules by user_email:' as info,
    COALESCE(user_email, 'NO EMAIL') as user_email,
    COUNT(*) as rule_count
FROM commission_rules
GROUP BY user_email
ORDER BY COUNT(*) DESC;

-- 4. Sample commission rules with details
SELECT 
    'Sample commission rules (first 5):' as info;
SELECT 
    cr.rule_id,
    c.carrier_name,
    cr.policy_type,
    cr.new_rate,
    cr.renewal_rate,
    cr.is_default,
    cr.user_email
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
LIMIT 5;

-- 5. Check for any RLS policies on commission_rules
SELECT 
    'RLS Policies on commission_rules:' as check;
SELECT 
    policyname,
    permissive,
    roles,
    cmd as operation,
    qual as policy_condition
FROM pg_policies
WHERE tablename = 'commission_rules'
ORDER BY policyname;

-- 6. Test what the app would see (simulate user query)
SELECT 
    'Testing filtered query (with user_email):' as test;
SELECT COUNT(*) as rules_with_your_email
FROM commission_rules 
WHERE user_email = 'patrick@stabell.net';  -- Replace with your actual email

-- 7. Test unfiltered query
SELECT 
    'Testing unfiltered query (what app sees without filter):' as test;
SELECT COUNT(*) as all_rules_visible
FROM commission_rules;