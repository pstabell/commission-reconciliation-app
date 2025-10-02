-- =====================================================================
-- Migration: Add UNIQUE constraint to Transaction ID
-- Date: 2025-01-02
-- Purpose: Prevent duplicate Transaction IDs in policies table
--
-- IMPORTANT: Run check_duplicate_transaction_ids.py FIRST to ensure
--            no duplicates exist before applying this constraint!
-- =====================================================================

-- Step 1: Check for existing duplicates (informational query)
-- Run this first to verify no duplicates exist
SELECT
    "Transaction ID",
    COUNT(*) as occurrence_count,
    STRING_AGG(_id::text, ', ') as record_ids
FROM policies
WHERE "Transaction ID" IS NOT NULL
GROUP BY "Transaction ID"
HAVING COUNT(*) > 1
ORDER BY occurrence_count DESC;

-- If the above query returns any rows, DO NOT proceed with Step 2!
-- Fix duplicates manually first.

-- =====================================================================
-- Step 2: Create UNIQUE index (constraint) on Transaction ID
-- This will fail if duplicates exist
-- =====================================================================

-- Create a unique index that acts as a UNIQUE constraint
CREATE UNIQUE INDEX IF NOT EXISTS idx_policies_transaction_id_unique
ON public.policies USING btree ("Transaction ID")
WHERE "Transaction ID" IS NOT NULL;  -- Only enforce uniqueness on non-null values

-- Add a comment to document the constraint
COMMENT ON INDEX idx_policies_transaction_id_unique IS
'Unique constraint on Transaction ID to prevent duplicates. Created 2025-01-02.';

-- =====================================================================
-- Step 3: Verify the constraint was created
-- =====================================================================

-- Check if the unique index exists
SELECT
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'policies'
  AND indexname = 'idx_policies_transaction_id_unique';

-- =====================================================================
-- Rollback (if needed)
-- =====================================================================

-- To remove the unique constraint, run:
-- DROP INDEX IF EXISTS idx_policies_transaction_id_unique;

-- =====================================================================
-- Testing the constraint
-- =====================================================================

-- Try to insert a duplicate (should fail after constraint is added)
-- DO NOT RUN THIS ON PRODUCTION!
/*
DO $$
DECLARE
    test_transaction_id text;
BEGIN
    -- Get an existing Transaction ID
    SELECT "Transaction ID" INTO test_transaction_id
    FROM policies
    WHERE "Transaction ID" IS NOT NULL
    LIMIT 1;

    -- Try to insert a duplicate
    INSERT INTO policies ("Transaction ID", "Customer", "Policy Type")
    VALUES (test_transaction_id, 'Test Customer', 'Test Type');

    RAISE NOTICE 'ERROR: Duplicate was inserted! Constraint not working!';
EXCEPTION
    WHEN unique_violation THEN
        RAISE NOTICE 'SUCCESS: Unique constraint is working correctly!';
END $$;
*/

-- =====================================================================
-- Notes:
-- =====================================================================

-- 1. The constraint uses a partial index (WHERE "Transaction ID" IS NOT NULL)
--    to allow NULL values (which are always considered unique in PostgreSQL)
--
-- 2. The application now uses generate_unique_transaction_id() which checks
--    for duplicates before inserting, making collisions extremely rare
--
-- 3. This constraint provides a final safety net at the database level
--
-- 4. If you need to temporarily disable the constraint:
--    ALTER INDEX idx_policies_transaction_id_unique SET (fillfactor = 100);
--    (Note: This doesn't actually disable it, better to DROP and recreate)
--
-- 5. Monitor for constraint violations in application logs after deployment
