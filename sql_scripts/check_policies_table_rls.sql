-- Check RLS policies specifically on the policies table
SELECT 
    policyname,
    cmd as operation,
    roles,
    qual as using_clause,
    with_check as with_check_clause
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename = 'policies'
ORDER BY policyname;

-- Also check if we have both old and new policies
SELECT 
    CASE 
        WHEN policyname LIKE '%user_id%' THEN 'NEW (user_id based)'
        WHEN policyname LIKE '%user_email%' OR policyname LIKE 'Anyone can%' THEN 'OLD (user_email based)'
        ELSE 'OTHER'
    END as policy_type,
    COUNT(*) as count,
    STRING_AGG(policyname || ' (' || cmd || ')', ', ' ORDER BY policyname) as policies
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename = 'policies'
GROUP BY policy_type
ORDER BY policy_type;