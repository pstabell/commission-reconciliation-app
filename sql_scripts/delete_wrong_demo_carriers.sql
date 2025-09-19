-- DELETE WRONG CARRIERS AND IMPORT CORRECT ONES

-- 1. First, let's save what commission rules exist (if any)
SELECT 'SAVING EXISTING RULES:' as info;
SELECT COUNT(*) as existing_rules
FROM commission_rules
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. DELETE ALL WRONG CARRIERS
DELETE FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 3. Verify deletion
SELECT '';
SELECT 'AFTER DELETION:' as info;
SELECT COUNT(*) as remaining_carriers
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 4. Now INSERT the CORRECT carriers from your private database
-- These are the 63 carriers you actually use as an independent agent
INSERT INTO carriers (carrier_id, carrier_name, status, user_email, created_at, updated_at)
VALUES
    (gen_random_uuid(), 'ASI', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Ambetter/Centene', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'American Coastal', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'American Integrity', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Anchor', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Ark Royal', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Bankers', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Bristol West', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Burlington', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Citizens', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Clear Spring', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Cova', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Edison', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'EIG/NOVA', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Elements', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'FHB (Farm Home Business)', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'FedNat', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'First Community', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'First Protective', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Florida Peninsula', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Frontline', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Gulfstream', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Heritage', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Homeowners Choice', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'JEFFVA (Slide)', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Kin', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Liberty Mutual', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Mercury', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Monarch (Southern Oak)', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Occidental', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Olympus', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Pacific Specialty', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'People''s Trust', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Plymouth Rock (Bunker Hill Ins Co)', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Progressive', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'QBE', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'PURE', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'RLI - Vacant Homes DP1 and DP3', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Rockhill (Vacant/Specialty)', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'SafePoint', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'SECURA', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Security First', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Southern Fidelity', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Southern Oak/Monarch', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'St. John''s', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'State Auto', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'State Farm Florida', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Stillwater', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Swyfft', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'The Hartford', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Tower Hill Prime', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Tower Hill Specialty (CitCo and FNIC)', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Travelers', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Truck Pro', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Twico Business Owners Policy', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'TWICO Package Policies', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'TWICO Vacant', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Typhoon (Acacia)', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'United', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'UPC/APPCOVA/FNIC (United P&C Ins)', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'US Assure', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Universal - North Point', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Universal PC- Arrowhead', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Vault Reciprocal Exchange', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW()),
    (gen_random_uuid(), 'Wright Flood', 'Active', 'Demo@AgentCommissionTracker.com', NOW(), NOW());

-- 5. Verify import
SELECT '';
SELECT 'IMPORT COMPLETE:' as info;
SELECT COUNT(*) as correct_carriers_count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 6. Confirm Burlington is there
SELECT '';
SELECT 'BURLINGTON CHECK:' as info;
SELECT carrier_name
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND carrier_name = 'Burlington';