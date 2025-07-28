-- STEP 2: Verify the migration worked correctly
-- Run these queries to check the data

-- Check if any data didn't copy correctly (should return 0)
SELECT COUNT(*) as mismatch_count
FROM policies 
WHERE ("Agent Comm %" != "Agent Comm (NEW 50% RWL 25%)" 
       AND "Agent Comm (NEW 50% RWL 25%)" IS NOT NULL)
   OR ("Agent Comm %" IS NULL AND "Agent Comm (NEW 50% RWL 25%)" IS NOT NULL);

-- View sample records to visually verify
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Agent Comm (NEW 50% RWL 25%)" as old_column,
    "Agent Comm %" as new_column
FROM policies
WHERE "Agent Comm (NEW 50% RWL 25%)" IS NOT NULL
LIMIT 20;

-- Count total records with data
SELECT 
    COUNT(*) as total_records,
    COUNT("Agent Comm (NEW 50% RWL 25%)") as old_column_count,
    COUNT("Agent Comm %") as new_column_count
FROM policies;