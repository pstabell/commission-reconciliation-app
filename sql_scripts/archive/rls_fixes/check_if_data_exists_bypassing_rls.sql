-- CHECK IF DATA EXISTS (BYPASSING RLS)
-- Run this as database owner in Supabase SQL Editor

-- 1. Create SECURITY DEFINER functions to bypass RLS
CREATE OR REPLACE FUNCTION count_all_carriers()
RETURNS TABLE(total_count bigint)
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT COUNT(*) FROM carriers;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION count_all_mgas()
RETURNS TABLE(total_count bigint)
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT COUNT(*) FROM mgas;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION count_all_commission_rules()
RETURNS TABLE(total_count bigint, by_user jsonb)
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        COUNT(*),
        jsonb_object_agg(COALESCE(user_email, 'null'), cnt)
    FROM (
        SELECT user_email, COUNT(*) as cnt 
        FROM commission_rules 
        GROUP BY user_email
    ) t;
END;
$$ LANGUAGE plpgsql;

-- 2. Run the functions to see ALL data
SELECT 'Checking ALL data (bypassing RLS):' as status;

SELECT 'Total Carriers:' as item, * FROM count_all_carriers();
SELECT 'Total MGAs:' as item, * FROM count_all_mgas();
SELECT 'Total Commission Rules:' as item, total_count, by_user FROM count_all_commission_rules();

-- 3. Check what current user can see normally
SELECT 'What current user sees:' as status;
SELECT 'Carriers visible:' as item, COUNT(*) FROM carriers;
SELECT 'MGAs visible:' as item, COUNT(*) FROM mgas;
SELECT 'Commission rules visible:' as item, COUNT(*) FROM commission_rules;

-- 4. Show sample of any existing carriers (bypassing RLS)
CREATE OR REPLACE FUNCTION show_sample_carriers()
RETURNS TABLE(carrier_name text, status text, created_at timestamptz)
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY 
    SELECT c.carrier_name, c.status, c.created_at 
    FROM carriers c 
    ORDER BY c.created_at DESC 
    LIMIT 10;
END;
$$ LANGUAGE plpgsql;

SELECT 'Sample carriers (if any exist):' as status;
SELECT * FROM show_sample_carriers();

-- 5. Clean up functions
DROP FUNCTION IF EXISTS count_all_carriers();
DROP FUNCTION IF EXISTS count_all_mgas();
DROP FUNCTION IF EXISTS count_all_commission_rules();
DROP FUNCTION IF EXISTS show_sample_carriers();