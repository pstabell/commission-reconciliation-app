-- Find potential duplicate policies created during edit

-- First, let's see the most recent transactions
SELECT "Transaction ID", 
       "Customer", 
       "Policy Number",
       "Premium Sold",
       "Effective Date",
       updated_at
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
ORDER BY updated_at DESC
LIMIT 50;

-- Find policies with identical key fields (likely duplicates)
WITH policy_groups AS (
    SELECT 
        "Customer",
        "Policy Number", 
        "Effective Date",
        "Premium Sold",
        COUNT(*) as duplicate_count,
        STRING_AGG("Transaction ID", ', ') as transaction_ids
    FROM policies
    WHERE user_email = 'demo@agentcommissiontracker.com'
    AND "Policy Number" IS NOT NULL
    GROUP BY "Customer", "Policy Number", "Effective Date", "Premium Sold"
    HAVING COUNT(*) > 1
)
SELECT * FROM policy_groups
ORDER BY duplicate_count DESC
LIMIT 20;

-- Count how many were updated recently (last 2 hours)
SELECT 
    DATE_TRUNC('hour', updated_at) as updated_hour,
    COUNT(*) as count
FROM policies  
WHERE user_email = 'demo@agentcommissiontracker.com'
AND updated_at > NOW() - INTERVAL '2 hours'
GROUP BY DATE_TRUNC('hour', updated_at)
ORDER BY updated_hour DESC;

-- Show total count
SELECT COUNT(*) as total_policies 
FROM policies 
WHERE user_email = 'demo@agentcommissiontracker.com';