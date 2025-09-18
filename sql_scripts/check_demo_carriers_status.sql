-- Check demo user's carriers and their status values
-- This will help debug why "No carriers found" is showing

-- 1. Count total carriers for demo user
SELECT COUNT(*) as total_carriers
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Check status distribution
SELECT 
    status,
    COUNT(*) as count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY status
ORDER BY count DESC;

-- 3. Show sample carriers with all fields to see what's missing
SELECT 
    carrier_id,
    carrier_name,
    status,
    updated_at,
    created_at
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name
LIMIT 10;

-- 4. Check if any carriers have NULL or empty status
SELECT 
    carrier_id,
    carrier_name,
    status,
    CASE 
        WHEN status IS NULL THEN 'NULL status'
        WHEN status = '' THEN 'Empty string'
        WHEN status = 'Active' THEN 'Active (correct)'
        ELSE CONCAT('Other: ', status)
    END as status_check
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND (status IS NULL OR status != 'Active')
LIMIT 20;

-- 5. Check if there are any Active carriers at all
SELECT 
    carrier_id,
    carrier_name,
    status,
    updated_at
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND status = 'Active'
LIMIT 10;