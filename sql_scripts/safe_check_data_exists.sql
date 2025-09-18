-- SAFELY CHECK IF DATA EXISTS (NO DESTRUCTIVE OPERATIONS)
-- Run this in Supabase SQL Editor

-- 1. Simple count with current permissions
SELECT 'Current User View' as check_type;
SELECT 'Carriers I can see:' as item, COUNT(*) as count FROM carriers;
SELECT 'MGAs I can see:' as item, COUNT(*) as count FROM mgas;
SELECT 'Commission rules I can see:' as item, COUNT(*) as count FROM commission_rules;
SELECT 'Relationships I can see:' as item, COUNT(*) as count FROM carrier_mga_relationships;

-- 2. Check RLS status on tables
SELECT 'RLS Status Check' as check_type;
SELECT 
    tablename,
    rowsecurity as rls_enabled,
    CASE 
        WHEN rowsecurity THEN '🔒 RLS is ON' 
        ELSE '🔓 RLS is OFF' 
    END as status
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('carriers', 'mgas', 'commission_rules', 'carrier_mga_relationships')
ORDER BY tablename;

-- 3. Check if commission_rules has user_email column
SELECT 'Table Structure Check' as check_type;
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
AND table_name = 'commission_rules'
AND column_name = 'user_email';

-- 4. If you're logged in as demo, check specifically for demo data
SELECT 'Demo User Data Check' as check_type;
SELECT 
    'Commission rules for demo user:' as item,
    COUNT(*) as count 
FROM commission_rules 
WHERE user_email IN ('demo@agentcommissiontracker.com', 'Demo@AgentCommissionTracker.com');

-- 5. Check if tables have any RLS policies defined
SELECT 'RLS Policies Check' as check_type;
SELECT 
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual
FROM pg_policies
WHERE schemaname = 'public'
AND tablename IN ('carriers', 'mgas', 'commission_rules', 'carrier_mga_relationships')
ORDER BY tablename, policyname;