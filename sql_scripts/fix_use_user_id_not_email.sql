-- BETTER ARCHITECTURE: USE USER_ID INSTEAD OF EMAIL
-- Emails can change, IDs are forever

-- 1. First, let's see if you have a users table
SELECT 'Checking for users table:' as check;
SELECT 
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'users'
ORDER BY ordinal_position;

-- 2. If no users table exists, create one
CREATE TABLE IF NOT EXISTS users (
    user_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Add user_id to all tables (better than user_email)
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(user_id);

ALTER TABLE carriers 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(user_id);

ALTER TABLE mgas 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(user_id);

ALTER TABLE commission_rules 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(user_id);

ALTER TABLE carrier_mga_relationships 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(user_id);

-- 4. Migrate existing data
-- First, ensure users exist for all emails
INSERT INTO users (email)
SELECT DISTINCT user_email 
FROM (
    SELECT user_email FROM policies WHERE user_email IS NOT NULL
    UNION
    SELECT user_email FROM carriers WHERE user_email IS NOT NULL
    UNION
    SELECT user_email FROM commission_rules WHERE user_email IS NOT NULL
) emails
ON CONFLICT (email) DO NOTHING;

-- 5. Update all tables to use user_id
UPDATE policies p
SET user_id = u.user_id
FROM users u
WHERE p.user_email = u.email
  AND p.user_id IS NULL;

UPDATE carriers c
SET user_id = u.user_id
FROM users u
WHERE c.user_email = u.email
  AND c.user_id IS NULL;

UPDATE mgas m
SET user_id = u.user_id
FROM users u
WHERE m.user_email = u.email
  AND m.user_id IS NULL;

UPDATE commission_rules cr
SET user_id = u.user_id
FROM users u
WHERE cr.user_email = u.email
  AND cr.user_id IS NULL;

UPDATE carrier_mga_relationships cmr
SET user_id = u.user_id
FROM users u
WHERE cmr.user_email = u.email
  AND cmr.user_id IS NULL;

-- 6. Create indexes on user_id
CREATE INDEX IF NOT EXISTS idx_policies_user_id ON policies(user_id);
CREATE INDEX IF NOT EXISTS idx_carriers_user_id ON carriers(user_id);
CREATE INDEX IF NOT EXISTS idx_mgas_user_id ON mgas(user_id);
CREATE INDEX IF NOT EXISTS idx_commission_rules_user_id ON commission_rules(user_id);
CREATE INDEX IF NOT EXISTS idx_relationships_user_id ON carrier_mga_relationships(user_id);

-- 7. Show migration results
SELECT 'Migration Status:' as check;
SELECT 
    'policies' as table_name,
    COUNT(*) FILTER (WHERE user_id IS NOT NULL) as with_user_id,
    COUNT(*) FILTER (WHERE user_id IS NULL) as without_user_id
FROM policies
UNION ALL
SELECT 
    'carriers' as table_name,
    COUNT(*) FILTER (WHERE user_id IS NOT NULL) as with_user_id,
    COUNT(*) FILTER (WHERE user_id IS NULL) as without_user_id
FROM carriers
UNION ALL
SELECT 
    'commission_rules' as table_name,
    COUNT(*) FILTER (WHERE user_id IS NOT NULL) as with_user_id,
    COUNT(*) FILTER (WHERE user_id IS NULL) as without_user_id
FROM commission_rules;

-- 8. Future: Drop user_email columns after app is updated
-- ALTER TABLE policies DROP COLUMN user_email;
-- ALTER TABLE carriers DROP COLUMN user_email;
-- etc...