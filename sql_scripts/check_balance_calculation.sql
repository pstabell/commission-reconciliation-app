-- Check if _balance column exists and why Agent Commission Due is low
-- The dashboard uses calculate_transaction_balances which creates a '_balance' column

-- 1. Check what columns we have
SELECT 'Column Check:' as analysis;
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'policies' 
AND column_name LIKE '%balance%'
ORDER BY column_name;

-- 2. The dashboard calculates balance as: Total Agent Comm - Agent Paid Amount (STMT)
-- Let's manually calculate what it should be
SELECT 'Manual Balance Calculation:' as analysis;
SELECT 
    SUM(CAST("Total Agent Comm" AS NUMERIC)) as total_agent_comm,
    SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_paid,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) - SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as calculated_balance
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Transaction Type" NOT IN ('CAN', 'XCL');

-- 3. List ALL columns in policies table to see what we have
SELECT 'All Columns in Policies Table:' as analysis;
SELECT column_name, data_type
FROM information_schema.columns 
WHERE table_name = 'policies' 
AND (column_name LIKE '%balance%' OR column_name LIKE '%due%' OR column_name LIKE '%comm%' OR column_name LIKE '%paid%')
ORDER BY column_name;

-- 4. The real issue might be that Total Agent Comm needs to include formulas
-- Check a few records to see the calculation
SELECT 'Sample Calculations:' as analysis;
SELECT 
    "Transaction ID",
    "Transaction Type",
    "Premium Sold",
    "Policy Gross Comm %",
    CAST("Premium Sold" AS NUMERIC) * (CAST("Policy Gross Comm %" AS NUMERIC) / 100) as agency_comm,
    CASE 
        WHEN "Transaction Type" IN ('NEW', 'NBS') THEN 0.50
        WHEN "Transaction Type" IN ('RWL', 'REWRITE') THEN 0.25
        ELSE 0.25
    END as agent_rate,
    (CAST("Premium Sold" AS NUMERIC) * (CAST("Policy Gross Comm %" AS NUMERIC) / 100)) * 
    CASE 
        WHEN "Transaction Type" IN ('NEW', 'NBS') THEN 0.50
        WHEN "Transaction Type" IN ('RWL', 'REWRITE') THEN 0.25
        ELSE 0.25
    END as calculated_agent_comm,
    "Agent Estimated Comm $",
    "Total Agent Comm"
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Premium Sold" IS NOT NULL
AND "Policy Gross Comm %" IS NOT NULL
LIMIT 10;