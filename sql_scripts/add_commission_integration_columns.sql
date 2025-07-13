-- Add commission integration columns to policies table
-- This enables linking policies to carriers/MGAs and commission rules
-- All columns are NULLABLE for backward compatibility

-- Step 1: Add foreign key columns to policies table
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS carrier_id UUID REFERENCES carriers(carrier_id),
ADD COLUMN IF NOT EXISTS mga_id UUID REFERENCES mgas(mga_id),
ADD COLUMN IF NOT EXISTS commission_rule_id UUID REFERENCES commission_rules(rule_id),
ADD COLUMN IF NOT EXISTS commission_rate_override DECIMAL(5,2),
ADD COLUMN IF NOT EXISTS override_reason TEXT;

-- Step 2: Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_policies_carrier_id ON policies(carrier_id);
CREATE INDEX IF NOT EXISTS idx_policies_mga_id ON policies(mga_id);
CREATE INDEX IF NOT EXISTS idx_policies_commission_rule_id ON policies(commission_rule_id);
CREATE INDEX IF NOT EXISTS idx_policies_commission_override ON policies(commission_rate_override) WHERE commission_rate_override IS NOT NULL;

-- Step 3: Add comments to document the new columns
COMMENT ON COLUMN policies.carrier_id IS 'Foreign key to carriers table - links policy to carrier';
COMMENT ON COLUMN policies.mga_id IS 'Foreign key to mgas table - links policy to MGA (NULL for direct appointments)';
COMMENT ON COLUMN policies.commission_rule_id IS 'Foreign key to commission_rules table - tracks which rule was used';
COMMENT ON COLUMN policies.commission_rate_override IS 'Manual override of commission rate (stores actual rate used if different from rule)';
COMMENT ON COLUMN policies.override_reason IS 'Reason for commission rate override (required when override is used)';

-- Step 4: Verify the changes
SELECT 
    'New columns added successfully' as status,
    COUNT(*) as total_policies
FROM policies;

-- Step 5: Show sample of updated table structure
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'policies' 
    AND column_name IN ('carrier_id', 'mga_id', 'commission_rule_id', 'commission_rate_override', 'override_reason')
ORDER BY ordinal_position;

-- Step 6: Show existing policies are unaffected
SELECT 
    'Existing policies preserved' as status,
    COUNT(*) as count,
    MIN("Transaction ID") as first_transaction,
    MAX("Transaction ID") as last_transaction
FROM policies 
WHERE carrier_id IS NULL; -- All existing policies will have NULL values

-- Step 7: Test foreign key constraints work
-- This query will show carrier/MGA combinations available for testing
SELECT 
    c.carrier_name,
    COALESCE(m.mga_name, 'Direct Appointment') as mga_option,
    c.carrier_id,
    m.mga_id,
    COUNT(cr.rule_id) as available_rules
FROM carriers c
LEFT JOIN commission_rules cr ON c.carrier_id = cr.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
GROUP BY c.carrier_id, c.carrier_name, m.mga_id, m.mga_name
ORDER BY c.carrier_name, mga_option
LIMIT 10;