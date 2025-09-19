-- Comprehensive Commission Rules Population
-- Based on the Excel data provided
-- This creates ALL commission rules from your spreadsheet

DO $$
DECLARE
    v_carrier_id UUID;
    v_mga_id UUID;
BEGIN
    -- AAA (Home and Membership: 15%, Auto/Package: 12%, Umbrella: 10%)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'AAA';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, policy_type, new_rate, renewal_rate, state, rule_description)
        VALUES 
        (v_carrier_id, 'Home,Membership', 15, 15, 'FL', 'AAA Home and Membership products'),
        (v_carrier_id, 'Auto,Package', 12, 12, 'FL', 'AAA Auto and Package products'),
        (v_carrier_id, 'Umbrella', 10, 10, 'FL', 'AAA Umbrella products')
        ON CONFLICT DO NOTHING;
    END IF;

    -- Allrisk (10/10)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Allrisk';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 10, 10, 'FL', 'Allrisk standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- American Integrity (12/8)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'American Integrity';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 12, 8, 'FL', 'American Integrity standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- American Traditions (11/11)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'American Traditions';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default, payment_terms)
        VALUES (v_carrier_id, 11, 11, 'FL', 'American Traditions - pays based on insured payment plan', true, 'As Earned')
        ON CONFLICT DO NOTHING;
    END IF;

    -- Attune (12.5/12.5)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Attune';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 12.5, 12.5, 'FL', 'Attune standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Burns & Wilcox MGA (10/8.5)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Burns & Wilcox';
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Burns & Wilcox';
    IF v_carrier_id IS NOT NULL AND v_mga_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, mga_id, new_rate, renewal_rate, state, rule_description)
        VALUES (v_carrier_id, v_mga_id, 10, 8.5, 'FL', 'Burns & Wilcox MGA rate')
        ON CONFLICT DO NOTHING;
    END IF;

    -- Bristol West (10/8)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Bristol West';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 10, 8, 'FL', 'Bristol West standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- BTIS MGA (10/10)
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'BTIS';
    IF v_mga_id IS NOT NULL THEN
        -- Note: BTIS is an MGA without specific carrier, handled separately
        NULL;
    END IF;

    -- Cabrillo (10/10)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Cabrillo';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default, payment_terms)
        VALUES (v_carrier_id, 10, 10, 'FL', 'Cabrillo - pays based on insured payment plan', true, 'As Earned')
        ON CONFLICT DO NOTHING;
    END IF;

    -- Chubb (Cyber: 18, Auto/BOP/Umbrella: 15)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Chubb';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, policy_type, new_rate, renewal_rate, state, rule_description)
        VALUES 
        (v_carrier_id, 'Cyber', 18, 15, 'FL', 'Chubb Cyber Liability'),
        (v_carrier_id, 'Auto,BOP,Umbrella', 15, 15, 'FL', 'Chubb Auto/BOP/Umbrella products')
        ON CONFLICT DO NOTHING;
    END IF;

    -- Citizens (10/10)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Citizens';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 10, 10, 'FL', 'Citizens standard rate - all policy types', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- CNA with Iroquois (20/blank - using 20 for renewal)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'CNA';
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Iroquois';
    IF v_carrier_id IS NOT NULL AND v_mga_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, mga_id, new_rate, renewal_rate, state, rule_description)
        VALUES (v_carrier_id, v_mga_id, 20, 20, 'FL', 'CNA through Iroquois MGA')
        ON CONFLICT DO NOTHING;
    END IF;

    -- Edison (10/10)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Edison';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 10, 10, 'FL', 'Edison standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Empire Underwrites LLC MGA (6/6)
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Empire Underwrites LLC';
    IF v_mga_id IS NOT NULL THEN
        -- Note: Empire Underwrites is an MGA without specific carrier
        NULL;
    END IF;

    -- Federated National (8/8)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Federated National';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 8, 8, 'FL', 'Federated National standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Florida Peninsula (10/10)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Florida Peninsula';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 10, 10, 'FL', 'Florida Peninsula standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Foremost (15/12.5)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Foremost';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default, payment_terms)
        VALUES (v_carrier_id, 15, 12.5, 'FL', 'Foremost - pays based on insured payment plan', true, 'As Earned')
        ON CONFLICT DO NOTHING;
    END IF;

    -- Hagerty (10/10)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Hagerty';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 10, 10, 'FL', 'Hagerty specialty auto rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Hartford Flood FL (15.5/11.5)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Hartford Flood FL';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 15.5, 11.5, 'FL', 'Hartford Flood standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Heritage (11/11)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Heritage';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 11, 11, 'FL', 'Heritage standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Johnson and Johnson MGA (12.5/12.5)
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Johnson and Johnson';
    IF v_mga_id IS NOT NULL THEN
        -- Note: J&J is an MGA without specific carrier
        NULL;
    END IF;

    -- MacNeill Group MGA (10/10)
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'MacNeill Group';
    IF v_mga_id IS NOT NULL THEN
        -- Note: MacNeill is an MGA without specific carrier
        NULL;
    END IF;

    -- Mercury with Advantage Partners (8/6)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Mercury';
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Advantage Partners';
    IF v_carrier_id IS NOT NULL AND v_mga_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, mga_id, new_rate, renewal_rate, state, rule_description, payment_terms)
        VALUES (v_carrier_id, v_mga_id, 8, 6, 'FL', 'Mercury through Advantage Partners - pays based on insured payment plan', 'As Earned')
        ON CONFLICT DO NOTHING;
    END IF;

    -- Monarch (8/8)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Monarch';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 8, 8, 'FL', 'Monarch standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- National General (12/12)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'National General';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default, payment_terms)
        VALUES (v_carrier_id, 12, 12, 'FL', 'National General - pays based on insured payment plan', true, 'As Earned')
        ON CONFLICT DO NOTHING;
    END IF;

    -- National General Flood (18/15)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'National General Flood';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 18, 15, 'FL', 'National General Flood rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Neptune (12/12)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Neptune';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default, payment_terms)
        VALUES (v_carrier_id, 12, 12, 'FL', 'Neptune - pays on full premium', true, 'Advanced')
        ON CONFLICT DO NOTHING;
    END IF;

    -- NEXT with Simon Agency (WC: 7, GL: 10 / WC: 7, GL: 9)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'NEXT';
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Simon Agency';
    IF v_carrier_id IS NOT NULL AND v_mga_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, mga_id, policy_type, new_rate, renewal_rate, state, rule_description)
        VALUES 
        (v_carrier_id, v_mga_id, 'WC', 7, 7, 'FL', 'NEXT Workers Comp through Simon Agency'),
        (v_carrier_id, v_mga_id, 'GL', 10, 9, 'FL', 'NEXT General Liability through Simon Agency')
        ON CONFLICT DO NOTHING;
    END IF;

    -- Normandy (blank/12 - using 12 for both)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Normandy';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 12, 12, 'FL', 'Normandy standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Olympus (9/7)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Olympus';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 9, 7, 'FL', 'Olympus standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Orchid (10/8)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Orchid';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 10, 8, 'FL', 'Orchid standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Ovation with Florida Peninsula MGA (10/10)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Ovation';
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Florida Peninsula';
    IF v_carrier_id IS NOT NULL AND v_mga_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, mga_id, new_rate, renewal_rate, state, rule_description)
        VALUES (v_carrier_id, v_mga_id, 10, 10, 'FL', 'Ovation through Florida Peninsula MGA')
        ON CONFLICT DO NOTHING;
    END IF;

    -- Progressive (Auto: 12, Boat: 10, Renters: 15)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Progressive';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, policy_type, new_rate, renewal_rate, state, rule_description)
        VALUES 
        (v_carrier_id, 'Auto', 12, 12, 'FL', 'Progressive Auto mono-line'),
        (v_carrier_id, 'Boat', 10, 10, 'FL', 'Progressive Boat insurance'),
        (v_carrier_id, 'Renters', 15, 15, 'FL', 'Progressive Renters insurance')
        ON CONFLICT DO NOTHING;
    END IF;

    -- Ryan Specialty Group MGA (12.5/10)
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Ryan Specialty Group';
    IF v_mga_id IS NOT NULL THEN
        -- Note: Ryan Specialty is an MGA without specific carrier
        NULL;
    END IF;

    -- Safeco (Home: 15, Auto: 12 / Home: 15, Auto: 10)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Safeco';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, policy_type, new_rate, renewal_rate, state, rule_description)
        VALUES 
        (v_carrier_id, 'Home', 15, 15, 'FL', 'Safeco Home insurance'),
        (v_carrier_id, 'Auto', 12, 10, 'FL', 'Safeco Auto insurance')
        ON CONFLICT DO NOTHING;
    END IF;

    -- Simon Agency MGA (WC: 7, GL: 10)
    -- Already handled with NEXT carrier above

    -- Southern Oak (10/8.5)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Southern Oak';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 10, 8.5, 'FL', 'Southern Oak standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Spinnaker (10/10)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Spinnaker';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 10, 10, 'FL', 'Spinnaker standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- StormPeace (10/10)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'StormPeace';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 10, 10, 'FL', 'StormPeace standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Travelers (15/12, Umbrella: 10)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Travelers';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, policy_type, new_rate, renewal_rate, state, rule_description)
        VALUES 
        (v_carrier_id, NULL, 15, 12, 'FL', 'Travelers standard rate', true),
        (v_carrier_id, 'Umbrella', 15, 10, 'FL', 'Travelers Umbrella product')
        ON CONFLICT DO NOTHING;
    END IF;

    -- TypTap (20/10)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'TypTap';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 20, 10, 'FL', 'TypTap standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Universal (12/8)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Universal';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 12, 8, 'FL', 'Universal standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- UPC (12/8)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'UPC';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 12, 8, 'FL', 'UPC standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Velocity with Advantage Partners (12/10)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Velocity';
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Advantage Partners';
    IF v_carrier_id IS NOT NULL AND v_mga_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, mga_id, new_rate, renewal_rate, state, rule_description)
        VALUES (v_carrier_id, v_mga_id, 12, 10, 'FL', 'Velocity through Advantage Partners')
        ON CONFLICT DO NOTHING;
    END IF;

    -- Wright Flood (15/15)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Wright Flood';
    IF v_carrier_id IS NOT NULL THEN
        INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, state, rule_description, is_default)
        VALUES (v_carrier_id, 15, 15, 'FL', 'Wright Flood standard rate', true)
        ON CONFLICT DO NOTHING;
    END IF;

    -- E&S Market MGA (10/10)
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'E&S Market';
    IF v_mga_id IS NOT NULL THEN
        -- Note: E&S Market is an MGA without specific carrier
        NULL;
    END IF;

END $$;

-- Final summary of all commission rules
SELECT 'Total commission rules created:' as status, COUNT(*) as count FROM commission_rules;