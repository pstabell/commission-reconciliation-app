-- Add effective date tracking to commission rules
-- This allows tracking rate changes over time without losing history

-- Step 1: Add the new columns
ALTER TABLE commission_rules 
ADD COLUMN IF NOT EXISTS effective_date DATE DEFAULT CURRENT_DATE,
ADD COLUMN IF NOT EXISTS end_date DATE,
ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true;

-- Step 2: Create an index for faster date-based queries
CREATE INDEX IF NOT EXISTS idx_commission_rules_dates ON commission_rules(effective_date, end_date);
CREATE INDEX IF NOT EXISTS idx_commission_rules_active ON commission_rules(is_active);

-- Step 3: Update all existing rules to have today as their effective date
UPDATE commission_rules 
SET effective_date = CURRENT_DATE 
WHERE effective_date IS NULL;

-- Step 4: Verify the changes worked
SELECT 
    'Commission rules with dates added:' as status, 
    COUNT(*) as count 
FROM commission_rules 
WHERE effective_date IS NOT NULL;

-- Step 5: Show sample of updated rules
SELECT 
    c.carrier_name,
    COALESCE(m.mga_name, 'Direct') as mga,
    cr.policy_type,
    cr.new_rate || '%' as new_rate,
    cr.renewal_rate || '%' as renewal_rate,
    TO_CHAR(cr.effective_date, 'MM/DD/YYYY') as effective_date,
    CASE 
        WHEN cr.end_date IS NULL THEN 'Current'
        ELSE TO_CHAR(cr.end_date, 'MM/DD/YYYY')
    END as end_date,
    cr.is_active
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
ORDER BY c.carrier_name, cr.effective_date DESC
LIMIT 10;