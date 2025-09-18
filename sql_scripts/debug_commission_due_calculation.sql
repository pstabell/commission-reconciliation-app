-- Debug why Agent Commission Due might be showing 0

-- 1. Check total commissions earned vs paid
SELECT 
    'Total Earned (Original Transactions)' as description,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) as amount
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-STMT-%')
    AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-VOID-%')
    AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-ADJ-%')
UNION ALL
SELECT 
    'Total Paid (-STMT- entries)' as description,
    SUM(CAST("Agent Paid Amount (STMT)" AS NUMERIC)) as amount
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction ID" LIKE '%-STMT-%'
UNION ALL
SELECT 
    'Simple Balance (Earned - Paid)' as description,
    (
        SELECT SUM(CAST("Total Agent Comm" AS NUMERIC))
        FROM policies
        WHERE user_email = 'demo@agentcommissiontracker.com'
        AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-STMT-%')
    ) - 
    COALESCE((
        SELECT SUM(CAST("Agent Paid Amount (STMT)" AS NUMERIC))
        FROM policies
        WHERE user_email = 'demo@agentcommissiontracker.com'
        AND "Transaction ID" LIKE '%-STMT-%'
    ), 0) as amount;

-- 2. Check if the issue is with specific policies having partial payments
WITH policy_balances AS (
    SELECT 
        p."Policy Number",
        p."Effective Date",
        SUM(CASE 
            WHEN p."Transaction ID" NOT LIKE '%-STMT-%' 
            THEN CAST(p."Total Agent Comm" AS NUMERIC) 
            ELSE 0 
        END) as total_earned,
        SUM(CASE 
            WHEN p."Transaction ID" LIKE '%-STMT-%' 
            THEN CAST(p."Agent Paid Amount (STMT)" AS NUMERIC) 
            ELSE 0 
        END) as total_paid
    FROM policies p
    WHERE 
        p.user_email = 'demo@agentcommissiontracker.com'
        AND p."Total Agent Comm" IS NOT NULL
    GROUP BY p."Policy Number", p."Effective Date"
)
SELECT 
    COUNT(*) as policies_with_balance,
    SUM(total_earned - total_paid) as total_balance_due
FROM policy_balances
WHERE total_earned > total_paid;

-- 3. Show a few examples of policies with balances
WITH policy_balances AS (
    SELECT 
        p."Policy Number",
        p."Effective Date",
        SUM(CASE 
            WHEN p."Transaction ID" NOT LIKE '%-STMT-%' 
            THEN CAST(p."Total Agent Comm" AS NUMERIC) 
            ELSE 0 
        END) as total_earned,
        SUM(CASE 
            WHEN p."Transaction ID" LIKE '%-STMT-%' 
            THEN CAST(p."Agent Paid Amount (STMT)" AS NUMERIC) 
            ELSE 0 
        END) as total_paid
    FROM policies p
    WHERE 
        p.user_email = 'demo@agentcommissiontracker.com'
    GROUP BY p."Policy Number", p."Effective Date"
    HAVING SUM(CASE 
            WHEN p."Transaction ID" NOT LIKE '%-STMT-%' 
            THEN CAST(p."Total Agent Comm" AS NUMERIC) 
            ELSE 0 
        END) > 0
)
SELECT 
    "Policy Number",
    "Effective Date",
    total_earned,
    total_paid,
    (total_earned - total_paid) as balance_due
FROM policy_balances
WHERE total_earned > total_paid
ORDER BY balance_due DESC
LIMIT 10;