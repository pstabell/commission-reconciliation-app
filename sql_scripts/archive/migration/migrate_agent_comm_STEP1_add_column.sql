-- STEP 1: Add new column and copy data
-- This is SAFE - it only adds a column and copies data

-- Add the new column
ALTER TABLE policies ADD COLUMN IF NOT EXISTS "Agent Comm %" TEXT;

-- Copy data from old column to new column
UPDATE policies 
SET "Agent Comm %" = "Agent Comm (NEW 50% RWL 25%)"
WHERE "Agent Comm (NEW 50% RWL 25%)" IS NOT NULL;