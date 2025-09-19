-- COPY ALL CARRIERS, MGAS, AND COMMISSION RULES TO DEMO ACCOUNT
-- This script copies all data that doesn't have a user_email to Demo@AgentCommissionTracker.com

-- 1. First, let's see what we're going to copy
SELECT 'PREVIEW - Data to be copied:' as info;
SELECT 
    'Carriers without user_email: ' || COUNT(*) as count
FROM carriers 
WHERE user_email IS NULL
UNION ALL
SELECT 
    'MGAs without user_email: ' || COUNT(*)
FROM mgas 
WHERE user_email IS NULL
UNION ALL
SELECT 
    'Commission rules without user_email: ' || COUNT(*)
FROM commission_rules 
WHERE user_email IS NULL;

-- 2. Create temporary tables with new IDs for demo user
SELECT '';
SELECT 'STEP 1: Creating temporary mapping tables...' as status;

-- Create carrier mapping
CREATE TEMP TABLE carrier_mapping AS
SELECT 
    carrier_id as old_id,
    gen_random_uuid() as new_id,
    carrier_name,
    naic_code,
    producer_code,
    parent_company,
    status,
    notes
FROM carriers
WHERE user_email IS NULL;

-- Create MGA mapping
CREATE TEMP TABLE mga_mapping AS
SELECT 
    mga_id as old_id,
    gen_random_uuid() as new_id,
    mga_name,
    status,
    notes
FROM mgas
WHERE user_email IS NULL;

-- 3. Insert carriers for demo user
SELECT 'STEP 2: Inserting carriers for demo user...' as status;
INSERT INTO carriers (carrier_id, carrier_name, naic_code, producer_code, parent_company, status, notes, user_email)
SELECT 
    new_id,
    carrier_name,
    naic_code,
    producer_code,
    parent_company,
    status,
    notes,
    'Demo@AgentCommissionTracker.com'
FROM carrier_mapping;

-- 4. Insert MGAs for demo user
SELECT 'STEP 3: Inserting MGAs for demo user...' as status;
INSERT INTO mgas (mga_id, mga_name, status, notes, user_email)
SELECT 
    new_id,
    mga_name,
    status,
    notes,
    'Demo@AgentCommissionTracker.com'
FROM mga_mapping;

-- 5. Insert commission rules with mapped IDs
SELECT 'STEP 4: Inserting commission rules for demo user...' as status;
INSERT INTO commission_rules (
    carrier_id, 
    mga_id, 
    state, 
    policy_type, 
    term_months, 
    new_rate, 
    renewal_rate, 
    payment_terms, 
    rule_description, 
    rule_priority, 
    is_default,
    user_email,
    effective_date,
    is_active
)
SELECT 
    COALESCE(cm.new_id, cr.carrier_id) as carrier_id,
    COALESCE(mm.new_id, cr.mga_id) as mga_id,
    cr.state,
    cr.policy_type,
    cr.term_months,
    cr.new_rate,
    cr.renewal_rate,
    cr.payment_terms,
    cr.rule_description,
    cr.rule_priority,
    cr.is_default,
    'Demo@AgentCommissionTracker.com',
    cr.effective_date,
    cr.is_active
FROM commission_rules cr
LEFT JOIN carrier_mapping cm ON cr.carrier_id = cm.old_id
LEFT JOIN mga_mapping mm ON cr.mga_id = mm.old_id
WHERE cr.user_email IS NULL
AND cr.is_active = true;

-- 6. Verify the results
SELECT '';
SELECT 'STEP 5: Verification...' as status;
SELECT 
    'Demo account now has:' as info
UNION ALL
SELECT 
    '  Carriers: ' || COUNT(*) 
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    '  MGAs: ' || COUNT(*)
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    '  Commission rules: ' || COUNT(*)
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 7. Show some sample data
SELECT '';
SELECT 'Sample carriers for demo:' as info;
SELECT carrier_name, status 
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com' 
ORDER BY carrier_name 
LIMIT 5;

SELECT '';
SELECT 'Sample MGAs for demo:' as info;
SELECT mga_name, status 
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com' 
ORDER BY mga_name 
LIMIT 5;

SELECT '';
SELECT 'SUCCESS: All data copied to demo account!' as status;