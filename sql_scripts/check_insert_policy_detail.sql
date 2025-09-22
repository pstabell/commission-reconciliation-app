-- Check the INSERT policy in detail
SELECT 
    policyname,
    cmd,
    roles,
    qual as using_clause,
    with_check as with_check_clause
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename = 'policies'
AND policyname = 'Insert by user_id';

-- For INSERT policies, the check should be in with_check, not qual
-- qual (USING) is for existing rows, with_check is for new rows being inserted