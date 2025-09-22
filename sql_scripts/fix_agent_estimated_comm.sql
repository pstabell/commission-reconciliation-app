-- Fix Agent Estimated Comm $ calculation for demo account
-- This will restore Agent Commission Due to ~$9,842.93

-- 1. First, check what we're working with
SELECT 'Current Status:' as check_type;
SELECT 
    COUNT(*) as total_records,
    SUM(CASE WHEN "Agent Estimated Comm $" IS NULL THEN 1 ELSE 0 END) as null_agent_comm,
    SUM(CASE WHEN "Premium Sold" IS NOT NULL AND "Agent Estimated Comm $" IS NULL THEN 1 ELSE 0 END) as missing_calculations
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com';

-- 2. Calculate what Agent Estimated Comm $ should be
-- Formula: (Premium Sold - Policy Taxes & Fees) * (Policy Gross Comm % / 100) * (Agent Comm % / 100)
-- For NEW business: Agent Comm % = 50%
-- For RENEWALS: Agent Comm % = 25%

SELECT 'Sample Calculations:' as check_type;
SELECT 
    "Transaction ID",
    "Transaction Type",
    "Premium Sold",
    "Policy Taxes & Fees",
    "Policy Gross Comm %",
    CASE 
        WHEN "Transaction Type" IN ('NEW', 'NBS', 'STL', 'BoR') THEN 50
        WHEN "Transaction Type" IN ('RWL', 'REWRITE') THEN 25
        WHEN "Transaction Type" IN ('CAN', 'XCL') THEN 0
        ELSE 25
    END as agent_rate,
    CASE 
        WHEN "Premium Sold" IS NOT NULL AND "Policy Gross Comm %" IS NOT NULL THEN
            ROUND((CAST("Premium Sold" AS NUMERIC) - COALESCE(CAST("Policy Taxes & Fees" AS NUMERIC), 0)) * 
                  (CAST("Policy Gross Comm %" AS NUMERIC) / 100) * 
                  (CASE 
                      WHEN "Transaction Type" IN ('NEW', 'NBS', 'STL', 'BoR') THEN 0.50
                      WHEN "Transaction Type" IN ('RWL', 'REWRITE') THEN 0.25
                      WHEN "Transaction Type" IN ('CAN', 'XCL') THEN 0
                      ELSE 0.25
                  END), 2)
        ELSE 0
    END as calculated_agent_comm
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Premium Sold" IS NOT NULL
LIMIT 10;

-- 3. UPDATE command to fix Agent Estimated Comm $
SELECT 'Fix Command:' as check_type;
SELECT 'Run this UPDATE command to fix all Agent Estimated Comm $ values:' as instruction;
SELECT '
UPDATE policies 
SET "Agent Estimated Comm $" = 
    CASE 
        WHEN "Premium Sold" IS NOT NULL AND "Policy Gross Comm %" IS NOT NULL THEN
            ROUND((CAST("Premium Sold" AS NUMERIC) - COALESCE(CAST("Policy Taxes & Fees" AS NUMERIC), 0)) * 
                  (CAST("Policy Gross Comm %" AS NUMERIC) / 100) * 
                  (CASE 
                      WHEN "Transaction Type" IN (''NEW'', ''NBS'', ''STL'', ''BoR'') THEN 0.50
                      WHEN "Transaction Type" IN (''RWL'', ''REWRITE'') THEN 0.25
                      WHEN "Transaction Type" IN (''CAN'', ''XCL'') THEN 0
                      ELSE 0.25
                  END), 2)
        ELSE 0
    END
WHERE user_email = ''demo@agentcommissiontracker.com''
AND "Agent Estimated Comm $" IS NULL;' as update_command;

-- 4. Then update Total Agent Comm again
SELECT 'Second Fix Command:' as check_type;
SELECT 'After running the first UPDATE, run this to recalculate Total Agent Comm:' as instruction;
SELECT '
UPDATE policies 
SET "Total Agent Comm" = COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) + COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0) 
WHERE user_email = ''demo@agentcommissiontracker.com'';' as update_command2;