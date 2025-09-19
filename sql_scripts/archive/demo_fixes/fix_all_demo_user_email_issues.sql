-- COMPREHENSIVE FIX FOR DEMO USER EMAIL ISSUES
-- This script ensures all carriers, MGAs, and relationships are properly assigned to the demo user
-- Run this in Supabase SQL Editor

-- Step 1: Show current state
SELECT '=== CURRENT STATE ===' as section;
SELECT 'Carriers without user_email:', COUNT(*) FROM carriers WHERE user_email IS NULL;
SELECT 'MGAs without user_email:', COUNT(*) FROM mgas WHERE user_email IS NULL;
SELECT 'Total carriers:', COUNT(*) FROM carriers;
SELECT 'Total MGAs:', COUNT(*) FROM mgas;

-- Step 2: Update carriers with NULL user_email to demo user
UPDATE carriers 
SET user_email = 'Demo@AgentCommissionTracker.com'
WHERE user_email IS NULL;

-- Step 3: Update MGAs with NULL user_email to demo user
UPDATE mgas 
SET user_email = 'Demo@AgentCommissionTracker.com'
WHERE user_email IS NULL;

-- Step 4: Check if carrier_mga_relationships has user_email column and update if needed
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'carrier_mga_relationships' 
        AND column_name = 'user_email'
    ) THEN
        -- Update relationships where both carrier and MGA belong to demo user
        UPDATE carrier_mga_relationships cmr
        SET user_email = 'Demo@AgentCommissionTracker.com'
        FROM carriers c, mgas m
        WHERE cmr.carrier_id = c.carrier_id
          AND cmr.mga_id = m.mga_id
          AND c.user_email = 'Demo@AgentCommissionTracker.com'
          AND m.user_email = 'Demo@AgentCommissionTracker.com'
          AND (cmr.user_email IS NULL OR cmr.user_email != 'Demo@AgentCommissionTracker.com');
          
        RAISE NOTICE 'Updated carrier_mga_relationships user_email values';
    ELSE
        RAISE NOTICE 'carrier_mga_relationships table does not have user_email column';
    END IF;
END $$;

-- Step 5: Verify the results
SELECT '';
SELECT '=== AFTER UPDATE ===' as section;
SELECT 'Demo user carriers:', COUNT(*) FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com';
SELECT 'Demo user MGAs:', COUNT(*) FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com';
SELECT 'Demo user commission rules:', COUNT(*) FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- Step 6: Show sample data
SELECT '';
SELECT '=== SAMPLE CARRIERS (first 20) ===' as section;
SELECT carrier_name, status
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name
LIMIT 20;

SELECT '';
SELECT '=== SAMPLE MGAS (first 10) ===' as section;
SELECT mga_name, status
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY mga_name
LIMIT 10;

-- Step 7: Show carrier-MGA relationships
SELECT '';
SELECT '=== SAMPLE RELATIONSHIPS (first 15) ===' as section;
SELECT 
    c.carrier_name,
    m.mga_name,
    CASE WHEN cmr.is_direct THEN 'Direct' ELSE 'Through MGA' END as relationship_type
FROM carrier_mga_relationships cmr
JOIN carriers c ON cmr.carrier_id = c.carrier_id
JOIN mgas m ON cmr.mga_id = m.mga_id
WHERE c.user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY c.carrier_name, m.mga_name
LIMIT 15;

-- Step 8: Final summary
SELECT '';
SELECT '=== FINAL SUMMARY ===' as section;
SELECT 
    'Data Available for Demo User' as description,
    (SELECT COUNT(*) FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com') as carriers,
    (SELECT COUNT(*) FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com') as mgas,
    (SELECT COUNT(*) FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com') as commission_rules;