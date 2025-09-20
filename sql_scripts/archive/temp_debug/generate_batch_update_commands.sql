-- Generate UPDATE commands to add batch IDs to demo reconciliation data
-- This will output SQL commands that you can review and run

-- First, let's see what we're working with
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT substring("Transaction ID" from '.*-STMT-(\d{8})$')) as unique_dates
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction ID" LIKE '%-STMT-%'
    AND reconciliation_id IS NULL;

-- Show the unique dates that will become batches
SELECT DISTINCT 
    substring("Transaction ID" from '.*-STMT-(\d{8})$') as statement_date,
    'DEMO-RECON-' || substring("Transaction ID" from '.*-STMT-(\d{8})$') as batch_id,
    COUNT(*) as transaction_count
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction ID" LIKE '%-STMT-%'
    AND reconciliation_id IS NULL
GROUP BY statement_date
ORDER BY statement_date;

-- Alternative: Let's check if we can just add the column data directly
-- First, let's see a sample of what would be updated
SELECT 
    _id,
    "Transaction ID",
    'DEMO-RECON-' || substring("Transaction ID" from '.*-STMT-(\d{8})$') as proposed_batch_id
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction ID" LIKE '%-STMT-%'
    AND reconciliation_id IS NULL
LIMIT 20;

-- If the trigger is the issue, we might need to:
-- 1. Contact Supabase support to fix the trigger
-- 2. Add an 'updated_at' column to the policies table
-- 3. Or use the Supabase dashboard to manually update these records

-- For now, let's at least see what the end result would look like
-- This query shows what the data WOULD look like after the update
SELECT 
    "Transaction ID",
    'DEMO-RECON-' || substring("Transaction ID" from '.*-STMT-(\d{8})$') as reconciliation_id,
    "Agency Comm Received (STMT)" as amount,
    "STMT DATE"
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction ID" LIKE '%-STMT-%'
ORDER BY reconciliation_id, "Transaction ID"
LIMIT 30;