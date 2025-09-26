-- Fix Agent Commission calculations and exclude totals rows
-- This script identifies and handles the totals row issue

-- 1. First identify the totals row
SELECT 'Identifying totals row:' as step;
SELECT 
    "Transaction ID",
    "Customer",
    "Transaction Type",
    "Total Agent Comm",
    CASE 
        WHEN ABS(CAST("Total Agent Comm" AS NUMERIC) - 1568.941) < 0.01 THEN 'TOTALS ROW - EXCLUDE'
        WHEN "Customer" IS NULL OR TRIM("Customer") = '' THEN 'EMPTY CUSTOMER - CHECK'
        WHEN UPPER("Customer") LIKE '%TOTAL%' THEN 'TOTALS IN NAME - EXCLUDE'
        ELSE 'VALID TRANSACTION'
    END as row_type
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND (
    ABS(CAST("Total Agent Comm" AS NUMERIC) - 1568.941) < 0.01 OR
    "Customer" IS NULL OR 
    TRIM("Customer") = '' OR
    UPPER("Customer") LIKE '%TOTAL%'
);

-- 2. Delete the totals row if it exists
SELECT 'Delete totals row command:' as step;
SELECT 'To remove the totals row, run this DELETE command:' as instruction;
SELECT '
DELETE FROM policies 
WHERE user_email = ''demo@agentcommissiontracker.com''
AND ABS(CAST("Total Agent Comm" AS NUMERIC) - 1568.941) < 0.01;
' as delete_command;

-- 3. After deleting totals row, fix Agent Estimated Comm $ for remaining rows
SELECT 'Fix Agent Estimated Comm command:' as step;
SELECT 'After deleting the totals row, run this to fix commission calculations:' as instruction;
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
WHERE user_email = ''demo@agentcommissiontracker.com'';
' as update_agent_comm_command;

-- 4. Update Total Agent Comm based on the fixed values
SELECT 'Update Total Agent Comm command:' as step;
SELECT 'Finally, run this to update Total Agent Comm:' as instruction;
SELECT '
UPDATE policies 
SET "Total Agent Comm" = COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) + COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0)
WHERE user_email = ''demo@agentcommissiontracker.com'';
' as update_total_command;

-- 5. Show what the final result will be
SELECT 'Expected final result:' as step;
SELECT 
    COUNT(*) - 1 as records_after_deletion,  -- Minus 1 for the totals row
    1568.941 as amount_to_exclude,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) - 1568.941 as expected_total_agent_comm,
    SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_paid,
    (SUM(CAST("Total Agent Comm" AS NUMERIC)) - 1568.941) - SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as expected_commission_due
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Transaction Type" NOT IN ('CAN', 'XCL');