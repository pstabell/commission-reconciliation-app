-- FIX FOR CUSTOM AUTH - Your app doesn't use Supabase Auth!
-- The RLS policies above won't work because auth.email() is NULL

-- 1. Since your app uses custom authentication, we need different RLS policies
-- Drop the JWT-based policies
DROP POLICY IF EXISTS "Users see only own carriers" ON carriers;
DROP POLICY IF EXISTS "Users see only own mgas" ON mgas;
DROP POLICY IF EXISTS "Users see only own relationships" ON carrier_mga_relationships;
DROP POLICY IF EXISTS "Users see only own commission rules" ON commission_rules;

-- 2. For now, disable RLS until we implement proper policies for custom auth
ALTER TABLE carriers DISABLE ROW LEVEL SECURITY;
ALTER TABLE mgas DISABLE ROW LEVEL SECURITY;
ALTER TABLE carrier_mga_relationships DISABLE ROW LEVEL SECURITY;
ALTER TABLE commission_rules DISABLE ROW LEVEL SECURITY;

-- 3. The app will need to handle filtering by adding WHERE user_email = session['user_email']
-- This provides security at the application level instead of database level

SELECT 'Security Model:' as info, 'Application-level filtering by user_email' as approach;

-- 4. Show the current state
SELECT 'User Data Isolation Status:' as check;
SELECT 
    tablename,
    CASE 
        WHEN rowsecurity THEN 'RLS Enabled' 
        ELSE 'RLS Disabled - App handles security' 
    END as security_model
FROM pg_tables 
WHERE tablename IN ('carriers', 'mgas', 'carrier_mga_relationships', 'commission_rules')
ORDER BY tablename;