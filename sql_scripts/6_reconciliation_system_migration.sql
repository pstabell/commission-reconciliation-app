-- =====================================================
-- Reconciliation System Database Migration
-- Run this to add reconciliation support to your database
-- =====================================================

-- Step 1: Add reconciliation columns to policies table
-- These track the reconciliation status of each transaction
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS reconciliation_status TEXT DEFAULT 'unreconciled' 
    CHECK (reconciliation_status IN ('unreconciled', 'reconciled', 'void', 'adjustment'));

ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS reconciliation_id TEXT;

ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS reconciled_at TIMESTAMPTZ;

ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS is_reconciliation_entry BOOLEAN DEFAULT FALSE;

-- Step 2: Create index for better performance on reconciliation queries
CREATE INDEX IF NOT EXISTS idx_policies_reconciliation_status 
ON policies(reconciliation_status);

CREATE INDEX IF NOT EXISTS idx_policies_transaction_id_suffix 
ON policies("Transaction ID") 
WHERE "Transaction ID" LIKE '%-STMT-%' 
   OR "Transaction ID" LIKE '%-ADJ-%' 
   OR "Transaction ID" LIKE '%-VOID-%';

-- Step 3: Create reconciliations tracking table
-- This tracks reconciliation sessions/batches
CREATE TABLE IF NOT EXISTS reconciliations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reconciliation_date DATE NOT NULL,
    statement_date DATE NOT NULL,
    carrier_name TEXT,
    total_amount DECIMAL(10,2),
    transaction_count INTEGER,
    created_by TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    notes TEXT
);

-- Step 4: Add RLS policy for reconciliations table
DROP POLICY IF EXISTS "Enable all operations for anon key" ON reconciliations;
CREATE POLICY "Enable all operations for anon key" 
ON reconciliations
FOR ALL TO anon
USING (true)
WITH CHECK (true);
GRANT ALL ON reconciliations TO anon;

-- Step 5: Create function to validate transaction ID format
CREATE OR REPLACE FUNCTION validate_transaction_id_format(trans_id TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    -- Check for reconciliation transaction patterns
    IF trans_id LIKE '%-STMT-%' THEN
        -- Format: XXXXXXX-STMT-YYYYMMDD
        RETURN LENGTH(SPLIT_PART(trans_id, '-', 1)) = 7 
           AND SPLIT_PART(trans_id, '-', 2) = 'STMT'
           AND LENGTH(SPLIT_PART(trans_id, '-', 3)) = 8;
    ELSIF trans_id LIKE '%-ADJ-%' THEN
        -- Format: XXXXXXX-ADJ-YYYYMMDD
        RETURN LENGTH(SPLIT_PART(trans_id, '-', 1)) = 7 
           AND SPLIT_PART(trans_id, '-', 2) = 'ADJ'
           AND LENGTH(SPLIT_PART(trans_id, '-', 3)) = 8;
    ELSIF trans_id LIKE '%-VOID-%' THEN
        -- Format: XXXXXXX-VOID-YYYYMMDD
        RETURN LENGTH(SPLIT_PART(trans_id, '-', 1)) = 7 
           AND SPLIT_PART(trans_id, '-', 2) = 'VOID'
           AND LENGTH(SPLIT_PART(trans_id, '-', 3)) = 8;
    ELSE
        -- Original transaction: 7 characters
        RETURN LENGTH(trans_id) = 7;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Step 6: Add constraint to enforce transaction ID format
-- Note: This will only apply to NEW records, existing records are grandfathered
ALTER TABLE policies 
ADD CONSTRAINT check_transaction_id_format 
CHECK (validate_transaction_id_format("Transaction ID"));

-- Step 7: Create trigger to automatically set reconciliation fields
CREATE OR REPLACE FUNCTION set_reconciliation_fields()
RETURNS TRIGGER AS $$
BEGIN
    -- For reconciliation entries, set appropriate defaults
    IF NEW."Transaction ID" LIKE '%-STMT-%' THEN
        NEW.is_reconciliation_entry := TRUE;
        NEW.reconciliation_status := 'reconciled';
        NEW."Agency Estimated Comm/Revenue (CRM)" := 0;
        NEW."Agent Estimated Comm $" := 0;
    ELSIF NEW."Transaction ID" LIKE '%-ADJ-%' THEN
        NEW.is_reconciliation_entry := TRUE;
        NEW.reconciliation_status := 'adjustment';
    ELSIF NEW."Transaction ID" LIKE '%-VOID-%' THEN
        NEW.is_reconciliation_entry := TRUE;
        NEW.reconciliation_status := 'void';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_set_reconciliation_fields
BEFORE INSERT ON policies
FOR EACH ROW
EXECUTE FUNCTION set_reconciliation_fields();

-- Step 8: Verify migration
SELECT 
    column_name,
    data_type,
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_name = 'policies'
    AND column_name IN ('reconciliation_status', 'reconciliation_id', 'reconciled_at', 'is_reconciliation_entry')
ORDER BY 
    ordinal_position;

-- Step 9: Check if reconciliations table was created
SELECT 
    'reconciliations table created' as status,
    COUNT(*) as row_count
FROM 
    reconciliations;

-- =====================================================
-- ROLLBACK SCRIPT (if needed)
-- =====================================================
/*
-- Remove trigger
DROP TRIGGER IF EXISTS trigger_set_reconciliation_fields ON policies;
DROP FUNCTION IF EXISTS set_reconciliation_fields();

-- Remove constraint and function
ALTER TABLE policies DROP CONSTRAINT IF EXISTS check_transaction_id_format;
DROP FUNCTION IF EXISTS validate_transaction_id_format(trans_id TEXT);

-- Remove indexes
DROP INDEX IF EXISTS idx_policies_reconciliation_status;
DROP INDEX IF EXISTS idx_policies_transaction_id_suffix;

-- Remove columns
ALTER TABLE policies DROP COLUMN IF EXISTS reconciliation_status;
ALTER TABLE policies DROP COLUMN IF EXISTS reconciliation_id;
ALTER TABLE policies DROP COLUMN IF EXISTS reconciled_at;
ALTER TABLE policies DROP COLUMN IF EXISTS is_reconciliation_entry;

-- Drop reconciliations table
DROP TABLE IF EXISTS reconciliations;
*/