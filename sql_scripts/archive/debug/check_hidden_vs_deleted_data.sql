-- CHECK IF DATA IS HIDDEN BY RLS VS ACTUALLY DELETED
-- Run this as database owner/admin in Supabase

-- 1. Bypass RLS completely to see ALL data
SET LOCAL row_level_security = OFF;

-- 2. Count ALL data regardless of RLS
SELECT 'Total Data Check (RLS OFF)' as check_type;

SELECT 'carriers (ALL)' as table_name, COUNT(*) as count FROM carriers
UNION ALL
SELECT 'mgas (ALL)' as table_name, COUNT(*) as count FROM mgas  
UNION ALL
SELECT 'commission_rules (ALL)' as table_name, COUNT(*) as count FROM commission_rules
UNION ALL
SELECT 'carrier_relationships (ALL)' as table_name, COUNT(*) as count FROM carrier_mga_relationships
ORDER BY table_name;

-- 3. Show commission rules by user
SELECT 
    'Commission Rules by User' as check_type,
    user_email,
    COUNT(*) as rule_count
FROM commission_rules
GROUP BY user_email
ORDER BY user_email;

-- 4. Check for any orphaned data
SELECT 
    'Orphaned MGAs (no relationships)' as check_type,
    mga_name
FROM mgas
WHERE mga_id NOT IN (
    SELECT DISTINCT mga_id 
    FROM carrier_mga_relationships 
    WHERE mga_id IS NOT NULL
);

-- 5. Turn RLS back on and check again
SET LOCAL row_level_security = ON;

SELECT 'With RLS ON' as check_type;
SELECT 'carriers (RLS ON)' as table_name, COUNT(*) as count FROM carriers
UNION ALL
SELECT 'mgas (RLS ON)' as table_name, COUNT(*) as count FROM mgas;