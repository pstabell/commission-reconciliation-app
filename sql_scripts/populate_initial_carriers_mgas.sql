-- Initial Carrier and MGA Population Script
-- Based on Excel data provided
-- Run this after creating the commission structure tables

-- Insert Carriers (alphabetical order)
INSERT INTO carriers (carrier_name, status, notes) VALUES
('AAA', 'Active', 'Direct appointment'),
('Allrisk', 'Active', 'Direct appointment'),
('American Integrity', 'Active', 'Direct appointment'),
('American Traditions', 'Active', 'Direct appointment'),
('Attune', 'Active', 'Direct appointment'),
('Bristol West', 'Active', 'Direct appointment'),
('Cabrillo', 'Active', 'Direct appointment'),
('Chubb', 'Active', 'Direct appointment'),
('Citizens', 'Active', 'Citizens Property Insurance Corporation - Direct'),
('CNA', 'Active', 'Works with Iroquois MGA'),
('Edison', 'Active', 'Direct appointment'),
('Federated National', 'Active', 'Direct appointment'),
('Florida Peninsula', 'Active', 'Direct appointment'),
('Foremost', 'Active', 'Direct appointment'),
('Hagerty', 'Active', 'Specialty auto insurance'),
('Hartford Flood FL', 'Active', 'Flood insurance specialist'),
('Heritage', 'Active', 'Direct appointment'),
('Mercury', 'Active', 'Works with Advantage Partners'),
('Monarch', 'Active', 'Direct appointment'),
('National General', 'Active', 'Direct appointment'),
('National General Flood', 'Active', 'Flood insurance'),
('Neptune', 'Active', 'Direct appointment'),
('NEXT', 'Active', 'Works with Simon Agency'),
('Normandy', 'Active', 'Direct appointment'),
('Olympus', 'Active', 'Direct appointment'),
('Orchid', 'Active', 'Direct appointment'),
('Ovation', 'Active', 'Works with Florida Peninsula MGA'),
('Progressive', 'Active', 'Auto insurance - mono-line in FL'),
('Safeco', 'Active', 'Direct appointment'),
('Southern Oak', 'Active', 'Direct appointment'),
('Spinnaker', 'Active', 'Direct appointment'),
('StormPeace', 'Active', 'Direct appointment'),
('Travelers', 'Active', 'Direct appointment'),
('TypTap', 'Active', 'Direct appointment'),
('Universal', 'Active', 'Direct appointment'),
('UPC', 'Active', 'Direct appointment'),
('Velocity', 'Active', 'Works with Advantage Partners'),
('Wright Flood', 'Active', 'Flood insurance specialist')
ON CONFLICT (carrier_name) DO NOTHING;

-- Insert MGAs
INSERT INTO mgas (mga_name, status, notes) VALUES
('Advantage Partners', 'Active', 'Works with Mercury and Velocity'),
('BTIS', 'Active', NULL),
('Burns & Wilcox', 'Active', NULL),
('E&S Market', 'Active', 'Excess and Surplus lines'),
('Empire Underwrites LLC', 'Active', NULL),
('Florida Peninsula', 'Active', 'MGA for Ovation'),
('Iroquois', 'Active', 'Works with CNA'),
('Johnson and Johnson', 'Active', NULL),
('MacNeill Group', 'Active', NULL),
('Ryan Specialty Group', 'Active', NULL),
('Simon Agency', 'Active', 'Works with NEXT and Safeco')
ON CONFLICT (mga_name) DO NOTHING;

-- Create carrier-MGA relationships
DO $$
DECLARE
    v_mercury_id UUID;
    v_velocity_id UUID;
    v_cna_id UUID;
    v_next_id UUID;
    v_safeco_id UUID;
    v_ovation_id UUID;
    v_advantage_id UUID;
    v_iroquois_id UUID;
    v_simon_id UUID;
    v_florida_pen_id UUID;
