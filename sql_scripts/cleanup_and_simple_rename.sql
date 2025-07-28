-- BETTER APPROACH: Clean up and do simple rename

-- First, drop the duplicate column we created (this is safe since it's just a copy)
ALTER TABLE policies DROP COLUMN "Agent Comm %";

-- Then do a simple rename of the original column
ALTER TABLE policies 
RENAME COLUMN "Agent Comm (NEW 50% RWL 25%)" TO "Agent Comm %";

-- Verify the rename worked
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'policies' 
AND column_name LIKE '%Agent Comm%';