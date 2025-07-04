-- SQL script to update column name from (AZ) to (CRM) if needed
-- This updates the column name in the policies table schema

-- For PostgreSQL/Supabase:
-- Note: Only run this if your database actually has a column with (AZ) in the name
-- First check if column exists:
-- SELECT column_name FROM information_schema.columns 
-- WHERE table_name = 'policies' AND column_name LIKE '%AZ%';

-- If column exists with (AZ), rename it:
-- ALTER TABLE policies 
-- RENAME COLUMN "Agency Estimated Comm/Revenue (AZ)" 
-- TO "Agency Estimated Comm/Revenue (CRM)";

-- Note: The application code has been updated to use (CRM) everywhere
-- Column mapping configuration already uses (CRM)