BEGIN
    -- Get carrier IDs
    SELECT carrier_id INTO v_mercury_id FROM carriers WHERE carrier_name = 'Mercury';
    SELECT carrier_id INTO v_velocity_id FROM carriers WHERE carrier_name = 'Velocity';
    SELECT carrier_id INTO v_cna_id FROM carriers WHERE carrier_name = 'CNA';
    SELECT carrier_id INTO v_next_id FROM carriers WHERE carrier_name = 'NEXT';
    SELECT carrier_id INTO v_safeco_id FROM carriers WHERE carrier_name = 'Safeco';
    SELECT carrier_id INTO v_ovation_id FROM carriers WHERE carrier_name = 'Ovation';
    
    -- Get MGA IDs
    SELECT mga_id INTO v_advantage_id FROM mgas WHERE mga_name = 'Advantage Partners';
    SELECT mga_id INTO v_iroquois_id FROM mgas WHERE mga_name = 'Iroquois';
    SELECT mga_id INTO v_simon_id FROM mgas WHERE mga_name = 'Simon Agency';
    SELECT mga_id INTO v_florida_pen_id FROM mgas WHERE mga_name = 'Florida Peninsula';
    
    -- Insert relationships
    IF v_mercury_id IS NOT NULL AND v_advantage_id IS NOT NULL THEN
        INSERT INTO carrier_mga_relationships (carrier_id, mga_id) 
        VALUES (v_mercury_id, v_advantage_id)
        ON CONFLICT DO NOTHING;
    END IF;
    
    IF v_velocity_id IS NOT NULL AND v_advantage_id IS NOT NULL THEN
        INSERT INTO carrier_mga_relationships (carrier_id, mga_id) 
        VALUES (v_velocity_id, v_advantage_id)
        ON CONFLICT DO NOTHING;
    END IF;
    
    IF v_cna_id IS NOT NULL AND v_iroquois_id IS NOT NULL THEN
        INSERT INTO carrier_mga_relationships (carrier_id, mga_id) 
        VALUES (v_cna_id, v_iroquois_id)
        ON CONFLICT DO NOTHING;
    END IF;
    
    IF v_next_id IS NOT NULL AND v_simon_id IS NOT NULL THEN
        INSERT INTO carrier_mga_relationships (carrier_id, mga_id) 
        VALUES (v_next_id, v_simon_id)
        ON CONFLICT DO NOTHING;
    END IF;
    
    IF v_safeco_id IS NOT NULL AND v_simon_id IS NOT NULL THEN
        INSERT INTO carrier_mga_relationships (carrier_id, mga_id) 
        VALUES (v_safeco_id, v_simon_id)
        ON CONFLICT DO NOTHING;
    END IF;
    
    IF v_ovation_id IS NOT NULL AND v_florida_pen_id IS NOT NULL THEN
        INSERT INTO carrier_mga_relationships (carrier_id, mga_id) 
        VALUES (v_ovation_id, v_florida_pen_id)
        ON CONFLICT DO NOTHING;
    END IF;
END $$;

-- Insert some sample commission rules based on Excel data
DO $$
DECLARE
    v_aaa_id UUID;
    v_citizens_id UUID;
    v_progressive_id UUID;
BEGIN
    -- Get carrier IDs
    SELECT carrier_id INTO v_aaa_id FROM carriers WHERE carrier_name = 'AAA';
    SELECT carrier_id INTO v_citizens_id FROM carriers WHERE carrier_name = 'Citizens';
    SELECT carrier_id INTO v_progressive_id FROM carriers WHERE carrier_name = 'Progressive';
    
    -- AAA rules (Home/Membership: 15%, Auto/Package: 12%, Umbrella: 10%)
    IF v_aaa_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, policy_type, new_rate, renewal_rate, state, rule_description)
        VALUES 
        (v_aaa_id, 'Home,Membership', 15, 15, 'FL', 'AAA Home and Membership products'),
        (v_aaa_id, 'Auto,Package', 12, 12, 'FL', 'AAA Auto and Package products'),
        (v_aaa_id, 'Umbrella', 10, 10, 'FL', 'AAA Umbrella products')
        ON CONFLICT DO NOTHING;
    END IF;
    
    -- Citizens rule (10% for all)
    IF v_citizens_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES 
        (v_citizens_id, 10, 10, 'FL', 'Citizens standard rate - all policy types', true)
        ON CONFLICT DO NOTHING;
    END IF;
    
    -- Progressive rules (Auto: 12%, Boat: 10%, Renters: 15%)
    IF v_progressive_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, policy_type, new_rate, renewal_rate, state, rule_description)
        VALUES 
        (v_progressive_id, 'Auto', 12, 12, 'FL', 'Progressive Auto mono-line'),
        (v_progressive_id, 'Boat', 10, 10, 'FL', 'Progressive Boat insurance'),
        (v_progressive_id, 'Renters', 15, 15, 'FL', 'Progressive Renters insurance')
        ON CONFLICT DO NOTHING;
    END IF;
END $$;

-- Summary
SELECT 'Carriers loaded:' as status, COUNT(*) as count FROM carriers
UNION ALL
SELECT 'MGAs loaded:', COUNT(*) FROM mgas
UNION ALL
SELECT 'Relationships created:', COUNT(*) FROM carrier_mga_relationships
UNION ALL
SELECT 'Commission rules created:', COUNT(*) FROM commission_rules;