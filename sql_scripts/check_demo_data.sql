-- Check what demo data actually looks like

-- First, see if demo@example.com has ANY data
SELECT COUNT(*) as total_demo_records
FROM policies
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- Look at sample Transaction IDs for demo user
SELECT 
    "Transaction ID",
    "Transaction Type",
    "STMT DATE",
    reconciliation_id
FROM policies
WHERE user_email = 'Demo@AgentCommissionTracker.com'
LIMIT 20;

-- Check if there are any records that look like reconciliation entries
SELECT 
    "Transaction ID",
    "Transaction Type",
    reconciliation_id,
    "Agency Comm Received (STMT)"
FROM policies
WHERE 
    user_email = 'Demo@AgentCommissionTracker.com'
    AND "Agency Comm Received (STMT)" IS NOT NULL
LIMIT 10;

-- See all unique Transaction ID patterns
SELECT DISTINCT 
    CASE 
        WHEN "Transaction ID" LIKE '%-STMT-%' THEN 'STMT Pattern'
        WHEN "Transaction ID" LIKE '%-PMT-%' THEN 'PMT Pattern'
        WHEN "Transaction ID" IS NULL THEN 'NULL'
        ELSE 'Other Pattern'
    END as pattern_type,
    COUNT(*) as count
FROM policies
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY pattern_type;