-- SQL script to convert dates from MM/DD/YYYY to YYYY-MM-DD format
-- Run this in your Supabase SQL Editor

-- First, let's check some sample data
SELECT 
    _id,
    "Effective Date",
    "Transaction Date",
    "Policy Origination Date"
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

-- Update Transaction Date
UPDATE policies
SET "Transaction Date" = 
    CASE 
        WHEN "Transaction Date" ~ '^\d{2}/\d{2}/\d{4}$' THEN
            CONCAT(
                SUBSTRING("Transaction Date", 7, 4), '-',
                SUBSTRING("Transaction Date", 1, 2), '-',
                SUBSTRING("Transaction Date", 4, 2)
            )
        ELSE "Transaction Date"
    END
WHERE "Transaction Date" ~ '^\d{2}/\d{2}/\d{4}$';

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

-- Update Commission Received Date
UPDATE policies
SET "Commission Received Date" = 
    CASE 
        WHEN "Commission Received Date" ~ '^\d{2}/\d{2}/\d{4}$' THEN
            CONCAT(
                SUBSTRING("Commission Received Date", 7, 4), '-',
                SUBSTRING("Commission Received Date", 1, 2), '-',
                SUBSTRING("Commission Received Date", 4, 2)
            )
        ELSE "Commission Received Date"
    END
WHERE "Commission Received Date" ~ '^\d{2}/\d{2}/\d{4}$';

-- Update Agent Paid Date
UPDATE policies
SET "Agent Paid Date" = 
    CASE 
        WHEN "Agent Paid Date" ~ '^\d{2}/\d{2}/\d{4}$' THEN
            CONCAT(
                SUBSTRING("Agent Paid Date", 7, 4), '-',
                SUBSTRING("Agent Paid Date", 1, 2), '-',
                SUBSTRING("Agent Paid Date", 4, 2)
            )
        ELSE "Agent Paid Date"
    END
WHERE "Agent Paid Date" ~ '^\d{2}/\d{2}/\d{4}$';

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
    "Transaction Date",
    "Policy Origination Date"
FROM policies
LIMIT 10;