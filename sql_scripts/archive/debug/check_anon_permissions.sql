-- CHECK ANON KEY PERMISSIONS

-- 1. Check current user/role
SELECT 'CURRENT DATABASE USER:' as info;
SELECT current_user, current_role;

-- 2. Check if anon role has SELECT permission on carriers
SELECT '';
SELECT 'ANON PERMISSIONS ON CARRIERS:' as info;
SELECT 
    grantee,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'public' 
AND table_name = 'carriers'
AND grantee IN ('anon', 'authenticated', 'public')
ORDER BY grantee, privilege_type;

-- 3. Grant permissions if missing
GRANT SELECT ON carriers TO anon;
GRANT SELECT ON mgas TO anon;
GRANT SELECT ON commission_rules TO anon;
GRANT SELECT ON carrier_mga_relationships TO anon;

-- 4. Verify grants worked
SELECT '';
SELECT 'AFTER GRANT - ANON PERMISSIONS:' as info;
SELECT 
    table_name,
    string_agg(privilege_type, ', ') as privileges
FROM information_schema.table_privileges
WHERE table_schema = 'public' 
AND table_name IN ('carriers', 'mgas', 'commission_rules', 'carrier_mga_relationships')
AND grantee = 'anon'
GROUP BY table_name
ORDER BY table_name;

-- 5. Test as anon would see
SET ROLE anon;
SELECT '';
SELECT 'AS ANON - DEMO CARRIERS COUNT:' as info;
SELECT COUNT(*) as visible_carriers
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- Reset role
RESET ROLE;

-- 6. Final check
SELECT '';
SELECT 'PERMISSIONS FIXED:' as info;
SELECT 'Please refresh the app and try again' as action;