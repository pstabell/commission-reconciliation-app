-- Inspect the "OTHER" policies to understand what they do
SELECT 
    policyname,
    cmd as operation,
    roles,
    qual as using_clause,
    with_check as with_check_clause
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename = 'policies'
AND policyname IN ('Service role has full access to policies', 'Users see only their own data')
ORDER BY policyname;

-- Also check if "Users see only their own data" uses user_email or user_id
SELECT 
    policyname,
    cmd,
    CASE 
        WHEN qual LIKE '%user_email%' THEN 'USES user_email - needs removal'
        WHEN qual LIKE '%user_id%' THEN 'USES user_id - keep it'
        WHEN qual IS NULL THEN 'No filter'
        ELSE 'Check manually: ' || qual
    END as filter_analysis
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename = 'policies'
AND policyname = 'Users see only their own data';