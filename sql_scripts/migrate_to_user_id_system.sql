-- PERMANENT FIX: Migrate from email-based to user_id-based data isolation
-- This will solve all case sensitivity issues forever

-- STEP 1: Check current state
SELECT 'Current email variations in policies:' as status;
SELECT user_email, COUNT(*) as count
FROM policies
WHERE LOWER(user_email) LIKE '%demo%'
GROUP BY user_email;

-- STEP 2: Ensure all users exist in users table
-- First consolidate all email variations to lowercase
INSERT INTO users (email)
SELECT DISTINCT LOWER(user_email) as email
FROM (
    SELECT user_email FROM policies WHERE user_email IS NOT NULL
    UNION
    SELECT user_email FROM carriers WHERE user_email IS NOT NULL
    UNION
    SELECT user_email FROM mgas WHERE user_email IS NOT NULL
    UNION
    SELECT user_email FROM commission_rules WHERE user_email IS NOT NULL
) all_emails
ON CONFLICT (email) DO NOTHING;

-- STEP 3: Add user_id columns to all tables
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);

ALTER TABLE carriers 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);

ALTER TABLE mgas 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);

ALTER TABLE commission_rules 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);

ALTER TABLE reconciliations 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);

ALTER TABLE carrier_mga_relationships 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);

-- STEP 4: Populate user_id based on email (case-insensitive)
UPDATE policies p
SET user_id = u.id
FROM users u
WHERE LOWER(p.user_email) = LOWER(u.email)
AND p.user_id IS NULL;

UPDATE carriers c
SET user_id = u.id
FROM users u
WHERE LOWER(c.user_email) = LOWER(u.email)
AND c.user_id IS NULL;

UPDATE mgas m
SET user_id = u.id
FROM users u
WHERE LOWER(m.user_email) = LOWER(u.email)
AND m.user_id IS NULL;

UPDATE commission_rules cr
SET user_id = u.id
FROM users u
WHERE LOWER(cr.user_email) = LOWER(u.email)
AND cr.user_id IS NULL;

UPDATE reconciliations r
SET user_id = u.id
FROM users u
WHERE LOWER(r.user_email) = LOWER(u.email)
AND r.user_id IS NULL;

UPDATE carrier_mga_relationships cmr
SET user_id = u.id
FROM users u
WHERE LOWER(cmr.user_email) = LOWER(u.email)
AND cmr.user_id IS NULL;

-- STEP 5: Verify migration
SELECT 'Migration Results:' as status;
SELECT 
    'policies' as table_name,
    COUNT(*) as total_records,
    COUNT(user_id) as records_with_user_id,
    COUNT(*) - COUNT(user_id) as missing_user_id
FROM policies
WHERE user_email IS NOT NULL
UNION ALL
SELECT 
    'carriers' as table_name,
    COUNT(*) as total_records,
    COUNT(user_id) as records_with_user_id,
    COUNT(*) - COUNT(user_id) as missing_user_id
FROM carriers
WHERE user_email IS NOT NULL
UNION ALL
SELECT 
    'mgas' as table_name,
    COUNT(*) as total_records,
    COUNT(user_id) as records_with_user_id,
    COUNT(*) - COUNT(user_id) as missing_user_id
FROM mgas
WHERE user_email IS NOT NULL
UNION ALL
SELECT 
    'commission_rules' as table_name,
    COUNT(*) as total_records,
    COUNT(user_id) as records_with_user_id,
    COUNT(*) - COUNT(user_id) as missing_user_id
FROM commission_rules
WHERE user_email IS NOT NULL;

-- STEP 6: Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_policies_user_id ON policies(user_id);
CREATE INDEX IF NOT EXISTS idx_carriers_user_id ON carriers(user_id);
CREATE INDEX IF NOT EXISTS idx_mgas_user_id ON mgas(user_id);
CREATE INDEX IF NOT EXISTS idx_commission_rules_user_id ON commission_rules(user_id);
CREATE INDEX IF NOT EXISTS idx_reconciliations_user_id ON reconciliations(user_id);
CREATE INDEX IF NOT EXISTS idx_carrier_mga_relationships_user_id ON carrier_mga_relationships(user_id);

-- STEP 7: Show demo user's final state
SELECT 'Demo user final state:' as status;
SELECT 
    u.id as user_id,
    u.email,
    COUNT(DISTINCT p."Transaction ID") as total_policies
FROM users u
LEFT JOIN policies p ON p.user_id = u.id
WHERE LOWER(u.email) = 'demo@agentcommissiontracker.com'
GROUP BY u.id, u.email;