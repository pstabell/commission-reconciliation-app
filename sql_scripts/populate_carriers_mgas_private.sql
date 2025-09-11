-- =====================================================
-- POPULATE CARRIERS AND MGAs FOR PRIVATE DATABASE
-- This script bypasses RLS using security definer functions
-- =====================================================

-- First, let's check the RLS policies to understand what's blocking us
SELECT 
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual
FROM pg_policies
WHERE tablename IN ('carriers', 'mgas')
ORDER BY tablename, policyname;

-- Option 1: If you have admin access, temporarily disable RLS to insert data
-- IMPORTANT: Only do this if you're the database owner
/*
-- Disable RLS temporarily
ALTER TABLE carriers DISABLE ROW LEVEL SECURITY;
ALTER TABLE mgas DISABLE ROW LEVEL SECURITY;
ALTER TABLE carrier_mga_relationships DISABLE ROW LEVEL SECURITY;
ALTER TABLE commission_rules DISABLE ROW LEVEL SECURITY;
*/

-- Option 2: Insert the data (this will work if RLS is disabled or if you have the right permissions)

-- Insert Carriers
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

-- Re-enable RLS if you disabled it
/*
ALTER TABLE carriers ENABLE ROW LEVEL SECURITY;
ALTER TABLE mgas ENABLE ROW LEVEL SECURITY;
ALTER TABLE carrier_mga_relationships ENABLE ROW LEVEL SECURITY;
ALTER TABLE commission_rules ENABLE ROW LEVEL SECURITY;
*/

-- Verify the data was inserted
SELECT 
    'Carriers inserted' as status, 
    COUNT(*) as count 
FROM carriers
UNION ALL
SELECT 
    'MGAs inserted' as status, 
    COUNT(*) as count 
FROM mgas;

-- =====================================================
-- ALTERNATIVE: Create Security Definer Functions
-- Use this if you can't disable RLS
-- =====================================================

-- Create a function to insert carriers that bypasses RLS
CREATE OR REPLACE FUNCTION insert_default_carriers()
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    INSERT INTO carriers (carrier_name, status, notes) VALUES
    ('AAA', 'Active', 'Direct appointment'),
    ('Allrisk', 'Active', 'Direct appointment'),
    ('American Integrity', 'Active', 'Direct appointment'),
    ('American Traditions', 'Active', 'Direct appointment'),
    ('Citizens', 'Active', 'Citizens Property Insurance Corporation'),
    ('Progressive', 'Active', 'Auto insurance - mono-line in FL'),
    ('State Farm', 'Active', 'Direct appointment'),
    ('Mercury', 'Active', 'Works with Advantage Partners')
    ON CONFLICT (carrier_name) DO NOTHING;
END;
$$;

-- Create a function to insert MGAs that bypasses RLS
CREATE OR REPLACE FUNCTION insert_default_mgas()
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    INSERT INTO mgas (mga_name, status, notes) VALUES
    ('Advantage Partners', 'Active', 'Works with Mercury and Velocity'),
    ('Iroquois', 'Active', 'Works with CNA'),
    ('Simon Agency', 'Active', 'Works with NEXT and Safeco')
    ON CONFLICT (mga_name) DO NOTHING;
END;
$$;

-- Call the functions to insert data
-- SELECT insert_default_carriers();
-- SELECT insert_default_mgas();