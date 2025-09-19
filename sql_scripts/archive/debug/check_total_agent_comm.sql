-- Check if Total Agent Comm field exists and has values

-- First, check what commission fields exist for 2025 unreconciled
SELECT 
    COUNT(*) as total_2025_unreconciled,
    SUM(COALESCE("Agent Estimated Comm $"::NUMERIC, 0)) as agent_estimated_sum,
    SUM(COALESCE("Total Agent Comm"::NUMERIC, 0)) as total_agent_comm_sum,
    SUM(COALESCE("Broker Fee Agent Comm"::NUMERIC, 0)) as broker_fee_sum
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction Type" NOT IN ('PMT', 'ADJ')
    AND "Effective Date" >= '2025-01-01'
    AND "Effective Date" <= '2025-12-31'
    AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-STMT-%')
    AND ("reconciliation_status" IS NULL OR "reconciliation_status" = '');

-- Show sample to see the difference
SELECT 
    "Policy Number",
    "Transaction Type",
    "Premium Sold",
    "Agent Estimated Comm $",
    "Broker Fee",
    "Broker Fee Agent Comm",
    "Total Agent Comm"
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Effective Date" >= '2025-01-01'
    AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-STMT-%')
LIMIT 10;