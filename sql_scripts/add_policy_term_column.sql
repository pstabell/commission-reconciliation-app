-- Add Policy Term column to policies table
-- This script adds the Policy Term column to track policy duration (6 months, 12 months, etc.)
-- This will improve renewal calculations on the Pending Policy Renewals page

-- Add the Policy Term column to the policies table
-- Stores the policy term as a simple integer representing months
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS "Policy Term" INTEGER;

-- Add a CHECK constraint to ensure valid values
-- Common policy terms: 3, 6, 9, 12 months
ALTER TABLE policies 
ADD CONSTRAINT chk_policy_term 
CHECK ("Policy Term" IS NULL OR "Policy Term" IN (3, 6, 9, 12));

-- Add an index on Policy Term for better query performance
CREATE INDEX IF NOT EXISTS idx_policies_policy_term ON policies("Policy Term");

-- Optional: Set default values based on existing data
-- This query attempts to calculate the term based on effective and expiration dates
-- Uncomment and run if you want to populate existing records
/*
UPDATE policies 
SET "Policy Term" = 
  CASE 
    WHEN "X-DATE" IS NOT NULL AND "Effective Date" IS NOT NULL THEN
      CASE 
        WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 80 AND 100 THEN 3
        WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 170 AND 190 THEN 6
        WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 260 AND 280 THEN 9
        WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 355 AND 375 THEN 12
        ELSE NULL  -- Don't guess if it doesn't match common terms
      END
    ELSE NULL
  END
WHERE "Policy Term" IS NULL 
  AND "Transaction Type" IN ('NEW', 'RWL');
*/