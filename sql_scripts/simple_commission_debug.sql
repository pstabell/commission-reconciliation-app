-- Simple debug for Agent Commission Due
-- Expected: $9,842.93, Currently showing: ~$2,545.75

-- 1. Basic totals
SELECT 
    SUM(CAST("Total Agent Comm" AS NUMERIC)) as total_commission,
    SUM(CAST("Agent Paid Amount (STMT)" AS NUMERIC)) as total_paid,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) - SUM(CAST("Agent Paid Amount (STMT)" AS NUMERIC)) as commission_due
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Transaction Type" NOT IN ('CAN', 'XCL');

-- 2. Check if Agent Estimated Comm $ has values
SELECT 
    COUNT(*) as total_records,
    COUNT(CASE WHEN "Agent Estimated Comm $" IS NOT NULL THEN 1 END) as records_with_agent_comm,
    SUM(CAST("Agent Estimated Comm $" AS NUMERIC)) as sum_agent_comm,
    SUM(CAST("Broker Fee Agent Comm" AS NUMERIC)) as sum_broker_fee_comm
FROM policies  
WHERE user_email = 'demo@agentcommissiontracker.com';

-- 3. Sample records to see values
SELECT 
    "Transaction ID",
    "Customer",
    "Premium Sold",
    "Agent Estimated Comm $",
    "Broker Fee Agent Comm",
    "Total Agent Comm"
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
LIMIT 10;