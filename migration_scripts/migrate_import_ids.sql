-- Migration Script: Add -IMPORT suffix to import-created transactions
-- Created: July 14, 2025
-- Purpose: Update transaction IDs for all import-created transactions

-- First, let's see what we're going to update (DRY RUN)
SELECT 
    "Transaction ID",
    "Customer",
    "NOTES",
    "Transaction ID" || '-IMPORT' as "New Transaction ID"
FROM policies
WHERE 
    "NOTES" LIKE '%Created from statement import%'
    AND "Transaction ID" NOT LIKE '%-IMPORT'
ORDER BY "Transaction ID";

-- Count how many we'll update
SELECT COUNT(*) as "Transactions to Update"
FROM policies
WHERE 
    "NOTES" LIKE '%Created from statement import%'
    AND "Transaction ID" NOT LIKE '%-IMPORT';

-- IMPORTANT: Review the results above before running the UPDATE below!
-- Make sure the transactions look correct

-- ========================================================
-- ACTUAL UPDATE - COMMENT OUT THE LINES BELOW UNTIL READY
-- ========================================================

/*
-- Update all import-created transactions to add -IMPORT suffix
UPDATE policies
SET "Transaction ID" = "Transaction ID" || '-IMPORT'
WHERE 
    "NOTES" LIKE '%Created from statement import%'
    AND "Transaction ID" NOT LIKE '%-IMPORT'
    AND "Transaction ID" IS NOT NULL;

-- Verify the update
SELECT 
    "Transaction ID",
    "Customer",
    "NOTES"
FROM policies
WHERE "Transaction ID" LIKE '%-IMPORT'
ORDER BY "Transaction ID";
*/

-- ========================================================
-- ROLLBACK SCRIPT (IF NEEDED)
-- ========================================================
-- If you need to undo this migration, use:
/*
UPDATE policies
SET "Transaction ID" = REPLACE("Transaction ID", '-IMPORT', '')
WHERE "Transaction ID" LIKE '%-IMPORT'
AND "NOTES" LIKE '%Created from statement import%';
*/