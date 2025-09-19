-- ADD MISSING MGAS TO DEMO ACCOUNT
-- Run this AFTER the main import script to add the 4 missing MGAs

-- Check if these MGAs already exist for demo user
SELECT 'CHECKING FOR MISSING MGAS:' as info;
SELECT mga_name 
FROM (VALUES 
    ('BTIS'),
    ('Empire Underwrites LLC'),
    ('E&S Market'),
    ('MacNeill Group')
) AS missing(mga_name)
WHERE NOT EXISTS (
    SELECT 1 FROM mgas 
    WHERE mgas.mga_name = missing.mga_name 
    AND user_email = 'Demo@AgentCommissionTracker.com'
);

-- Insert the 4 missing MGAs
INSERT INTO mgas (mga_id, mga_name, status, user_email) 
SELECT * FROM (VALUES
    ('9700fdff-1628-4a32-b927-1edc53df440c', 'BTIS', 'Active', 'Demo@AgentCommissionTracker.com'),
    ('fb6cba2b-8053-44f9-bc72-d776fa16e4dc', 'Empire Underwrites LLC', 'Active', 'Demo@AgentCommissionTracker.com'),
    ('61cf2fd5-1ca3-4b9b-9d54-06ee34964677', 'E&S Market', 'Active', 'Demo@AgentCommissionTracker.com'),
    ('b87d54a6-d421-4b39-8a03-17a56156a99f', 'MacNeill Group', 'Active', 'Demo@AgentCommissionTracker.com')
) AS new_mgas(mga_id, mga_name, status, user_email)
WHERE NOT EXISTS (
    SELECT 1 FROM mgas 
    WHERE mgas.mga_id = new_mgas.mga_id 
    AND mgas.user_email = 'Demo@AgentCommissionTracker.com'
);

-- Verify final count
SELECT '';
SELECT 'FINAL MGA COUNT FOR DEMO:' as info;
SELECT COUNT(*) || ' Active MGAs' as count
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com' 
AND status = 'Active';

-- List all MGAs for demo
SELECT '';
SELECT 'ALL DEMO MGAS:' as info;
SELECT mga_name 
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY mga_name;