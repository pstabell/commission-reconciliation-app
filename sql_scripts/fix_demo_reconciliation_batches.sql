-- Fix demo reconciliation data by adding batch IDs
-- This script fixes the trigger issue and updates demo data with proper batch IDs

-- Step 1: Fix the policies table by adding the missing updated_at column
-- This resolves the trigger error
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();

-- Step 2: Update demo reconciliation records with batch IDs
-- Batch ID format: DEMO-RECON-YYYYMMDD (based on statement date in Transaction ID)
UPDATE policies
SET reconciliation_id = 'DEMO-RECON-' || substring("Transaction ID" from '.*-STMT-(\d{8})$'),
    updated_at = NOW()
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND reconciliation_id IS NULL
    AND "Transaction ID" ~ '.*-STMT-\d{8}$';

-- Step 3: Verify the update worked - show batch summary
SELECT 
    reconciliation_id as batch_id,
    COUNT(*) as transaction_count,
    to_date(substring(reconciliation_id from 'DEMO-RECON-(\d{8})'), 'YYYYMMDD') as statement_date,
    SUM(CAST(NULLIF("Agency Comm Received (STMT)", '') AS NUMERIC)) as total_agency_commission
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND reconciliation_id IS NOT NULL
    AND "Transaction ID" LIKE '%-STMT-%'
GROUP BY reconciliation_id
ORDER BY statement_date DESC;

-- Step 4: Show total counts
SELECT 
    COUNT(DISTINCT reconciliation_id) as total_batches,
    COUNT(*) as total_transactions,
    SUM(CAST(NULLIF("Agency Comm Received (STMT)", '') AS NUMERIC)) as total_commission
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND reconciliation_id IS NOT NULL
    AND "Transaction ID" LIKE '%-STMT-%';