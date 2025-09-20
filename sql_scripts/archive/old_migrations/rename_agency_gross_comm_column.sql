-- Rename "Agency Gross Comm Received" to "Agency Comm Received (STMT)" in policies table
ALTER TABLE policies 
RENAME COLUMN "Agency Gross Comm Received" TO "Agency Comm Received (STMT)";

-- Verify the column was renamed
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'policies' 
AND column_name LIKE '%Agency%Comm%'
ORDER BY column_name;