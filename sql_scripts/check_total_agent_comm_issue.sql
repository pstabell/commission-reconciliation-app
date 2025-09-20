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
    SUM("Total Agent Comm") as sum_total_agent_comm,
    SUM("Agent Estimated Comm $") as sum_agent_estimated,
    SUM("Broker Fee Agent Comm") as sum_broker_fee_comm,
    SUM(COALESCE("Agent Estimated Comm $", 0) + COALESCE("Broker Fee Agent Comm", 0)) as calculated_total,
    SUM("Agent Paid Amount (STMT)") as sum_paid
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
    SUM(COALESCE("Total Agent Comm", 0)) - SUM(COALESCE("Agent Paid Amount (STMT)", 0)) as current_calc_method,
    -- Using fallback calculation (probably correct)
    SUM(COALESCE("Agent Estimated Comm $", 0) + COALESCE("Broker Fee Agent Comm", 0)) - SUM(COALESCE("Agent Paid Amount (STMT)", 0)) as correct_calc_method,
    -- Show the difference
    SUM(COALESCE("Agent Estimated Comm $", 0) + COALESCE("Broker Fee Agent Comm", 0)) - SUM(COALESCE("Total Agent Comm", 0)) as difference
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Transaction Type" NOT IN ('CAN', 'XCL');

-- 5. Fix suggestion - Update Total Agent Comm
SELECT 'Fix Command:' as check_type;
SELECT 
    'UPDATE policies SET "Total Agent Comm" = COALESCE("Agent Estimated Comm $", 0) + COALESCE("Broker Fee Agent Comm", 0) WHERE user_email = ''demo@agentcommissiontracker.com'' AND ("Total Agent Comm" IS NULL OR "Total Agent Comm" = 0);' as fix_command;