-- =====================================================
-- Diagnostic Script for Transaction ID Issues
-- Run this to check column constraints and data
-- =====================================================

-- 1. Check Transaction ID column specifications
SELECT 
    column_name,
    data_type,
    character_maximum_length,
    is_nullable,
    column_default
FROM 
    information_schema.columns
WHERE 
    table_name = 'policies'
    AND column_name = 'Transaction ID';

-- 2. Check if there are any constraints on Transaction ID
SELECT 
    conname AS constraint_name,
    pg_get_constraintdef(oid) AS constraint_definition
FROM 
    pg_constraint
WHERE 
    conrelid = 'policies'::regclass
    AND pg_get_constraintdef(oid) LIKE '%Transaction ID%';

-- 3. Check if the validation function exists and works
SELECT validate_transaction_id_format('A1B2C3D-STMT-20240630') as should_be_true;
SELECT validate_transaction_id_format('A1B2C3D') as should_be_true;
SELECT validate_transaction_id_format('ABC-STMT-20240630') as should_be_false;

-- 4. Check if trigger exists
SELECT 
    tgname AS trigger_name,
    proname AS function_name
FROM 
    pg_trigger t
    JOIN pg_proc p ON t.tgfoid = p.oid
WHERE 
    tgrelid = 'policies'::regclass;

-- 5. Look for recent reconciliation attempts
SELECT 
    "Transaction ID",
    "Customer",
    "STMT DATE",
    reconciliation_status,
    is_reconciliation_entry,
    LENGTH("Transaction ID") as id_length
FROM 
    policies
WHERE 
    created_at > NOW() - INTERVAL '1 hour'
ORDER BY 
    created_at DESC
LIMIT 10;

-- 6. Test inserting a reconciliation transaction directly
-- This will help identify where the issue occurs
/*
INSERT INTO policies (
    "Transaction ID",
    "Customer",
    "Carrier Name",
    "Premium Sold",
    "Agency Estimated Comm/Revenue (CRM)",
    "Agency Comm Received (STMT)",
    "STMT DATE",
    reconciliation_status,
    is_reconciliation_entry
) VALUES (
    'TEST123-STMT-20240630',
    'Test Customer',
    'Test Carrier',
    0,
    0,
    100.00,
    '2024-06-30',
    'reconciled',
    TRUE
);

-- Check if it was inserted correctly
SELECT 
    "Transaction ID",
    LENGTH("Transaction ID") as id_length,
    reconciliation_status,
    is_reconciliation_entry
FROM 
    policies
WHERE 
    "Transaction ID" LIKE 'TEST123%';

-- Clean up test
DELETE FROM policies WHERE "Transaction ID" = 'TEST123-STMT-20240630';
*/