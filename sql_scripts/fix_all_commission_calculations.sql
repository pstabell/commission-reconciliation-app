-- Fix ALL commission calculations to restore Agent Commission Due to $9,842.93
-- Your data shows NULL in Agent Estimated Comm $ for most records

-- 1. Fix Agent Estimated Comm $ using the proper formula
UPDATE policies 
SET "Agent Estimated Comm $" = 
    ROUND(
        CAST("Premium Sold" AS NUMERIC) * 
        (CAST("Policy Gross Comm %" AS NUMERIC) / 100) * 
        CASE 
            WHEN "Transaction Type" IN ('NEW', 'NBS', 'STL', 'BoR') THEN 0.50
            WHEN "Transaction Type" IN ('RWL', 'REWRITE') THEN 0.25
            WHEN "Transaction Type" IN ('CAN', 'XCL') THEN 0
            WHEN "Transaction Type" IN ('END', 'PCH') THEN 0.25
            ELSE 0.25
        END, 2)
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Premium Sold" IS NOT NULL
AND "Policy Gross Comm %" IS NOT NULL;

-- 2. Fix Broker Fee Agent Comm (50% of Broker Fee)
UPDATE policies 
SET "Broker Fee Agent Comm" = ROUND(COALESCE(CAST("Broker Fee" AS NUMERIC), 0) * 0.50, 2)
WHERE user_email = 'demo@agentcommissiontracker.com';

-- 3. Fix Total Agent Comm = Agent Estimated Comm $ + Broker Fee Agent Comm
UPDATE policies 
SET "Total Agent Comm" = 
    COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) + 
    COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0)
WHERE user_email = 'demo@agentcommissiontracker.com';

-- 4. Show the results
SELECT 
    'Final Result:' as check_type,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) as total_agent_comm,
    SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_paid,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) - SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as agent_commission_due
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Transaction Type" NOT IN ('CAN', 'XCL');