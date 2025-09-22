-- STEP 1: Create users from existing emails
-- Run this first

-- Ensure users table has all current users (case-insensitive)
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
SELECT id, email FROM users ORDER BY email;