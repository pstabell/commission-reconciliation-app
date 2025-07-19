-- Find records that have dates to check the format
SELECT 
    _id,
    "Customer",
    "Effective Date",
    "Policy Origination Date",
    "X-DATE",
    "STMT DATE"
FROM policies
WHERE 
    "Effective Date" IS NOT NULL 
    OR "Policy Origination Date" IS NOT NULL 
    OR "X-DATE" IS NOT NULL
    OR "STMT DATE" IS NOT NULL
LIMIT 20;

-- Count how many records have dates in MM/DD/YYYY format
SELECT 
    COUNT(*) FILTER (WHERE "Effective Date" ~ '^\d{2}/\d{2}/\d{4}$') as effective_date_count,
    COUNT(*) FILTER (WHERE "Policy Origination Date" ~ '^\d{2}/\d{2}/\d{4}$') as origination_date_count,
    COUNT(*) FILTER (WHERE "X-DATE" ~ '^\d{2}/\d{2}/\d{4}$') as x_date_count,
    COUNT(*) FILTER (WHERE "STMT DATE" ~ '^\d{2}/\d{2}/\d{4}$') as stmt_date_count
FROM policies;