-- Update Policy Term constraint to allow "Custom" value
-- This script modifies the constraint to allow special policy terms like cancellations

-- First, we need to change the column type to TEXT to allow "Custom"
-- This requires dropping and recreating the column
BEGIN;

-- Drop the existing constraint
ALTER TABLE policies 
DROP CONSTRAINT IF EXISTS chk_policy_term;

-- Change column type to TEXT to allow both numbers and "Custom"
ALTER TABLE policies 
ALTER COLUMN "Policy Term" TYPE TEXT;

-- Add new constraint that allows 3, 6, 9, 12, or 'Custom'
ALTER TABLE policies 
ADD CONSTRAINT chk_policy_term 
CHECK ("Policy Term" IS NULL OR "Policy Term" IN ('3', '6', '9', '12', 'Custom'));

-- Update any existing integer values to text format
UPDATE policies 
SET "Policy Term" = "Policy Term"::TEXT 
WHERE "Policy Term" IS NOT NULL;

COMMIT;

-- Note: The index on Policy Term will still work with TEXT type