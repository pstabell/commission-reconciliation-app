-- Debug why reconciliation shows 0 matches when commission is due

-- 1. Show transactions with outstanding balances (what makes up your $9,824.29)
SELECT 'Outstanding Transactions (Top 20):' as report_section;
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Effective Date",
    "Policy Type",
    "Total Agent Comm" as commission_owed,
    COALESCE("Agent Paid Amount (STMT)", '0') as amount_paid,
    CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0) as balance_due
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND CAST("Total Agent Comm" AS NUMERIC) > 0
AND CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0) > 0.01
AND "Transaction ID" NOT LIKE '%-STMT-%'
AND "Transaction ID" NOT LIKE '%-VOID-%'
AND "Transaction ID" NOT LIKE '%-ADJ-%'
ORDER BY balance_due DESC
LIMIT 20;

-- 2. Show variety in customer names (potential matching issues)
SELECT 'Customer Name Variations:' as report_section;
SELECT DISTINCT
    "Customer",
    COUNT(*) as transaction_count,
    SUM(CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_balance_due
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0) > 0.01
AND "Transaction ID" NOT LIKE '%-STMT-%'
GROUP BY "Customer"
ORDER BY total_balance_due DESC
LIMIT 10;

-- 3. Show date formats in use
SELECT 'Effective Date Formats:' as report_section;
SELECT DISTINCT
    "Effective Date",
    COUNT(*) as count
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Effective Date" IS NOT NULL
GROUP BY "Effective Date"
ORDER BY "Effective Date" DESC
LIMIT 10;

-- 4. Check for policy number patterns
SELECT 'Policy Number Patterns:' as report_section;
SELECT 
    LEFT("Policy Number", 3) as prefix,
    COUNT(DISTINCT "Policy Number") as unique_policies,
    COUNT(*) as transaction_count
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Policy Number" IS NOT NULL AND "Policy Number" != ''
GROUP BY LEFT("Policy Number", 3)
ORDER BY transaction_count DESC
LIMIT 10;

-- 5. Summary of what needs to be matched
SELECT 'Reconciliation Matching Requirements:' as report_section;
SELECT 
    COUNT(DISTINCT "Customer") as unique_customers,
    COUNT(DISTINCT "Policy Number") as unique_policies,
    COUNT(DISTINCT "Effective Date") as unique_dates,
    COUNT(*) as total_transactions_to_match,
    SUM(CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_to_reconcile
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0) > 0.01
AND "Transaction ID" NOT LIKE '%-STMT-%';