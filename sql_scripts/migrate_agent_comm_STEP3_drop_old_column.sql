-- STEP 3: Drop the old column
-- ⚠️ WARNING: ONLY RUN THIS AFTER:
-- 1. You've verified the data copied correctly in STEP 2
-- 2. You've exported/backed up your data
-- 3. You're confident the migration worked

-- This is IRREVERSIBLE in Supabase!
ALTER TABLE policies DROP COLUMN "Agent Comm (NEW 50% RWL 25%)";

-- After dropping, verify the new column exists and has data
SELECT 
    COUNT(*) as total_records,
    COUNT("Agent Comm %") as new_column_count
FROM policies;