-- RESTORE CARRIERS, MGAS, AND COMMISSION RULES FOR DEMO USER
-- Run this in Supabase SQL Editor

-- 1. First, make sure RLS is disabled on shared tables
ALTER TABLE carriers DISABLE ROW LEVEL SECURITY;
ALTER TABLE mgas DISABLE ROW LEVEL SECURITY;

-- 2. Insert essential carriers
INSERT INTO carriers (carrier_name, status, notes) VALUES
('Citizens', 'Active', 'Citizens Property Insurance Corporation'),
('Progressive', 'Active', 'Auto insurance specialist'),
('AAA', 'Active', 'Multi-line carrier'),
('State Farm', 'Active', 'Multi-line carrier'),
('Tower Hill', 'Active', 'Florida property specialist'),
('Allstate', 'Active', 'Multi-line carrier'),
('USAA', 'Active', 'Military and family members'),
('Travelers', 'Active', 'Commercial and personal lines'),
('Liberty Mutual', 'Active', 'Multi-line carrier'),
('Nationwide', 'Active', 'Multi-line carrier'),
('Farmers', 'Active', 'Multi-line carrier'),
('American Family', 'Active', 'Multi-line carrier'),
('Hartford', 'Active', 'AARP partner'),
('Chubb', 'Active', 'High-value homes'),
('Mercury', 'Active', 'California-based carrier')
ON CONFLICT (carrier_name) DO NOTHING;

-- 3. Insert common MGAs
INSERT INTO mgas (mga_name, status, notes) VALUES
('Direct Appointment', 'Active', 'Direct carrier appointment - no MGA'),
('SureTec', 'Active', 'Florida MGA'),
('FAIA', 'Active', 'Florida Association of Insurance Agents'),
('Iroquois', 'Active', 'National MGA network'),
('SIAA', 'Active', 'Strategic Insurance Agency Alliance'),
('Smart Choice', 'Active', 'National MGA network')
ON CONFLICT (mga_name) DO NOTHING;

-- 4. Get IDs for creating relationships and rules
DO $$
DECLARE
    demo_email TEXT := 'Demo@AgentCommissionTracker.com';
    citizens_id UUID;
    progressive_id UUID;
    aaa_id UUID;
    statefarm_id UUID;
    towerhill_id UUID;
    direct_mga_id UUID;
    suretec_id UUID;
BEGIN
    -- Get carrier IDs
    SELECT carrier_id INTO citizens_id FROM carriers WHERE carrier_name = 'Citizens';
    SELECT carrier_id INTO progressive_id FROM carriers WHERE carrier_name = 'Progressive';
    SELECT carrier_id INTO aaa_id FROM carriers WHERE carrier_name = 'AAA';
    SELECT carrier_id INTO statefarm_id FROM carriers WHERE carrier_name = 'State Farm';
    SELECT carrier_id INTO towerhill_id FROM carriers WHERE carrier_name = 'Tower Hill';
    
    -- Get MGA IDs
    SELECT mga_id INTO direct_mga_id FROM mgas WHERE mga_name = 'Direct Appointment';
    SELECT mga_id INTO suretec_id FROM mgas WHERE mga_name = 'SureTec';
    
    -- Create carrier-MGA relationships
    INSERT INTO carrier_mga_relationships (carrier_id, mga_id, is_direct) VALUES
    (citizens_id, direct_mga_id, true),
    (progressive_id, direct_mga_id, true),
    (aaa_id, direct_mga_id, true),
    (statefarm_id, suretec_id, false),
    (towerhill_id, direct_mga_id, true)
    ON CONFLICT DO NOTHING;
    
    -- Create commission rules for demo user
    -- Citizens - 10% flat
    INSERT INTO commission_rules (carrier_id, mga_id, new_rate, renewal_rate, payment_terms, rule_description, user_email) 
    VALUES (citizens_id, direct_mga_id, 10.0, 10.0, 'As Earned', 'Citizens standard rate', demo_email);
    
    -- Progressive - 12% auto
    INSERT INTO commission_rules (carrier_id, mga_id, policy_type, new_rate, renewal_rate, payment_terms, rule_description, user_email) 
    VALUES (progressive_id, direct_mga_id, 'Auto', 12.0, 12.0, 'Advanced', 'Progressive auto', demo_email);
    
    -- AAA - varied by product
    INSERT INTO commission_rules (carrier_id, mga_id, policy_type, new_rate, renewal_rate, payment_terms, rule_description, user_email) 
    VALUES 
    (aaa_id, direct_mga_id, 'HO3', 15.0, 12.0, 'As Earned', 'AAA Homeowners', demo_email),
    (aaa_id, direct_mga_id, 'Auto', 12.0, 10.0, 'As Earned', 'AAA Auto', demo_email);
    
    -- State Farm via SureTec
    INSERT INTO commission_rules (carrier_id, mga_id, new_rate, renewal_rate, payment_terms, rule_description, user_email) 
    VALUES (statefarm_id, suretec_id, 14.0, 12.0, 'Advanced', 'State Farm through SureTec', demo_email);
    
    -- Tower Hill
    INSERT INTO commission_rules (carrier_id, mga_id, policy_type, new_rate, renewal_rate, payment_terms, rule_description, user_email) 
    VALUES (towerhill_id, direct_mga_id, 'HO3', 18.0, 15.0, 'As Earned', 'Tower Hill property', demo_email);
    
END $$;

-- 5. Verify the restoration
SELECT 'After Restoration:' as status;

SELECT 'Carriers:' as table_name, COUNT(*) as count FROM carriers
UNION ALL
SELECT 'MGAs:' as table_name, COUNT(*) as count FROM mgas
UNION ALL
SELECT 'Relationships:' as table_name, COUNT(*) as count FROM carrier_mga_relationships
UNION ALL
SELECT 'Demo Rules:' as table_name, COUNT(*) as count FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY table_name;

-- 6. Show sample of demo user's rules
SELECT 
    c.carrier_name,
    m.mga_name,
    cr.policy_type,
    cr.new_rate || '%' as new_rate,
    cr.renewal_rate || '%' as renewal_rate
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.user_email = 'Demo@AgentCommissionTracker.com'
LIMIT 10;