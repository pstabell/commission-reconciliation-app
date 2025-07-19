-- Check actual date values and formats
SELECT 
    _id,
    "Customer",
    "Policy Number",
    "Effective Date",
    "Policy Origination Date",
    "X-DATE",
    LENGTH("Effective Date") as eff_date_length,
    LENGTH("Policy Origination Date") as orig_date_length,
    LENGTH("X-DATE") as x_date_length
FROM policies
WHERE 
    "Effective Date" IS NOT NULL 
    OR "Policy Origination Date" IS NOT NULL 
    OR "X-DATE" IS NOT NULL
ORDER BY _id DESC
LIMIT 30;

-- Check for different date patterns
SELECT 
    COUNT(*) as total_records,
    COUNT("Effective Date") as has_effective_date,
    COUNT("Policy Origination Date") as has_origination_date,
    COUNT("X-DATE") as has_x_date,
    -- Check for YYYY-MM-DD format
    COUNT(*) FILTER (WHERE "Effective Date" ~ '^\d{4}-\d{2}-\d{2}$') as eff_date_yyyy_mm_dd,
    COUNT(*) FILTER (WHERE "Policy Origination Date" ~ '^\d{4}-\d{2}-\d{2}$') as orig_date_yyyy_mm_dd,
    COUNT(*) FILTER (WHERE "X-DATE" ~ '^\d{4}-\d{2}-\d{2}$') as x_date_yyyy_mm_dd,
    -- Check for DD/MM/YYYY format
    COUNT(*) FILTER (WHERE "Effective Date" ~ '^\d{2}/\d{2}/\d{4}$') as eff_date_dd_mm_yyyy,
    COUNT(*) FILTER (WHERE "Policy Origination Date" ~ '^\d{2}/\d{2}/\d{4}$') as orig_date_dd_mm_yyyy,
    COUNT(*) FILTER (WHERE "X-DATE" ~ '^\d{2}/\d{2}/\d{4}$') as x_date_dd_mm_yyyy
FROM policies;

-- Look for Ashley Doctors records specifically
SELECT 
    _id,
    "Customer",
    "Policy Number",
    "Effective Date",
    "Policy Origination Date",
    "X-DATE"
FROM policies
WHERE "Customer" LIKE '%Ashley Doctors%'
ORDER BY _id DESC
LIMIT 10;