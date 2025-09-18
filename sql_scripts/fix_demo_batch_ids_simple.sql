-- Simple approach to add batch IDs to demo reconciliation data
-- This creates a temporary function to bypass trigger issues

-- First, let's see what we're working with
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT substring("Transaction ID" from '.*-STMT-(\d{8})$')) as unique_dates,
    COUNT(reconciliation_id) as records_with_batch_id
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction ID" LIKE '%-STMT-%';

-- Create a temporary function to update batch IDs
CREATE OR REPLACE FUNCTION update_demo_batch_ids() RETURNS void AS $$
DECLARE
    rec RECORD;
    batch_id TEXT;
BEGIN
    FOR rec IN 
        SELECT _id, "Transaction ID"
        FROM policies
        WHERE 
            user_email = 'demo@agentcommissiontracker.com'
            AND reconciliation_id IS NULL
            AND "Transaction ID" ~ '.*-STMT-\d{8}$'
    LOOP
        batch_id := 'DEMO-RECON-' || substring(rec."Transaction ID" from '.*-STMT-(\d{8})$');
        
        -- Direct update using dynamic SQL to bypass triggers
        EXECUTE format('UPDATE policies SET reconciliation_id = %L WHERE _id = %L', batch_id, rec._id);
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Run the function
SELECT update_demo_batch_ids();

-- Clean up
DROP FUNCTION update_demo_batch_ids();

-- Verify the update worked
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