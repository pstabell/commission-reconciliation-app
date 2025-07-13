-- Populate carrier-MGA relationships based on Excel data
-- This creates the relationships between carriers and MGAs
-- Run this after creating carriers and MGAs

DO $$
DECLARE
    v_carrier_id UUID;
    v_mga_id UUID;
BEGIN
    -- Mercury with Advantage Partners
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Mercury';
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Advantage Partners';
    IF v_carrier_id IS NOT NULL AND v_mga_id IS NOT NULL THEN
        INSERT INTO carrier_mga_relationships (carrier_id, mga_id, is_direct)
        VALUES (v_carrier_id, v_mga_id, false)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Velocity with Advantage Partners
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Velocity';
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Advantage Partners';
    IF v_carrier_id IS NOT NULL AND v_mga_id IS NOT NULL THEN
        INSERT INTO carrier_mga_relationships (carrier_id, mga_id, is_direct)
        VALUES (v_carrier_id, v_mga_id, false)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Burns & Wilcox (carrier) with Burns & Wilcox (MGA)
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Burns & Wilcox';
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Burns & Wilcox';
    IF v_carrier_id IS NOT NULL AND v_mga_id IS NOT NULL THEN
        INSERT INTO carrier_mga_relationships (carrier_id, mga_id, is_direct)
        VALUES (v_carrier_id, v_mga_id, false)
        ON CONFLICT DO NOTHING;
    END IF;

    -- CNA with Iroquois
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'CNA';
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Iroquois';
    IF v_carrier_id IS NOT NULL AND v_mga_id IS NOT NULL THEN
        INSERT INTO carrier_mga_relationships (carrier_id, mga_id, is_direct)
        VALUES (v_carrier_id, v_mga_id, false)
        ON CONFLICT DO NOTHING;
    END IF;

    -- NEXT with Simon Agency
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'NEXT';
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Simon Agency';
    IF v_carrier_id IS NOT NULL AND v_mga_id IS NOT NULL THEN
        INSERT INTO carrier_mga_relationships (carrier_id, mga_id, is_direct)
        VALUES (v_carrier_id, v_mga_id, false)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Ovation with Florida Peninsula
    SELECT carrier_id INTO v_carrier_id FROM carriers WHERE carrier_name = 'Ovation';
    SELECT mga_id INTO v_mga_id FROM mgas WHERE mga_name = 'Florida Peninsula';
    IF v_carrier_id IS NOT NULL AND v_mga_id IS NOT NULL THEN
        INSERT INTO carrier_mga_relationships (carrier_id, mga_id, is_direct)
        VALUES (v_carrier_id, v_mga_id, false)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Add direct appointment relationships for carriers that don't use MGAs
    -- (These are carriers that appear in the Excel without an MGA)
    FOR v_carrier_id IN 
        SELECT carrier_id FROM carriers 
        WHERE carrier_name IN (
            'AAA', 'Allrisk', 'American Integrity', 'American Traditions', 'Attune',
            'Bristol West', 'Cabrillo', 'Chubb', 'Citizens', 'Edison', 'Federated National',
            'Florida Peninsula', 'Foremost', 'Hagerty', 'Hartford Flood FL', 'Heritage',
            'Monarch', 'National General', 'National General Flood', 'Neptune', 'Normandy',
            'Olympus', 'Orchid', 'Progressive', 'Safeco', 'Southern Oak', 'Spinnaker',
            'StormPeace', 'Travelers', 'TypTap', 'Universal', 'UPC', 'Wright Flood'
        )
    LOOP
        -- Mark these as direct appointments (no MGA)
        INSERT INTO carrier_mga_relationships (carrier_id, mga_id, is_direct)
        VALUES (v_carrier_id, NULL, true)
        ON CONFLICT DO NOTHING;
    END LOOP;

END $$;

-- Show summary of relationships created
SELECT 
    c.carrier_name,
    COALESCE(m.mga_name, 'Direct Appointment') as mga_relationship,
    cmr.is_direct
FROM carrier_mga_relationships cmr
LEFT JOIN carriers c ON cmr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cmr.mga_id = m.mga_id
ORDER BY c.carrier_name;

-- Count of relationships
SELECT 
    'Total carrier-MGA relationships:' as description,
    COUNT(*) as count
FROM carrier_mga_relationships;