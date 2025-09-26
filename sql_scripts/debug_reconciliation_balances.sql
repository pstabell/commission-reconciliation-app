-- Debug reconciliation balance calculations
-- This script checks why dashboard shows $9,824 due but reconciliation shows tiny amounts

-- First, check Total Agent Comm values for all original transactions
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Effective Date",
    "Total Agent Comm",
    "Agent Estimated Comm $",
    "Broker Fee Agent Comm",
    COALESCE("Total Agent Comm", 0) as calculated_total_comm,
    CASE 
        WHEN "Total Agent Comm" IS NULL OR "Total Agent Comm" = 0 
        THEN COALESCE("Agent Estimated Comm $", 0) + COALESCE("Broker Fee Agent Comm", 0)
        ELSE "Total Agent Comm"
    END as final_commission
FROM policies
WHERE "Transaction ID" NOT LIKE '%-STMT-%'
    AND "Transaction ID" NOT LIKE '%-VOID-%'
    AND "Transaction ID" NOT LIKE '%-ADJ-%'
    AND user_email = 'patric@bellwethercm.com'
    AND "Effective Date" >= CURRENT_DATE - INTERVAL '18 months'
ORDER BY final_commission DESC
LIMIT 20;

-- Check for transactions with significant commission amounts
SELECT 
    COUNT(*) as trans_count,
    SUM(CASE 
        WHEN "Total Agent Comm" IS NULL OR "Total Agent Comm" = 0 
        THEN COALESCE("Agent Estimated Comm $", 0) + COALESCE("Broker Fee Agent Comm", 0)
        ELSE "Total Agent Comm"
    END) as total_commission_amount,
    SUM(CASE 
        WHEN "Total Agent Comm" > 100 THEN 1 
        ELSE 0 
    END) as high_value_transactions
FROM policies
WHERE "Transaction ID" NOT LIKE '%-STMT-%'
    AND "Transaction ID" NOT LIKE '%-VOID-%'
    AND "Transaction ID" NOT LIKE '%-ADJ-%'
    AND user_email = 'patric@bellwethercm.com'
    AND "Effective Date" >= CURRENT_DATE - INTERVAL '18 months';

-- Now check paid amounts from STMT entries
SELECT 
    p."Policy Number",
    p."Effective Date",
    SUM(CASE WHEN p."Transaction ID" NOT LIKE '%-STMT-%' THEN 
        CASE 
            WHEN p."Total Agent Comm" IS NULL OR p."Total Agent Comm" = 0 
            THEN COALESCE(p."Agent Estimated Comm $", 0) + COALESCE(p."Broker Fee Agent Comm", 0)
            ELSE p."Total Agent Comm"
        END 
    ELSE 0 END) as total_commission,
    SUM(CASE WHEN p."Transaction ID" LIKE '%-STMT-%' THEN p."Agent Paid Amount (STMT)" ELSE 0 END) as total_paid,
    SUM(CASE WHEN p."Transaction ID" NOT LIKE '%-STMT-%' THEN 
        CASE 
            WHEN p."Total Agent Comm" IS NULL OR p."Total Agent Comm" = 0 
            THEN COALESCE(p."Agent Estimated Comm $", 0) + COALESCE(p."Broker Fee Agent Comm", 0)
            ELSE p."Total Agent Comm"
        END 
    ELSE 0 END) - 
    SUM(CASE WHEN p."Transaction ID" LIKE '%-STMT-%' THEN p."Agent Paid Amount (STMT)" ELSE 0 END) as balance
FROM policies p
WHERE p.user_email = 'patric@bellwethercm.com'
    AND p."Effective Date" >= CURRENT_DATE - INTERVAL '18 months'
GROUP BY p."Policy Number", p."Effective Date"
HAVING SUM(CASE WHEN p."Transaction ID" NOT LIKE '%-STMT-%' THEN 
        CASE 
            WHEN p."Total Agent Comm" IS NULL OR p."Total Agent Comm" = 0 
            THEN COALESCE(p."Agent Estimated Comm $", 0) + COALESCE(p."Broker Fee Agent Comm", 0)
            ELSE p."Total Agent Comm"
        END 
    ELSE 0 END) - 
    SUM(CASE WHEN p."Transaction ID" LIKE '%-STMT-%' THEN p."Agent Paid Amount (STMT)" ELSE 0 END) > 1
ORDER BY balance DESC
LIMIT 20;

-- Check for any data quality issues with Total Agent Comm
SELECT 
    COUNT(*) as total_records,
    SUM(CASE WHEN "Total Agent Comm" IS NULL THEN 1 ELSE 0 END) as null_total_agent_comm,
    SUM(CASE WHEN "Total Agent Comm" = 0 THEN 1 ELSE 0 END) as zero_total_agent_comm,
    SUM(CASE WHEN "Total Agent Comm" > 0 THEN 1 ELSE 0 END) as positive_total_agent_comm,
    SUM(CASE WHEN "Total Agent Comm" < 0 THEN 1 ELSE 0 END) as negative_total_agent_comm
FROM policies
WHERE "Transaction ID" NOT LIKE '%-STMT-%'
    AND "Transaction ID" NOT LIKE '%-VOID-%'
    AND "Transaction ID" NOT LIKE '%-ADJ-%'
    AND user_email = 'patric@bellwethercm.com';

-- Find specific high-balance transactions that should appear
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Effective Date",
    "Total Agent Comm",
    (
        SELECT COALESCE(SUM("Agent Paid Amount (STMT)"), 0)
        FROM policies stmt
        WHERE stmt."Policy Number" = p."Policy Number"
            AND stmt."Effective Date" = p."Effective Date"
            AND stmt."Transaction ID" LIKE '%-STMT-%'
            AND stmt.user_email = 'patric@bellwethercm.com'
    ) as paid_amount,
    COALESCE("Total Agent Comm", 0) - (
        SELECT COALESCE(SUM("Agent Paid Amount (STMT)"), 0)
        FROM policies stmt
        WHERE stmt."Policy Number" = p."Policy Number"
            AND stmt."Effective Date" = p."Effective Date"
            AND stmt."Transaction ID" LIKE '%-STMT-%'
            AND stmt.user_email = 'patric@bellwethercm.com'
    ) as calculated_balance
FROM policies p
WHERE p."Transaction ID" NOT LIKE '%-STMT-%'
    AND p."Transaction ID" NOT LIKE '%-VOID-%'
    AND p."Transaction ID" NOT LIKE '%-ADJ-%'
    AND p.user_email = 'patric@bellwethercm.com'
    AND p."Total Agent Comm" > 100
    AND p."Effective Date" >= CURRENT_DATE - INTERVAL '18 months'
ORDER BY calculated_balance DESC
LIMIT 50;