-- Add MGA Name column to policies table
-- This script adds the MGA Name column after Carrier Name to track Managing General Agent information

-- Add the MGA Name column to the policies table
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS "MGA Name" TEXT;

-- Add an index on MGA Name for better search performance
CREATE INDEX IF NOT EXISTS idx_policies_mga_name ON policies("MGA Name");

-- Optional: Update any existing records with a default value if needed
-- UPDATE policies SET "MGA Name" = '' WHERE "MGA Name" IS NULL;