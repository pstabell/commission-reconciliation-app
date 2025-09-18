-- SQL script to update demo reconciliation data with batch IDs
-- based on statement dates extracted from transaction IDs
-- 
-- Transaction ID format: XXXXXXX-STMT-YYYYMMDD
-- Batch ID format: DEMO-RECON-YYYYMMDD

-- First, let's see what we're working with
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT substring("Transaction ID" from '.*-STMT-(\d{8})$')) as unique_dates,
    COUNT(reconciliation_id) as records_with_batch_id
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction ID" LIKE '%-STMT-%';

-- First check if we can disable the trigger temporarily
-- If this fails, we'll use a different approach
BEGIN;

-- Try to disable the trigger (this might fail if you don't have permissions)
-- ALTER TABLE policies DISABLE TRIGGER update_policies_updated_at;

-- Update records with batch IDs based on the date in transaction_id
-- Using a workaround approach with a CTE and individual updates
WITH batch_updates AS (
    SELECT 
        _id,
        'DEMO-RECON-' || substring("Transaction ID" from '.*-STMT-(\d{8})$') as new_batch_id
    FROM policies
    WHERE 
        user_email = 'demo@agentcommissiontracker.com'
        AND reconciliation_id IS NULL
        AND "Transaction ID" ~ '.*-STMT-\d{8}$'
)
UPDATE policies p
SET reconciliation_id = bu.new_batch_id
FROM batch_updates bu
WHERE p._id = bu._id;

-- Re-enable trigger if we disabled it
-- ALTER TABLE policies ENABLE TRIGGER update_policies_updated_at;

COMMIT;

-- Verify the update
SELECT 
    reconciliation_id as batch_id,
    COUNT(*) as transaction_count,
    MIN(substring("Transaction ID" from '.*-STMT-(\d{8})$')) as statement_date
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND reconciliation_id IS NOT NULL
    AND "Transaction ID" LIKE '%-STMT-%'
GROUP BY reconciliation_id
ORDER BY reconciliation_id;

-- Show sample of updated records
SELECT 
    "Transaction ID",
    reconciliation_id,
    "Agency Comm Received (STMT)" as amount
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND reconciliation_id IS NOT NULL
    AND "Transaction ID" LIKE '%-STMT-%'
ORDER BY reconciliation_id, "Transaction ID"
LIMIT 10;