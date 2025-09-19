-- Investigate why there are no 2025 unreconciled transactions

-- 1. Check ALL 2025 transactions regardless of reconciliation status
SELECT 
    COUNT(*) as total_2025_transactions,
    COUNT(CASE WHEN "Transaction ID" IS NULL THEN 1 END) as null_transaction_id,
    COUNT(CASE WHEN "Transaction ID" = '' THEN 1 END) as empty_transaction_id,
    COUNT(CASE WHEN "Transaction ID" LIKE '%-STMT-%' THEN 1 END) as reconciled_stmt,
    COUNT(CASE WHEN "Transaction ID" NOT LIKE '%-STMT-%' AND "Transaction ID" IS NOT NULL THEN 1 END) as has_transaction_id_not_stmt
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Effective Date" >= '2025-01-01'
    AND "Effective Date" <= '2025-12-31';

-- 2. Show sample of ALL 2025 transactions to see their status
SELECT 
    "Policy Number",
    "Transaction Type",
    "Effective Date",
    "Transaction ID",
    reconciliation_status,
    "Premium Sold",
    "Total Agent Comm"
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Effective Date" >= '2025-01-01'
    AND "Effective Date" <= '2025-12-31'
ORDER BY "Effective Date" DESC
LIMIT 10;

-- 3. Check what dates the demo data actually covers
SELECT 
    EXTRACT(YEAR FROM "Effective Date"::DATE) as year,
    COUNT(*) as transaction_count,
    COUNT(CASE WHEN "Transaction ID" LIKE '%-STMT-%' THEN 1 END) as reconciled_count,
    COUNT(CASE WHEN "Transaction ID" IS NULL OR ("Transaction ID" NOT LIKE '%-STMT-%') THEN 1 END) as unreconciled_count
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Effective Date" IS NOT NULL
GROUP BY EXTRACT(YEAR FROM "Effective Date"::DATE)
ORDER BY year DESC;