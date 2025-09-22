-- Debug why Agent Commission Due is still low
-- Should be $9,842.93 but showing ~$2,545.75

-- 1. Check Total Agent Comm after update
SELECT 'After Update - Total Agent Comm Check:' as analysis;
SELECT 
    COUNT(*) as total_records,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) as sum_total_agent_comm,
    SUM(CAST("Agent Estimated Comm $" AS NUMERIC)) as sum_agent_estimated,
    SUM(CAST("Broker Fee Agent Comm" AS NUMERIC)) as sum_broker_fee,
    SUM(CAST("Agent Paid Amount (STMT)" AS NUMERIC)) as sum_paid
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com';

-- 2. Calculate Agent Commission Due by transaction type
SELECT 'Commission Due by Transaction Type:' as analysis;
SELECT 
    "Transaction Type",
    COUNT(*) as count,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) as total_comm,
    SUM(CAST("Agent Paid Amount (STMT)" AS NUMERIC)) as total_paid,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) - SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as balance_due
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
GROUP BY "Transaction Type"
ORDER BY "Transaction Type";

-- 3. Check for excluded transactions
SELECT 'Excluded Transaction Types (CAN/XCL):' as analysis;
SELECT 
    "Transaction Type",
    COUNT(*) as count,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) as excluded_comm
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Transaction Type" IN ('CAN', 'XCL')
GROUP BY "Transaction Type";

-- 4. Check Agent Comm % values
SELECT 'Agent Comm % Analysis:' as analysis;
SELECT 
    COUNT(*) as total_records,
    COUNT("Agent Comm %") as records_with_agent_comm_percent,
    AVG(CASE WHEN "Agent Comm %" ~ '^[0-9.]+$' THEN CAST("Agent Comm %" AS NUMERIC) ELSE NULL END) as avg_agent_comm_percent
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com';

-- 5. Sample records to see the calculation
SELECT 'Sample Records with Calculations:' as analysis;
SELECT 
    "Transaction ID",
    "Transaction Type",
    "Premium Sold",
    "Policy Gross Comm %",
    "Agent Comm %",
    "Agent Estimated Comm $",
    "Broker Fee",
    "Broker Fee Agent Comm",
    "Total Agent Comm",
    "Agent Paid Amount (STMT)"
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Total Agent Comm" IS NOT NULL
LIMIT 10;

-- 6. Final calculation - what should Agent Commission Due be?
SELECT 'Final Agent Commission Due Calculation:' as analysis;
WITH calculated_totals AS (
    SELECT 
        SUM(CAST("Total Agent Comm" AS NUMERIC)) as total_commission,
        SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_paid,
        COUNT(*) as record_count
    FROM policies
    WHERE user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction Type" NOT IN ('CAN', 'XCL')
)
SELECT 
    total_commission,
    total_paid,
    total_commission - total_paid as agent_commission_due,
    record_count
FROM calculated_totals;

-- 7. Check if Agent Estimated Comm $ is populated
SELECT 'Agent Estimated Comm $ Status:' as analysis;
SELECT 
    COUNT(*) as total_records,
    SUM(CASE WHEN "Agent Estimated Comm $" IS NULL THEN 1 ELSE 0 END) as null_agent_comm,
    SUM(CASE WHEN CAST("Agent Estimated Comm $" AS NUMERIC) = 0 THEN 1 ELSE 0 END) as zero_agent_comm
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com';