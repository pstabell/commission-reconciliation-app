-- Debug Mobile Demo Issue
-- Run this in Supabase SQL Editor to verify Demo user data

-- 1. Check exact email matches
SELECT 
    user_email,
    COUNT(*) as record_count,
    MIN(created_at) as first_record,
    MAX(created_at) as last_record
FROM policies
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY user_email;

-- 2. Check case variations
SELECT DISTINCT 
    user_email,
    COUNT(*) as count
FROM policies
WHERE LOWER(user_email) = LOWER('Demo@AgentCommissionTracker.com')
GROUP BY user_email
ORDER BY user_email;

-- 3. Check all user emails to see if Demo exists with different casing
SELECT 
    user_email,
    COUNT(*) as record_count
FROM policies
WHERE user_email ILIKE '%demo%'
GROUP BY user_email
ORDER BY user_email;

-- 4. Sample some Demo records to verify they exist
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Effective Date",
    user_email,
    created_at
FROM policies
WHERE user_email = 'Demo@AgentCommissionTracker.com'
LIMIT 10;

-- 5. Check RLS policies on policies table
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
ORDER BY policyname;

-- 6. Test what anon role can see
-- This simulates what the app sees when using anon key
SET ROLE anon;
SELECT COUNT(*) as visible_count 
FROM policies 
WHERE user_email = 'Demo@AgentCommissionTracker.com';
RESET ROLE;

-- 7. Check if there are any recent changes to Demo data
SELECT 
    DATE(created_at) as date,
    COUNT(*) as records_added
FROM policies
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY DATE(created_at)
ORDER BY DATE(created_at) DESC
LIMIT 7;