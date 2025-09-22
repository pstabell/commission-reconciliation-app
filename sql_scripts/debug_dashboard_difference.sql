-- Debug why dashboard shows $2,502.59 when database shows $12,531.76

-- 1. Check if there are any filters the dashboard might be applying
SELECT 'Transaction Type Breakdown:' as analysis;
SELECT 
    "Transaction Type",
    COUNT(*) as count,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) as total_comm,
    SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_paid,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) - SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as balance
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
GROUP BY "Transaction Type"
ORDER BY balance DESC;

-- 2. Check for any NULL or empty Transaction Types
SELECT 'NULL Transaction Types:' as analysis;
SELECT COUNT(*) as null_trans_type_count
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND ("Transaction Type" IS NULL OR "Transaction Type" = '');

-- 3. Check if dashboard might be using a date filter
SELECT 'Recent Transactions Only (Last 90 days):' as analysis;
SELECT 
    SUM(CAST("Total Agent Comm" AS NUMERIC)) as total_comm_90d,
    SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_paid_90d,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) - SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as balance_90d
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Transaction Type" NOT IN ('CAN', 'XCL')
AND "Effective Date" >= CURRENT_DATE - INTERVAL '90 days';

-- 4. Check what the dashboard calculation would be with just -STMT- transactions excluded
SELECT 'Excluding STMT Transactions:' as analysis;
SELECT 
    SUM(CAST("Total Agent Comm" AS NUMERIC)) as total_comm,
    SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_paid,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) - SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as balance
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Transaction Type" NOT IN ('CAN', 'XCL')
AND "Transaction ID" NOT LIKE '%-STMT-%';

-- 5. Total without any filters (what we calculated)
SELECT 'Total Without Filters:' as analysis;
SELECT 
    SUM(CAST("Total Agent Comm" AS NUMERIC)) as total_comm,
    SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_paid,
    SUM(CAST("Total Agent Comm" AS NUMERIC)) - SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as balance
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Transaction Type" NOT IN ('CAN', 'XCL');