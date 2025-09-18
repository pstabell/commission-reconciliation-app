-- Fix demo data by calculating missing commission fields

-- First, let's see what needs to be calculated
SELECT 
    COUNT(*) as total_records,
    COUNT(CASE WHEN "Agent Estimated Comm $" IS NULL THEN 1 END) as missing_agent_comm,
    COUNT(CASE WHEN "Total Agent Comm" IS NULL THEN 1 END) as missing_total_comm
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-STMT-%');

-- Add the missing updated_at column if needed for the trigger
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();

-- Calculate Agency Estimated Comm/Revenue (CRM) if missing
UPDATE policies
SET "Agency Estimated Comm/Revenue (CRM)" = 
    ROUND(CAST("Premium Sold" AS NUMERIC) * CAST("Policy Gross Comm %" AS NUMERIC) / 100, 2)
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Agency Estimated Comm/Revenue (CRM)" IS NULL
    AND "Premium Sold" IS NOT NULL 
    AND "Policy Gross Comm %" IS NOT NULL;

-- Calculate Agent Estimated Comm $ based on transaction type and rates
UPDATE policies
SET "Agent Estimated Comm $" = 
    CASE 
        -- For transaction types with fixed rates
        WHEN "Transaction Type" IN ('NEW', 'NBS', 'STL', 'BoR') THEN 
            ROUND(CAST("Agency Estimated Comm/Revenue (CRM)" AS NUMERIC) * 0.50, 2)
        WHEN "Transaction Type" IN ('RWL', 'REWRITE') THEN 
            ROUND(CAST("Agency Estimated Comm/Revenue (CRM)" AS NUMERIC) * 0.25, 2)
        WHEN "Transaction Type" IN ('CAN', 'XCL') THEN 
            0
        WHEN "Transaction Type" IN ('END', 'PCH') THEN
            -- Check if new business or renewal based on dates
            CASE 
                WHEN "Policy Origination Date" = "Effective Date" THEN
                    ROUND(CAST("Agency Estimated Comm/Revenue (CRM)" AS NUMERIC) * 0.50, 2)
                ELSE
                    ROUND(CAST("Agency Estimated Comm/Revenue (CRM)" AS NUMERIC) * 0.25, 2)
            END
        -- Use Agent Comm % if provided
        WHEN "Agent Comm %" IS NOT NULL AND CAST("Agent Comm %" AS NUMERIC) > 0 THEN
            ROUND(CAST("Agency Estimated Comm/Revenue (CRM)" AS NUMERIC) * CAST("Agent Comm %" AS NUMERIC) / 100, 2)
        ELSE 
            0
    END
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Agent Estimated Comm $" IS NULL
    AND "Agency Estimated Comm/Revenue (CRM)" IS NOT NULL;

-- Calculate Broker Fee Agent Comm (always 50% of Broker Fee)
UPDATE policies
SET "Broker Fee Agent Comm" = 
    ROUND(COALESCE(CAST("Broker Fee" AS NUMERIC), 0) * 0.50, 2)
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Broker Fee Agent Comm" IS NULL;

-- Calculate Total Agent Comm = Agent Estimated Comm $ + Broker Fee Agent Comm
UPDATE policies
SET "Total Agent Comm" = 
    ROUND(
        COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) + 
        COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0), 
        2
    )
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Total Agent Comm" IS NULL;

-- Verify the calculations
SELECT 
    COUNT(*) as total_updated,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) as total_commission_amount
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Effective Date"::DATE >= '2025-01-01'
    AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-STMT-%');

-- Show sample of updated records
SELECT 
    "Policy Number",
    "Transaction Type",
    "Premium Sold",
    "Policy Gross Comm %",
    "Agency Estimated Comm/Revenue (CRM)",
    "Agent Comm %",
    "Agent Estimated Comm $",
    "Broker Fee",
    "Broker Fee Agent Comm",
    "Total Agent Comm"
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Effective Date"::DATE >= '2025-01-01'
    AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-STMT-%')
LIMIT 10;