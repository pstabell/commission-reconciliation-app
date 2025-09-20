-- Deep dive to find the missing 41 transactions

-- 1. First, what's the EXACT count for demo emails?
SELECT 'Exact demo email counts:' as check;
SELECT user_email, COUNT(*) as count
FROM policies
WHERE user_email IN (
    'demo@agentcommissiontracker.com',
    'Demo@AgentCommissionTracker.com',
    'DEMO@agentcommissiontracker.com',
    'Demo@agentcommissiontracker.com',
    'demo@AgentCommissionTracker.com'
)
GROUP BY user_email
ORDER BY user_email;

-- 2. Total of all the above
SELECT 'Total across all exact demo matches:' as check;
SELECT COUNT(*) as total
FROM policies
WHERE user_email IN (
    'demo@agentcommissiontracker.com',
    'Demo@AgentCommissionTracker.com',
    'DEMO@agentcommissiontracker.com',
    'Demo@agentcommissiontracker.com',
    'demo@AgentCommissionTracker.com'
);

-- 3. Check if any policies were deleted (check created_at dates)
SELECT 'Policies by creation date:' as check;
SELECT 
    DATE(created_at) as created_date,
    COUNT(*) as policies_created
FROM policies
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
  AND created_at IS NOT NULL
GROUP BY DATE(created_at)
ORDER BY created_date DESC
LIMIT 10;

-- 4. Check for any unusual user_email patterns
SELECT 'Check for spaces or special characters:' as check;
SELECT 
    user_email,
    LENGTH(user_email) as email_length,
    COUNT(*) as count
FROM policies
WHERE user_email LIKE '%demo%' 
   OR user_email LIKE '%Demo%'
   OR user_email LIKE '%DEMO%'
GROUP BY user_email, LENGTH(user_email)
ORDER BY email_length DESC;

-- 5. Historical check - were there ever 466?
SELECT 'Check updated_at for recent changes:' as check;
SELECT 
    DATE(updated_at) as updated_date,
    COUNT(*) as policies_updated
FROM policies
WHERE LOWER(user_email) LIKE '%demo%'
  AND updated_at > NOW() - INTERVAL '24 hours'
GROUP BY DATE(updated_at)
ORDER BY updated_date DESC;