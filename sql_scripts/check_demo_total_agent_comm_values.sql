-- Check if Total Agent Comm field exists and has values for 2025 unreconciled

-- First, check column existence and values
SELECT 
    COUNT(*) as total_records,
    COUNT("Total Agent Comm") as has_column,
    COUNT(CASE WHEN "Total Agent Comm" IS NOT NULL AND "Total Agent Comm"::TEXT != '' THEN 1 END) as has_value,
    SUM(CASE 
        WHEN "Total Agent Comm" IS NULL OR "Total Agent Comm"::TEXT = '' THEN 0
        ELSE "Total Agent Comm"::NUMERIC
    END) as sum_total_agent_comm
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction Type" NOT IN ('PMT', 'ADJ')
    AND "Effective Date" >= '2025-01-01'
    AND "Effective Date" <= '2025-12-31'
    AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-STMT-%')
    AND (reconciliation_status IS NULL OR reconciliation_status = '');

-- Show sample records to see what fields exist
SELECT 
    "Policy Number",
    "Transaction Type",
    "Effective Date",
    "Premium Sold",
    "Agent Estimated Comm $",
    "Broker Fee",
    "Broker Fee Agent Comm",
    "Total Agent Comm",
    "Transaction ID",
    reconciliation_status
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Effective Date" >= '2025-01-01'
    AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-STMT-%')
    AND (reconciliation_status IS NULL OR reconciliation_status = '')
LIMIT 5;

-- Check if the column exists in the table schema
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'policies' 
AND column_name IN ('Total Agent Comm', 'Agent Estimated Comm $')
ORDER BY column_name;