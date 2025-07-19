-- SQL script to convert dates from MM/DD/YYYY to YYYY-MM-DD format
-- Run this in your Supabase SQL Editor

-- First, let's check some sample data
SELECT 
    _id,
    "Effective Date",
    "Policy Origination Date",
    "X-DATE",
    "STMT DATE"
FROM policies
LIMIT 10;

-- Update Effective Date
UPDATE policies
SET "Effective Date" = 
    CASE 
        WHEN "Effective Date" ~ '^\d{2}/\d{2}/\d{4}$' THEN
            CONCAT(
                SUBSTRING("Effective Date", 7, 4), '-',
                SUBSTRING("Effective Date", 1, 2), '-',
                SUBSTRING("Effective Date", 4, 2)
            )
        ELSE "Effective Date"
    END
WHERE "Effective Date" ~ '^\d{2}/\d{2}/\d{4}$';

-- Update Policy Origination Date
UPDATE policies
SET "Policy Origination Date" = 
    CASE 
        WHEN "Policy Origination Date" ~ '^\d{2}/\d{2}/\d{4}$' THEN
            CONCAT(
                SUBSTRING("Policy Origination Date", 7, 4), '-',
                SUBSTRING("Policy Origination Date", 1, 2), '-',
                SUBSTRING("Policy Origination Date", 4, 2)
            )
        ELSE "Policy Origination Date"
    END
WHERE "Policy Origination Date" ~ '^\d{2}/\d{2}/\d{4}$';

-- Update X-DATE (Policy Expiration Date)
UPDATE policies
SET "X-DATE" = 
    CASE 
        WHEN "X-DATE" ~ '^\d{2}/\d{2}/\d{4}$' THEN
            CONCAT(
                SUBSTRING("X-DATE", 7, 4), '-',
                SUBSTRING("X-DATE", 1, 2), '-',
                SUBSTRING("X-DATE", 4, 2)
            )
        ELSE "X-DATE"
    END
WHERE "X-DATE" ~ '^\d{2}/\d{2}/\d{4}$';

-- Update STMT DATE
UPDATE policies
SET "STMT DATE" = 
    CASE 
        WHEN "STMT DATE" ~ '^\d{2}/\d{2}/\d{4}$' THEN
            CONCAT(
                SUBSTRING("STMT DATE", 7, 4), '-',
                SUBSTRING("STMT DATE", 1, 2), '-',
                SUBSTRING("STMT DATE", 4, 2)
            )
        ELSE "STMT DATE"
    END
WHERE "STMT DATE" ~ '^\d{2}/\d{2}/\d{4}$';

-- Verify the results
SELECT 
    _id,
    "Effective Date",
    "Policy Origination Date",
    "X-DATE",
    "STMT DATE"
FROM policies
LIMIT 10;