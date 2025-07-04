-- Add missing columns to commission_payments table to match application requirements

-- Add policy_number column
ALTER TABLE commission_payments 
ADD COLUMN IF NOT EXISTS policy_number TEXT;

-- Add statement_date column
ALTER TABLE commission_payments 
ADD COLUMN IF NOT EXISTS statement_date TEXT;

-- Add payment_timestamp column
ALTER TABLE commission_payments 
ADD COLUMN IF NOT EXISTS payment_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Add statement_details column
ALTER TABLE commission_payments 
ADD COLUMN IF NOT EXISTS statement_details TEXT;

-- Create indexes for the new columns
CREATE INDEX IF NOT EXISTS idx_commission_payments_policy_number ON commission_payments(policy_number);
CREATE INDEX IF NOT EXISTS idx_commission_payments_statement_date ON commission_payments(statement_date);

-- Verify the updated table structure
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'commission_payments'
ORDER BY ordinal_position;