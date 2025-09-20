-- IMPORTANT: Execute this script in Supabase SQL Editor to rename the column
-- This renames "Agency Gross Comm Received" to "Agency Comm Received (STMT)" 
-- in the policies table to match the UI and prevent mapping confusion

-- Step 1: Rename the column in policies table
ALTER TABLE policies 
RENAME COLUMN "Agency Gross Comm Received" TO "Agency Comm Received (STMT)";

-- Step 2: Verify the column was renamed successfully
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'policies' 
AND column_name LIKE '%Agency%Comm%'
ORDER BY column_name;

-- Expected result: You should see "Agency Comm Received (STMT)" in the results
-- If successful, the application will no longer need to map between different column names