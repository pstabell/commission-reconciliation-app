-- Check Total Agent Comm values for demo user
-- This explains why Agent Commission Due dropped from $9,842.93 to $2,045.75

-- 1. Check if Total Agent Comm column has values
SELECT 'Total Agent Comm Analysis:' as check_type;
SELECT 
    COUNT(*) as total_records,
    COUNT("Total Agent Comm") as records_with_total_agent_comm,
    SUM(CASE WHEN "Total Agent Comm" IS NULL THEN 1 ELSE 0 END) as null_values,
    SUM(CASE WHEN "Total Agent Comm" = 0 THEN 1 ELSE 0 END) as zero_values,
    SUM(CASE WHEN "Total Agent Comm" > 0 THEN 1 ELSE 0 END) as positive_values
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com';

-- 2. Compare Total Agent Comm vs calculated values
SELECT 'Calculation Comparison:' as check_type;
SELECT 
    SUM(CAST("Total Agent Comm" AS NUMERIC)) as sum_total_agent_comm,
    SUM(CAST("Agent Estimated Comm $" AS NUMERIC)) as sum_agent_estimated,
    SUM(CAST("Broker Fee Agent Comm" AS NUMERIC)) as sum_broker_fee_comm,
    SUM(COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) + COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0)) as calculated_total,
    SUM(CAST("Agent Paid Amount (STMT)" AS NUMERIC)) as sum_paid
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Transaction Type" NOT IN ('CAN', 'XCL');

-- 3. Show sample records with missing Total Agent Comm
SELECT 'Sample Missing Total Agent Comm:' as check_type;
SELECT 
    "Transaction ID",
    "Customer",
    "Agent Estimated Comm $",
    "Broker Fee Agent Comm",
    "Total Agent Comm",
    COALESCE("Agent Estimated Comm $", 0) + COALESCE("Broker Fee Agent Comm", 0) as should_be_total
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND ("Total Agent Comm" IS NULL OR "Total Agent Comm" = 0)
AND ("Agent Estimated Comm $" > 0 OR "Broker Fee Agent Comm" > 0)
LIMIT 10;

-- 4. Calculate what Agent Commission Due should be
SELECT 'Agent Commission Due Calculation:' as check_type;
SELECT 
    -- Using Total Agent Comm (current method - probably wrong)
    SUM(COALESCE(CAST("Total Agent Comm" AS NUMERIC), 0)) - SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as current_calc_method,
    -- Using fallback calculation (probably correct)
    SUM(COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) + COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0)) - SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as correct_calc_method,
    -- Show the difference
    SUM(COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) + COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0)) - SUM(COALESCE(CAST("Total Agent Comm" AS NUMERIC), 0)) as difference
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Transaction Type" NOT IN ('CAN', 'XCL');

-- 5. Fix suggestion - Update Total Agent Comm
SELECT 'Fix Command:' as check_type;
SELECT 
    'UPDATE policies SET "Total Agent Comm" = COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) + COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0) WHERE user_email = ''demo@agentcommissiontracker.com'' AND ("Total Agent Comm" IS NULL OR "Total Agent Comm" = 0 OR "Total Agent Comm" = '''');' as fix_command;