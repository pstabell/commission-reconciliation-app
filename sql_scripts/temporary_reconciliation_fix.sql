-- TEMPORARY FIX for reconciliation showing all zeros
-- This is a quick fix to get reconciliation working while a proper code fix is implemented

-- Option 1: Quick fix for current user only
-- Replace 'your@email.com' with the actual user email
UPDATE policies 
SET "Total Agent Comm" = 
    CASE 
        WHEN COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) + COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0) > 0 
        THEN COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) + COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0)
        ELSE COALESCE(CAST("Agency Estimated Comm/Revenue (CRM)" AS NUMERIC), 0) * 0.5  -- Fallback to 50% of agency commission
    END
WHERE user_email = 'your@email.com'  -- CHANGE THIS TO YOUR EMAIL
AND ("Total Agent Comm" IS NULL OR CAST("Total Agent Comm" AS TEXT) = '' OR CAST("Total Agent Comm" AS TEXT) = '0');

-- Option 2: Fix for ALL users (use carefully)
/*
UPDATE policies 
SET "Total Agent Comm" = 
    CASE 
        WHEN COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) + COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0) > 0 
        THEN COALESCE(CAST("Agent Estimated Comm $" AS NUMERIC), 0) + COALESCE(CAST("Broker Fee Agent Comm" AS NUMERIC), 0)
        ELSE COALESCE(CAST("Agency Estimated Comm/Revenue (CRM)" AS NUMERIC), 0) * 0.5
    END
WHERE ("Total Agent Comm" IS NULL OR CAST("Total Agent Comm" AS TEXT) = '' OR CAST("Total Agent Comm" AS TEXT) = '0')
AND COALESCE(CAST("Agency Estimated Comm/Revenue (CRM)" AS NUMERIC), 0) > 0;
*/

-- Verify the fix worked
SELECT 
    'After Fix - Transactions Available for Reconciliation:' as status,
    COUNT(*) as count
FROM policies
WHERE CAST("Total Agent Comm" AS NUMERIC) > 0
AND user_email = 'your@email.com';  -- CHANGE THIS TO YOUR EMAIL