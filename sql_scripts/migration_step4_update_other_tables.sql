-- STEP 4: Update remaining tables with user_id
-- Run this fourth

-- Update carriers
UPDATE carriers c
SET user_id = u.id
FROM users u
WHERE LOWER(c.user_email) = LOWER(u.email)
AND c.user_id IS NULL;

-- Update mgas
UPDATE mgas m
SET user_id = u.id
FROM users u
WHERE LOWER(m.user_email) = LOWER(u.email)
AND m.user_id IS NULL;

-- Update commission_rules
UPDATE commission_rules cr
SET user_id = u.id
FROM users u
WHERE LOWER(cr.user_email) = LOWER(u.email)
AND cr.user_id IS NULL;

-- Update reconciliations if table exists
UPDATE reconciliations r
SET user_id = u.id
FROM users u
WHERE LOWER(r.user_email) = LOWER(u.email)
AND r.user_id IS NULL;

-- Update carrier_mga_relationships
UPDATE carrier_mga_relationships cmr
SET user_id = u.id
FROM users u
WHERE LOWER(cmr.user_email) = LOWER(u.email)
AND cmr.user_id IS NULL;

-- Verify all tables updated
SELECT 
    'carriers' as table_name, COUNT(*) as total, COUNT(user_id) as with_user_id
FROM carriers WHERE user_email IS NOT NULL
UNION ALL
SELECT 
    'mgas', COUNT(*), COUNT(user_id)
FROM mgas WHERE user_email IS NOT NULL
UNION ALL
SELECT 
    'commission_rules', COUNT(*), COUNT(user_id)
FROM commission_rules WHERE user_email IS NOT NULL;