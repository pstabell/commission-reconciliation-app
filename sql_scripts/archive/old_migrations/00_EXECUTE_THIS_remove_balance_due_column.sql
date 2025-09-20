-- IMPORTANT: Execute this script in Supabase SQL Editor to remove the Balance Due column
-- This removes the "Balance Due" column from the policies table as it's no longer needed

-- Step 1: Drop the Balance Due column from policies table
ALTER TABLE policies 
DROP COLUMN IF EXISTS "Balance Due";

-- Step 2: Also check for variations of the column name and drop them
ALTER TABLE policies 
DROP COLUMN IF EXISTS "BALANCE DUE";

ALTER TABLE policies 
DROP COLUMN IF EXISTS "balance_due";

-- Step 3: Verify the column was removed successfully
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'policies' 
AND (column_name ILIKE '%balance%due%')
ORDER BY column_name;

-- Expected result: No rows should be returned, confirming Balance Due column is removed