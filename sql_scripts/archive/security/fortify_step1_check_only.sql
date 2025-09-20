-- STEP 1: CHECK CURRENT STATE (SAFE - NO CHANGES)
-- Run this first to see what needs to be done

-- 1. Check if tables have user_email column
SELECT 'Current Table Structure:' as info;
SELECT 
    table_name,
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = t.table_name 
            AND column_name = 'user_email'
        ) THEN '✅ Has user_email'
        ELSE '❌ Missing user_email'
    END as user_email_status
FROM (
    VALUES ('carriers'), ('mgas'), ('carrier_mga_relationships'), ('commission_rules')
) AS t(table_name);

-- 2. Check current data counts
SELECT 'Current Data:' as info;
SELECT 'carriers' as table_name, COUNT(*) as total_records FROM carriers
UNION ALL
SELECT 'mgas', COUNT(*) FROM mgas
UNION ALL
SELECT 'commission_rules', COUNT(*) FROM commission_rules
ORDER BY table_name;

-- 3. Check if any records already have user_email
SELECT 'Records with user_email:' as info;
SELECT 
    'carriers' as table_name,
    COUNT(*) FILTER (WHERE user_email IS NOT NULL) as with_email,
    COUNT(*) FILTER (WHERE user_email IS NULL) as without_email
FROM carriers;

-- 4. List existing RLS policies (what will be dropped)
SELECT 'Existing RLS Policies to be replaced:' as info;
SELECT 
    tablename,
    policyname,
    CASE WHEN cmd = 'ALL' THEN '🔐 Full Access' 
         WHEN cmd = 'SELECT' THEN '👁️ Read Only'
         ELSE cmd END as access_type
FROM pg_policies
WHERE tablename IN ('carriers', 'mgas', 'carrier_mga_relationships', 'commission_rules')
ORDER BY tablename, policyname;

-- 5. Show what will happen
SELECT 'What the fortification script will do:' as info,
'1. Create backup tables (backup_carriers_20250118, etc.)' as step1,
'2. Add user_email column to carriers, mgas, relationships' as step2,
'3. Set all existing records to Demo user email' as step3,
'4. Drop old RLS policies and create new strict ones' as step4,
'5. Each user will only see their own data' as step5;