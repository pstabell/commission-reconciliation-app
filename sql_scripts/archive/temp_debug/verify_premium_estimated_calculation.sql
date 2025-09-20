-- Verify how Premium Estimated is calculated

-- Find 2025 original transactions that have NOT been paid
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
    COUNT(*) as unpaid_transaction_count,
    SUM(CAST("Premium Sold" AS NUMERIC)) as premium_estimated_total
FROM originals_2025 o
WHERE NOT EXISTS (
    SELECT 1 
    FROM paid_policies p 
    WHERE p."Policy Number" = o."Policy Number" 
    AND p."Effective Date" = o."Effective Date"
);

-- Compare with total 2025 premium to see the breakdown
SELECT 
    'Total 2025 Premium' as category,
    SUM(CAST("Premium Sold" AS NUMERIC)) as amount
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Effective Date"::DATE >= '2025-01-01'
    AND "Effective Date"::DATE <= '2025-12-31'
    AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-STMT-%')
UNION ALL
SELECT 
    'Paid (has -STMT- entry)' as category,
    SUM(CAST(o."Premium Sold" AS NUMERIC)) as amount
FROM policies o
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND o."Effective Date"::DATE >= '2025-01-01'
    AND o."Effective Date"::DATE <= '2025-12-31'
    AND ("Transaction ID" IS NULL OR o."Transaction ID" NOT LIKE '%-STMT-%')
    AND EXISTS (
        SELECT 1 
        FROM policies p 
        WHERE p.user_email = 'demo@agentcommissiontracker.com'
        AND p."Transaction ID" LIKE '%-STMT-%'
        AND p."Policy Number" = o."Policy Number" 
        AND p."Effective Date" = o."Effective Date"
    );