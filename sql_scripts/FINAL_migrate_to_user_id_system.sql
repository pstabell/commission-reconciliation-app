-- FINAL MIGRATION: From email-based to user_id-based system
-- This will permanently solve all case sensitivity issues

-- STEP 1: Ensure users table has all current users (case-insensitive)
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

-- Verify users were created
SELECT 'Users created:' as status;
SELECT id, email FROM users ORDER BY email;

-- STEP 2: Add user_id columns to all tables (if not exists)
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

-- STEP 3: Populate user_id in all tables (case-insensitive matching)
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

-- STEP 4: Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_policies_user_id ON policies(user_id);
CREATE INDEX IF NOT EXISTS idx_carriers_user_id ON carriers(user_id);
CREATE INDEX IF NOT EXISTS idx_mgas_user_id ON mgas(user_id);
CREATE INDEX IF NOT EXISTS idx_commission_rules_user_id ON commission_rules(user_id);
CREATE INDEX IF NOT EXISTS idx_reconciliations_user_id ON reconciliations(user_id);
CREATE INDEX IF NOT EXISTS idx_carrier_mga_relationships_user_id ON carrier_mga_relationships(user_id);

-- STEP 5: Verify migration success
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

-- STEP 6: Check demo user specifically
SELECT 'Demo user verification:' as status;
SELECT 
    u.id as user_id,
    u.email,
    COUNT(DISTINCT p."Transaction ID") as total_policies,
    COUNT(DISTINCT c.carrier_id) as total_carriers,
    COUNT(DISTINCT m.mga_id) as total_mgas,
    COUNT(DISTINCT cr.rule_id) as total_rules
FROM users u
LEFT JOIN policies p ON p.user_id = u.id
LEFT JOIN carriers c ON c.user_id = u.id
LEFT JOIN mgas m ON m.user_id = u.id
LEFT JOIN commission_rules cr ON cr.user_id = u.id
WHERE u.email = 'demo@agentcommissiontracker.com'
GROUP BY u.id, u.email;

-- IMPORTANT: After running this migration and updating the app code,
-- we can later drop the user_email columns entirely