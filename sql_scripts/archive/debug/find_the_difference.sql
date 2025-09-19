-- FIND THE ACTUAL DIFFERENCE
-- We have 63 carriers in demo, Burlington is missing but was in our import list
-- So what carrier is in demo that SHOULDN'T be there?

-- List all demo carriers alphabetically
SELECT 'ALL 63 DEMO CARRIERS:' as info;
SELECT carrier_name
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name;

-- The original private list had these 63 carriers:
-- ASI, Ambetter/Centene, American Coastal, American Integrity, Anchor, Ark Royal, 
-- Bankers, Bristol West, Burlington, Citizens, Clear Spring, Cova, 
-- Edison, EIG/NOVA, Elements, FHB (Farm Home Business), FedNat, First Community, 
-- First Protective, Florida Peninsula, Frontline, Gulfstream, Heritage, 
-- Homeowners Choice, JEFFVA (Slide), Kin, Liberty Mutual, Mercury, 
-- Monarch (Southern Oak), Occidental, Olympus, Pacific Specialty, People's Trust, 
-- Plymouth Rock (Bunker Hill Ins Co), Progressive, QBE, PURE, 
-- RLI - Vacant Homes DP1 and DP3, Rockhill (Vacant/Specialty), SafePoint, SECURA, 
-- Security First, Southern Fidelity, Southern Oak/Monarch, St. John's, State Auto, 
-- State Farm Florida, Stillwater, Swyfft, The Hartford, Tower Hill Prime, 
-- Tower Hill Specialty (CitCo and FNIC), Travelers, Truck Pro, Twico Business Owners Policy, 
-- TWICO Package Policies, TWICO Vacant, Typhoon (Acacia), United, 
-- UPC/APPCOVA/FNIC (United P&C Ins), US Assure, Universal - North Point, 
-- Universal PC- Arrowhead, Vault Reciprocal Exchange, Wright Flood

-- So one of these is missing (Burlington) and something else is there instead