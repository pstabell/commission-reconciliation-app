-- Fix the policies table by adding the missing updated_at column

-- First, check if the column already exists
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'policies' 
AND column_name = 'updated_at';

-- Add the updated_at column if it doesn't exist
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();

-- Now we can run the original update
UPDATE policies
SET reconciliation_id = 'DEMO-RECON-' || substring("Transaction ID" from '.*-STMT-(\d{8})$')
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND reconciliation_id IS NULL
    AND "Transaction ID" ~ '.*-STMT-\d{8}$';

-- Verify the update worked
SELECT 
    reconciliation_id as batch_id,
    COUNT(*) as transaction_count,
    to_date(substring(reconciliation_id from 'DEMO-RECON-(\d{8})'), 'YYYYMMDD') as statement_date
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND reconciliation_id IS NOT NULL
    AND "Transaction ID" LIKE '%-STMT-%'
GROUP BY reconciliation_id
ORDER BY statement_date DESC;

-- Show that batches now appear correctly
SELECT 
    COUNT(DISTINCT reconciliation_id) as total_batches,
    COUNT(*) as total_transactions
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND reconciliation_id IS NOT NULL
    AND "Transaction ID" LIKE '%-STMT-%';