-- Debug reconciliation transaction type matching showing zeros
-- This script helps diagnose why Matched/Unmatched/Can Create counts are showing 0

-- 1. Check if there are any transactions in the policies table
SELECT 'Total Transactions in Database:' as check_type;
SELECT 
    COUNT(*) as total_transactions,
    COUNT(DISTINCT user_email) as unique_users,
    COUNT(CASE WHEN user_email = 'demo@agentcommissiontracker.com' THEN 1 END) as demo_transactions
FROM policies;

-- 2. Check transactions with outstanding balances (what reconciliation looks for)
SELECT 'Transactions with Outstanding Balance:' as check_type;
SELECT 
    COUNT(*) as total_with_balance,
    SUM(CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_outstanding
FROM policies
WHERE CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0) > 0.01;

-- 3. Check recent transactions (last 18 months - what reconciliation uses)
SELECT 'Recent Transactions (18 months):' as check_type;
SELECT 
    COUNT(*) as recent_transactions,
    MIN("Effective Date") as oldest_date,
    MAX("Effective Date") as newest_date
FROM policies
WHERE "Effective Date" >= CURRENT_DATE - INTERVAL '18 months';

-- 4. Check transaction types in the database
SELECT 'Transaction Types in Database:' as check_type;
SELECT 
    "Transaction Type",
    COUNT(*) as count
FROM policies
GROUP BY "Transaction Type"
ORDER BY count DESC;

-- 5. Check if Total Agent Comm is populated (required for balance calculation)
SELECT 'Total Agent Comm Status:' as check_type;
SELECT 
    COUNT(*) as total_records,
    COUNT("Total Agent Comm") as has_total_agent_comm,
    COUNT(CASE WHEN "Total Agent Comm" IS NULL OR CAST("Total Agent Comm" AS TEXT) = '' THEN 1 END) as missing_total_agent_comm,
    COUNT(CASE WHEN CAST("Total Agent Comm" AS NUMERIC) > 0 THEN 1 END) as positive_values
FROM policies;

-- 6. Sample transactions that should appear in reconciliation
SELECT 'Sample Unreconciled Transactions:' as check_type;
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Effective Date",
    "Transaction Type",
    "Total Agent Comm",
    "Agent Paid Amount (STMT)",
    CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0) as balance
FROM policies
WHERE CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0) > 0.01
LIMIT 10;

-- 7. Check for STMT transactions (these affect balance calculations)
SELECT 'STMT Transaction Count:' as check_type;
SELECT 
    COUNT(*) as stmt_transactions,
    SUM(CAST("Agent Paid Amount (STMT)" AS NUMERIC)) as total_paid
FROM policies
WHERE "Transaction ID" LIKE '%-STMT-%';

-- 8. Check transaction type mappings table
SELECT 'Transaction Type Mappings:' as check_type;
SELECT COUNT(*) as mapping_count
FROM user_transaction_type_mappings;

-- If mappings exist, show them
SELECT 'Current Mappings:' as check_type;
SELECT 
    statement_type,
    standard_type,
    user_email
FROM user_transaction_type_mappings
LIMIT 10;