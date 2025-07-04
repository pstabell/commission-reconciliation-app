-- Migration helper SQL for importing SQLite data to PostgreSQL
-- Run this AFTER creating the schema and importing the data

-- Update foreign key relationships based on matching policy numbers
UPDATE commission_payments cp
SET policy_id = p.id
FROM policies p
WHERE cp.policy_number = p."Policy Number";

-- Update renewal history foreign keys based on transaction IDs
UPDATE renewal_history rh
SET original_policy_id = p1.id,
    new_policy_id = p2.id
FROM policies p1, policies p2
WHERE rh.original_transaction_id = p1."Transaction ID"
AND rh.new_transaction_id = p2."Transaction ID";

-- Clean up currency fields (convert text currency to decimal)
-- This updates the "Paid Amount" field to be numeric
ALTER TABLE policies ADD COLUMN IF NOT EXISTS "Paid Amount Numeric" DECIMAL(10,2);

UPDATE policies 
SET "Paid Amount Numeric" = clean_currency("Paid Amount")
WHERE "Paid Amount" IS NOT NULL;

-- Clean up date fields (convert MM/DD/YYYY to proper dates)
ALTER TABLE policies 
    ADD COLUMN IF NOT EXISTS "Effective Date Parsed" DATE,
    ADD COLUMN IF NOT EXISTS "X-DATE Parsed" DATE,
    ADD COLUMN IF NOT EXISTS "STMT DATE Parsed" DATE,
    ADD COLUMN IF NOT EXISTS "Policy Origination Date Parsed" DATE;

UPDATE policies 
SET 
    "Effective Date Parsed" = TO_DATE("Effective Date", 'MM/DD/YYYY'),
    "X-DATE Parsed" = TO_DATE("X-DATE", 'MM/DD/YYYY'),
    "STMT DATE Parsed" = TO_DATE("STMT DATE", 'MM/DD/YYYY'),
    "Policy Origination Date Parsed" = TO_DATE("Policy Origination Date", 'MM/DD/YYYY')
WHERE 
    "Effective Date" ~ '^\d{2}/\d{2}/\d{4}$' OR
    "X-DATE" ~ '^\d{2}/\d{2}/\d{4}$' OR
    "STMT DATE" ~ '^\d{2}/\d{2}/\d{4}$' OR
    "Policy Origination Date" ~ '^\d{2}/\d{2}/\d{4}$';

-- Update manual_commission_entries dates
ALTER TABLE manual_commission_entries
    ADD COLUMN IF NOT EXISTS effective_date_parsed DATE,
    ADD COLUMN IF NOT EXISTS statement_date_parsed DATE;

UPDATE manual_commission_entries
SET 
    effective_date_parsed = TO_DATE(effective_date, 'MM/DD/YYYY'),
    statement_date_parsed = TO_DATE(statement_date, 'MM/DD/YYYY')
WHERE 
    effective_date ~ '^\d{2}/\d{2}/\d{4}$' OR
    statement_date ~ '^\d{2}/\d{2}/\d{4}$';

-- Create a normalized view with clean data types
CREATE OR REPLACE VIEW policies_normalized AS
SELECT 
    id,
    "Client ID",
    "Transaction ID",
    "Customer",
    "Carrier Name",
    "Policy Type",
    "Policy Number",
    "Transaction Type",
    "Agent Comm (NEW 50% RWL 25%)",
    COALESCE("Policy Origination Date Parsed", TO_DATE("Policy Origination Date", 'MM/DD/YYYY')) as policy_origination_date,
    COALESCE("Effective Date Parsed", TO_DATE("Effective Date", 'MM/DD/YYYY')) as effective_date,
    COALESCE("X-DATE Parsed", TO_DATE("X-DATE", 'MM/DD/YYYY')) as expiration_date,
    "NEW BIZ CHECKLIST COMPLETE",
    clean_currency("Premium Sold") as premium_sold,
    CASE 
        WHEN "Policy Gross Comm %" ~ '^[0-9.]+%?$' 
        THEN REPLACE("Policy Gross Comm %", '%', '')::DECIMAL
        ELSE NULL 
    END as policy_gross_comm_percent,
    COALESCE("STMT DATE Parsed", TO_DATE("STMT DATE", 'MM/DD/YYYY')) as statement_date,
    clean_currency("Agency Estimated Comm/Revenue (AZ)") as agency_estimated_comm_revenue,
    clean_currency("Agency Gross Comm Received") as agency_gross_comm_received,
    "Agent Estimated Comm $" as agent_estimated_comm,
    COALESCE("Paid Amount Numeric", clean_currency("Paid Amount")) as paid_amount,
    "BALANCE DUE" as balance_due,
    "FULL OR MONTHLY PMTS" as payment_type,
    "NOTES" as notes,
    created_at,
    updated_at
FROM policies;

-- Data quality check queries
SELECT 'Total policies imported:' as metric, COUNT(*) as value FROM policies
UNION ALL
SELECT 'Policies with valid Transaction ID:' as metric, COUNT(*) as value FROM policies WHERE "Transaction ID" IS NOT NULL AND "Transaction ID" != ''
UNION ALL
SELECT 'Manual commission entries imported:' as metric, COUNT(*) as value FROM manual_commission_entries
UNION ALL
SELECT 'Commission payments imported:' as metric, COUNT(*) as value FROM commission_payments
UNION ALL
SELECT 'Renewal history records imported:' as metric, COUNT(*) as value FROM renewal_history;