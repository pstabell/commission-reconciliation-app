-- Check email case sensitivity issue
-- The mobile shows: demo@agentcommissiontracker.com (all lowercase)
-- The desktop works with: Demo@AgentCommissionTracker.com

-- 1. Check what exact email is stored in policies
SELECT DISTINCT 
    user_email,
    COUNT(*) as record_count
FROM policies
WHERE LOWER(user_email) = LOWER('Demo@AgentCommissionTracker.com')
GROUP BY user_email;

-- 2. Check users table for email case
SELECT 
    email,
    subscription_status,
    created_at
FROM users
WHERE LOWER(email) = LOWER('Demo@AgentCommissionTracker.com');

-- 3. Verify the exact case-sensitive match
SELECT 
    'Exact match demo@agentcommissiontracker.com' as test,
    COUNT(*) as count
FROM policies  
WHERE user_email = 'demo@agentcommissiontracker.com'
UNION ALL
SELECT 
    'Exact match Demo@AgentCommissionTracker.com' as test,
    COUNT(*) as count
FROM policies
WHERE user_email = 'Demo@AgentCommissionTracker.com';