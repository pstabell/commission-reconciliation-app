-- Check RLS status on policies table
SELECT 
    tablename,
    rowsecurity as rls_enabled,
    CASE 
        WHEN rowsecurity THEN '🔒 RLS ENABLED - May block inserts'
        ELSE '🔓 RLS DISABLED - Inserts allowed'
    END as status
FROM pg_tables 
WHERE tablename = 'policies'
    AND schemaname = 'public';

-- Check existing RLS policies on policies table
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE tablename = 'policies'
    AND schemaname = 'public';

-- Check if the user email exists in users table
SELECT 
    email,
    subscription_status,
    created_at
FROM users
WHERE LOWER(email) = LOWER('Demo@AgentCommissionTracker.com');

-- If you need to disable RLS on policies table (USE WITH CAUTION):
-- ALTER TABLE policies DISABLE ROW LEVEL SECURITY;

-- Or create a policy that allows demo user to insert:
-- CREATE POLICY "demo_user_policy" ON policies
-- FOR ALL
-- TO authenticated
-- USING (user_email = 'Demo@AgentCommissionTracker.com' OR user_email = auth.email())
-- WITH CHECK (user_email = 'Demo@AgentCommissionTracker.com' OR user_email = auth.email());