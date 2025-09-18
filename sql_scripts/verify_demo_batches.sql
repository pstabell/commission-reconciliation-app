-- Verify demo batches are properly set up

-- Show all batches with their details
SELECT 
    reconciliation_id as batch_id,
    COUNT(*) as transaction_count,
    to_date(substring(reconciliation_id from 'DEMO-RECON-(\d{8})'), 'YYYYMMDD') as statement_date,
    COUNT(DISTINCT "Policy Number") as unique_policies,
    COUNT(DISTINCT "Client ID") as unique_clients
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND reconciliation_id IS NOT NULL
    AND "Transaction ID" LIKE '%-STMT-%'
GROUP BY reconciliation_id
ORDER BY statement_date DESC;

-- Sample transactions from a recent batch
SELECT 
    "Transaction ID",
    "Policy Number",
    "Client ID",
    "STMT DATE",
    reconciliation_id
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND reconciliation_id = 'DEMO-RECON-20250731'
LIMIT 5;