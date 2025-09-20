-- ============================================
-- SQLite to PostgreSQL Data Import Instructions
-- ============================================

-- STEP 1: Export SQLite data to CSV files
-- Run these commands in your terminal:
/*
sqlite3 commissions.db <<EOF
.headers on
.mode csv
.output policies.csv
SELECT * FROM policies;
.output commission_payments.csv
SELECT * FROM commission_payments;
.output manual_commission_entries.csv
SELECT * FROM manual_commission_entries;
.output renewal_history.csv
SELECT * FROM renewal_history;
.quit
EOF
*/

-- STEP 2: Import CSV files into PostgreSQL
-- Run these COPY commands in PostgreSQL:

-- Import policies (excluding the id column which will be auto-generated)
COPY policies(
    "Client ID",
    "Transaction ID",
    "Customer",
    "Carrier Name",
    "Policy Type",
    "Policy Number",
    "Transaction Type",
    "Agent Comm (NEW 50% RWL 25%)",
    "Policy Origination Date",
    "Effective Date",
    "X-DATE",
    "NEW BIZ CHECKLIST COMPLETE",
    "Premium Sold",
    "Policy Gross Comm %",
    "STMT DATE",
    "Agency Estimated Comm/Revenue (AZ)",
    "Agency Gross Comm Received",
    "Agent Estimated Comm $",
    "Paid Amount",
    "BALANCE DUE",
    "FULL OR MONTHLY PMTS",
    "NOTES"
)
FROM '/path/to/policies.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '"', ESCAPE '"');

-- Import commission_payments (id will be auto-generated)
-- First, create a temporary table to handle the SQLite ID
CREATE TEMP TABLE temp_commission_payments AS SELECT * FROM commission_payments WHERE 1=0;
ALTER TABLE temp_commission_payments ADD COLUMN sqlite_id INTEGER;

COPY temp_commission_payments(sqlite_id, policy_number, customer, payment_amount, statement_date, payment_timestamp, statement_details)
FROM '/path/to/commission_payments.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '"', ESCAPE '"');

-- Insert into final table without the SQLite ID
INSERT INTO commission_payments(policy_number, customer, payment_amount, statement_date, payment_timestamp, statement_details)
SELECT policy_number, customer, payment_amount, statement_date, payment_timestamp, statement_details
FROM temp_commission_payments;

DROP TABLE temp_commission_payments;

-- Import manual_commission_entries (similar process)
CREATE TEMP TABLE temp_manual_entries AS SELECT * FROM manual_commission_entries WHERE 1=0;
ALTER TABLE temp_manual_entries ADD COLUMN sqlite_id INTEGER;

COPY temp_manual_entries(sqlite_id, customer, policy_type, policy_number, effective_date, transaction_type, commission_paid, agency_commission_received, statement_date, client_id, transaction_id)
FROM '/path/to/manual_commission_entries.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '"', ESCAPE '"');

INSERT INTO manual_commission_entries(customer, policy_type, policy_number, effective_date, transaction_type, commission_paid, agency_commission_received, statement_date, client_id, transaction_id)
SELECT customer, policy_type, policy_number, effective_date, transaction_type, commission_paid, agency_commission_received, statement_date, client_id, transaction_id
FROM temp_manual_entries;

DROP TABLE temp_manual_entries;

-- Import renewal_history (similar process)
CREATE TEMP TABLE temp_renewal_history AS SELECT * FROM renewal_history WHERE 1=0;
ALTER TABLE temp_renewal_history ADD COLUMN sqlite_id INTEGER;

COPY temp_renewal_history(sqlite_id, renewal_timestamp, renewed_by, original_transaction_id, new_transaction_id, details)
FROM '/path/to/renewal_history.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '"', ESCAPE '"');

INSERT INTO renewal_history(renewal_timestamp, renewed_by, original_transaction_id, new_transaction_id, details)
SELECT renewal_timestamp, renewed_by, original_transaction_id, new_transaction_id, details
FROM temp_renewal_history;

DROP TABLE temp_renewal_history;

-- STEP 3: Verify the import
SELECT 'policies' as table_name, COUNT(*) as row_count FROM policies
UNION ALL
SELECT 'commission_payments', COUNT(*) FROM commission_payments
UNION ALL
SELECT 'manual_commission_entries', COUNT(*) FROM manual_commission_entries
UNION ALL
SELECT 'renewal_history', COUNT(*) FROM renewal_history;

-- STEP 4: Update sequences to correct values
SELECT setval('commission_payments_id_seq', (SELECT MAX(id) FROM commission_payments));
SELECT setval('manual_commission_entries_id_seq', (SELECT MAX(id) FROM manual_commission_entries));
SELECT setval('renewal_history_id_seq', (SELECT MAX(id) FROM renewal_history));