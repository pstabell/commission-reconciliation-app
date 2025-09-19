-- Check what's in the unreconciled 2025 transactions that have premium but no commission

-- First, let's replicate the dashboard's logic
-- Find 2025 original transactions (no -STMT-, -VOID-, -ADJ- in Transaction ID)
WITH originals_2025 AS (
    SELECT *
    FROM policies
    WHERE 
        user_email = 'demo@agentcommissiontracker.com'
        AND "Effective Date"::DATE >= '2025-01-01'
        AND "Effective Date"::DATE <= '2025-12-31'
        AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-STMT-%')
        AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-VOID-%')
        AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-ADJ-%')
),
-- Find which ones have been paid (have matching -STMT- entries)
paid_policies AS (
    SELECT DISTINCT "Policy Number", "Effective Date"
    FROM policies
    WHERE 
        user_email = 'demo@agentcommissiontracker.com'
        AND "Transaction ID" LIKE '%-STMT-%'
)
-- Get unpaid 2025 originals
SELECT 
    COUNT(*) as count,
    SUM(CAST("Premium Sold" AS NUMERIC)) as total_premium,
    SUM(CASE WHEN "Total Agent Comm" IS NOT NULL THEN CAST("Total Agent Comm" AS NUMERIC) ELSE 0 END) as total_agent_comm_sum,
    SUM(CASE WHEN "Agent Estimated Comm $" IS NOT NULL THEN CAST("Agent Estimated Comm $" AS NUMERIC) ELSE 0 END) as agent_estimated_sum,
    COUNT(CASE WHEN "Total Agent Comm" IS NOT NULL AND "Total Agent Comm"::TEXT != '' THEN 1 END) as has_total_agent_comm,
    COUNT(CASE WHEN "Agent Estimated Comm $" IS NOT NULL AND "Agent Estimated Comm $"::TEXT != '' THEN 1 END) as has_agent_estimated
FROM originals_2025 o
WHERE NOT EXISTS (
    SELECT 1 
    FROM paid_policies p 
    WHERE p."Policy Number" = o."Policy Number" 
    AND p."Effective Date" = o."Effective Date"
);

-- Show sample of these unpaid records
WITH originals_2025 AS (
    SELECT *
    FROM policies
    WHERE 
        user_email = 'demo@agentcommissiontracker.com'
        AND "Effective Date"::DATE >= '2025-01-01'
        AND "Effective Date"::DATE <= '2025-12-31'
        AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-STMT-%')
        AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-VOID-%')
        AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-ADJ-%')
),
paid_policies AS (
    SELECT DISTINCT "Policy Number", "Effective Date"
    FROM policies
    WHERE 
        user_email = 'demo@agentcommissiontracker.com'
        AND "Transaction ID" LIKE '%-STMT-%'
)
SELECT 
    "Policy Number",
    "Transaction Type",
    "Effective Date",
    "Premium Sold",
    "Policy Gross Comm %",
    "Agent Comm %",
    "Total Agent Comm",
    "Agent Estimated Comm $"
FROM originals_2025 o
WHERE NOT EXISTS (
    SELECT 1 
    FROM paid_policies p 
    WHERE p."Policy Number" = o."Policy Number" 
    AND p."Effective Date" = o."Effective Date"
)
LIMIT 10;