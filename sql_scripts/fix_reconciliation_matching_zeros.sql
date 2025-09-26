-- Fix reconciliation showing 0 for Matched/Unmatched/Can Create counts
-- Issue: Total Agent Comm values are missing, causing balance calculations to return 0

-- 1. First, check the current state of Total Agent Comm
SELECT 'Current Total Agent Comm Status:' as check_type;
SELECT 
    user_email,
    COUNT(*) as total_records,
    COUNT(CASE WHEN "Total Agent Comm" IS NULL OR CAST("Total Agent Comm" AS TEXT) = '' THEN 1 END) as missing_total_agent_comm,
    COUNT(CASE WHEN CAST("Total Agent Comm" AS NUMERIC) > 0 THEN 1 END) as has_positive_value
FROM policies
GROUP BY user_email;

-- 2. Fix Total Agent Comm by calculating it from component fields
-- This ensures reconciliation has values to work with
UPDATE policies 
SET "Total Agent Comm" = 
    COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) + 
    COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0)
WHERE ("Total Agent Comm" IS NULL OR CAST("Total Agent Comm" AS TEXT) = '' OR CAST("Total Agent Comm" AS TEXT) = '0')
AND (COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) > 0 OR COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0) > 0);

-- 3. For records where both component fields are also missing, calculate from base fields
UPDATE policies 
SET "Agent Estimated Comm $" = 
    ROUND(
        CAST("Commissionable Premium" AS NUMERIC) * 
        (CAST("Policy Gross Comm %" AS NUMERIC) / 100) * 
        (CAST("Agent Comm %" AS NUMERIC) / 100), 2)
WHERE ("Agent Estimated Comm $" IS NULL OR CAST("Agent Estimated Comm $" AS TEXT) = '')
AND "Commissionable Premium" IS NOT NULL
AND "Policy Gross Comm %" IS NOT NULL
AND "Agent Comm %" IS NOT NULL;

-- 4. Update Total Agent Comm again after fixing components
UPDATE policies 
SET "Total Agent Comm" = 
    COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) + 
    COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0)
WHERE ("Total Agent Comm" IS NULL OR CAST("Total Agent Comm" AS TEXT) = '' OR CAST("Total Agent Comm" AS TEXT) = '0');

-- 5. Show the results - transactions that should now appear in reconciliation
SELECT 'Transactions with Outstanding Balance After Fix:' as check_type;
SELECT 
    COUNT(*) as transactions_with_balance,
    SUM(CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_outstanding
FROM policies
WHERE CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0) > 0.01
AND "Transaction ID" NOT LIKE '%-STMT-%'
AND "Transaction ID" NOT LIKE '%-VOID-%'
AND "Transaction ID" NOT LIKE '%-ADJ-%';

-- 6. Sample transactions that should now match
SELECT 'Sample Fixed Transactions:' as check_type;
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Effective Date",
    "Total Agent Comm",
    "Agent Paid Amount (STMT)",
    CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0) as balance
FROM policies
WHERE CAST("Total Agent Comm" AS NUMERIC) > 0
AND "Transaction ID" NOT LIKE '%-STMT-%'
AND "Transaction ID" NOT LIKE '%-VOID-%'
AND "Transaction ID" NOT LIKE '%-ADJ-%'
ORDER BY "Effective Date" DESC
LIMIT 10;

-- 7. Final verification by user
SELECT 'Summary by User:' as check_type;
SELECT 
    user_email,
    COUNT(*) as total_transactions,
    COUNT(CASE WHEN CAST("Total Agent Comm" AS NUMERIC) > 0 THEN 1 END) as has_commission,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) as total_commission_owed,
    SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_paid,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) - SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as outstanding_balance
FROM policies
WHERE "Transaction Type" NOT IN ('CAN', 'XCL')
AND "Transaction ID" NOT LIKE '%-STMT-%'
AND "Transaction ID" NOT LIKE '%-VOID-%'
AND "Transaction ID" NOT LIKE '%-ADJ-%'
GROUP BY user_email;