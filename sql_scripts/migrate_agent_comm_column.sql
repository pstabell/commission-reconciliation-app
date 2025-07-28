-- Migration Script: Rename "Agent Comm (NEW 50% RWL 25%)" to "Agent Comm %"
-- Date: 2025-01-27
-- IMPORTANT: Run each step separately and verify before proceeding to the next

-- Step 1: Add the new column
ALTER TABLE policies ADD COLUMN IF NOT EXISTS "Agent Comm %" TEXT;

-- Step 2: Copy data from old column to new column
UPDATE policies 
SET "Agent Comm %" = "Agent Comm (NEW 50% RWL 25%)"
WHERE "Agent Comm (NEW 50% RWL 25%)" IS NOT NULL;

-- Step 3: Verify data was copied correctly
-- This should return 0 rows if migration is successful
SELECT COUNT(*) as mismatch_count
FROM policies 
WHERE ("Agent Comm %" != "Agent Comm (NEW 50% RWL 25%)" 
       AND "Agent Comm (NEW 50% RWL 25%)" IS NOT NULL)
   OR ("Agent Comm %" IS NULL AND "Agent Comm (NEW 50% RWL 25%)" IS NOT NULL);

-- Step 4: Check a few sample records
SELECT 
    "Transaction ID",
    "Customer",
    "Agent Comm (NEW 50% RWL 25%)" as old_column,
    "Agent Comm %" as new_column
FROM policies
LIMIT 10;

-- Step 5: ONLY AFTER VERIFICATION - Drop the old column
-- DANGER: This is irreversible! Make sure you have a backup!
ALTER TABLE policies DROP COLUMN "Agent Comm (NEW 50% RWL 25%)";

-- Rollback Script (if needed):
-- ALTER TABLE policies ADD COLUMN "Agent Comm (NEW 50% RWL 25%)" TEXT;
-- UPDATE policies SET "Agent Comm (NEW 50% RWL 25%)" = "Agent Comm %";
-- ALTER TABLE policies DROP COLUMN "Agent Comm %";