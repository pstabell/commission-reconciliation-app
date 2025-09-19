-- Check carrier status values for demo user

-- Count carriers by status for demo user
SELECT 
    status,
    COUNT(*) as count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY status
ORDER BY count DESC;

-- Check if there are any Active carriers (case-sensitive check)
SELECT 
    carrier_id,
    carrier_name,
    status,
    user_email
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
    AND status = 'Active'
LIMIT 10;

-- Check all unique status values in carriers table
SELECT DISTINCT status
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- Sample of carriers to see actual status values
SELECT 
    carrier_id,
    carrier_name,
    status,
    created_at
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY created_at DESC
LIMIT 10;