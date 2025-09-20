-- Find potential duplicate policies created during edit
-- These would have similar data but different Transaction IDs

-- First, let's see the most recent transactions
SELECT "Transaction ID", 
       customer, 
       "Policy Number",
       "Premium Sold",
       "Effective Date",
       created_at
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
ORDER BY created_at DESC
LIMIT 50;

-- Find policies with identical key fields (likely duplicates)
WITH policy_groups AS (
    SELECT 
        customer,
        "Policy Number", 
        "Effective Date",
        "Premium Sold",
        COUNT(*) as duplicate_count,
        STRING_AGG("Transaction ID", ', ') as transaction_ids,
        STRING_AGG(created_at::text, ', ') as created_dates
    FROM policies
    WHERE user_email = 'demo@agentcommissiontracker.com'
    AND "Policy Number" IS NOT NULL
    GROUP BY customer, "Policy Number", "Effective Date", "Premium Sold"
    HAVING COUNT(*) > 1
)
SELECT * FROM policy_groups
ORDER BY duplicate_count DESC
LIMIT 20;

-- Count how many were created recently (last hour)
SELECT 
    DATE_TRUNC('hour', created_at) as created_hour,
    COUNT(*) as count
FROM policies  
WHERE user_email = 'demo@agentcommissiontracker.com'
AND created_at > NOW() - INTERVAL '2 hours'
GROUP BY DATE_TRUNC('hour', created_at)
ORDER BY created_hour DESC;

-- Show total count
SELECT COUNT(*) as total_policies 
FROM policies 
WHERE user_email = 'demo@agentcommissiontracker.com';