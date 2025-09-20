-- Find potential duplicate policies created during edit
-- These would have similar data but different Transaction IDs

-- First, let's see the most recent transactions
SELECT "Transaction ID", 
       "Customer Name", 
       "Policy Number",
       "Premium Sold",
       "Effective Date",
       created_at
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
ORDER BY created_at DESC
LIMIT 20;

-- Find policies with identical key fields (likely duplicates)
WITH policy_groups AS (
    SELECT 
        "Customer Name",
        "Policy Number", 
        "Effective Date",
        "Premium Sold",
        COUNT(*) as duplicate_count,
        STRING_AGG("Transaction ID", ', ') as transaction_ids,
        STRING_AGG(created_at::text, ', ') as created_dates
    FROM policies
    WHERE user_email = 'demo@agentcommissiontracker.com'
    AND "Policy Number" IS NOT NULL
    GROUP BY "Customer Name", "Policy Number", "Effective Date", "Premium Sold"
    HAVING COUNT(*) > 1
)
SELECT * FROM policy_groups
ORDER BY duplicate_count DESC;

-- Count how many were created today
SELECT 
    DATE(created_at) as created_date,
    COUNT(*) as count
FROM policies  
WHERE user_email = 'demo@agentcommissiontracker.com'
AND DATE(created_at) = CURRENT_DATE
GROUP BY DATE(created_at);