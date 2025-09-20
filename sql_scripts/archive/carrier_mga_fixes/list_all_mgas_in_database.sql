-- LIST ALL MGAS IN YOUR PRIVATE DATABASE
-- Run this in your PRIVATE database

-- 1. Count all MGAs in mgas table (including unused ones)
SELECT 'TOTAL MGAS IN DATABASE:' as info, COUNT(*) as count FROM mgas;

-- 2. List ALL MGAs with their usage
SELECT '';
SELECT 'ALL MGAS WITH USAGE COUNT:' as info;
SELECT 
    m.mga_id,
    m.mga_name,
    m.status,
    COUNT(cr.rule_id) as rules_using_this_mga
FROM mgas m
LEFT JOIN commission_rules cr ON m.mga_id = cr.mga_id AND cr.is_active = true
GROUP BY m.mga_id, m.mga_name, m.status
ORDER BY m.mga_name;

-- 3. Generate INSERT statements for ALL MGAs
SELECT '';
SELECT '-- INSERT STATEMENTS FOR ALL MGAS:' as info;
SELECT 
    'INSERT INTO mgas (mga_id, mga_name, status, user_email) VALUES (''' 
    || mga_id || ''', ''' 
    || REPLACE(mga_name, '''', '''''') || ''', ''' 
    || COALESCE(status, 'Active') || ''', ''Demo@AgentCommissionTracker.com'');' as sql
FROM mgas
ORDER BY mga_name;