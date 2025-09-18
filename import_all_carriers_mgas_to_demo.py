"""
Import all carriers, MGAs, and commission rules to demo account in production.
This script generates SQL INSERT statements that you can run in Supabase.
"""

# All carriers from your system
CARRIERS = [
    ("Citizens", None, None),
    ("AAA", None, None),
    ("Progressive", None, None),
    ("Tower Hill", None, None),
    ("Heritage", None, None),
    ("Universal", None, None),
    ("Florida Peninsula", None, None),
    ("Federated National", None, None),
    ("St. Johns", None, None),
    ("Southern Oak", None, None),
    ("American Integrity", None, None),
    ("People's Trust", None, None),
    ("First Community", None, None),
    ("Centauri", None, None),
    ("Kin", None, None),
    ("Slide", None, None),
    ("TypTap", None, None),
    ("Homeowners Choice", None, None),
    ("United Property & Casualty", None, None),
    ("Safe Harbor", None, None),
    ("Elements", None, None),
    ("Cypress", None, None),
    ("Prepared", None, None),
    ("Velocity", None, None),
    ("Orchid", None, None),
    ("Edison", None, None),
    ("Olympus", None, None),
    ("Weston", None, None),
    ("Monarch", None, None),
    ("Family Security", None, None),
    ("Lighthouse", None, None),
    ("Anchor", None, None),
    ("ASI/Progressive", None, None),
    ("Foremost", None, None),
    ("American Strategic (ASI)", None, None),
    ("Bristol West", None, None),
    ("Safeco", None, None),
    ("Travelers", None, None),
    ("Allstate", None, None),
    ("State Farm", None, None),
    ("Farmers", None, None),
    ("Liberty Mutual", None, None),
    ("MetLife", None, None),
    ("Hartford", None, None),
    ("Chubb", None, None),
    ("Nationwide", None, None),
    ("Mercury", None, None),
    ("USAA", None, None),
    ("Auto-Owners", None, None),
    ("Erie", None, None),
    ("American Family", None, None),
    ("Kemper", None, None),
    ("Esurance", None, None),
    ("21st Century", None, None),
    ("National General", None, None),
    ("The General", None, None),
    ("Infinity", None, None),
    ("Hagerty", None, None),
    ("Grundy", None, None),
    ("Dairyland", None, None),
    ("Wright Flood", None, None),
    ("Neptune", None, None),
    ("Beyond Flood", None, None),
]

# All MGAs from your system
MGAS = [
    "Direct Appointment",
    "SureTec", 
    "Advantage Partners",
    "Florida Peninsula MGA",
    "Simon Agency",
    "Iroquois MGA",
    "Strategic Insurance Partners",
    "Southern Risk MGA",
    "Coastal MGA",
    "Premier MGA",
    "Elite MGA Services",
    "Professional Risk MGA",
    "Atlantic MGA",
    "Gulf Coast MGA",
    "Sunshine State MGA",
    "First Choice MGA",
]

# Common commission rules
COMMISSION_RULES = [
    # (carrier_name, mga_name, policy_type, new_rate, renewal_rate, description)
    ("Citizens", "Direct Appointment", None, 10.0, 10.0, "Citizens standard rate"),
    ("AAA", "Direct Appointment", "Auto,Package", 12.0, 12.0, "AAA Auto and Package products"),
    ("AAA", "Direct Appointment", "Home,Membership", 15.0, 15.0, "AAA Home and Membership products"),
    ("AAA", "Direct Appointment", "Umbrella", 10.0, 10.0, "AAA Umbrella products"),
    ("Progressive", "Direct Appointment", "Auto", 12.0, 10.0, "Progressive auto insurance"),
    ("Progressive", "Direct Appointment", "Home", 15.0, 12.0, "Progressive home insurance"),
    ("Progressive", "Direct Appointment", "Renters", 15.0, 15.0, "Progressive renters insurance"),
    ("Progressive", "Direct Appointment", "Boat", 10.0, 10.0, "Progressive boat insurance"),
    ("Tower Hill", "Direct Appointment", None, 18.0, 15.0, "Tower Hill standard rate"),
    ("Heritage", "Direct Appointment", None, 11.0, 11.0, "Heritage standard rate"),
    ("Universal", "Direct Appointment", None, 12.0, 8.0, "Universal standard rate"),
    ("Florida Peninsula", "Direct Appointment", None, 10.0, 10.0, "Florida Peninsula standard rate"),
    ("Federated National", "Direct Appointment", None, 8.0, 8.0, "Federated National standard rate"),
    ("St. Johns", "Direct Appointment", None, 10.0, 10.0, "St. Johns standard rate"),
    ("Southern Oak", "Direct Appointment", None, 10.0, 8.5, "Southern Oak standard rate"),
    ("American Integrity", "Direct Appointment", None, 12.0, 8.0, "American Integrity standard rate"),
    ("State Farm", "SureTec", None, 14.0, 12.0, "State Farm through SureTec"),
    ("Mercury", "Advantage Partners", None, 8.0, 6.0, "Mercury through Advantage Partners"),
    ("Safeco", "Direct Appointment", "Auto", 12.0, 10.0, "Safeco Auto insurance"),
    ("Safeco", "Direct Appointment", "Home", 15.0, 15.0, "Safeco Home insurance"),
    ("Travelers", "Direct Appointment", None, 12.0, 12.0, "Travelers standard rate"),
    ("Travelers", "Direct Appointment", "Umbrella", 10.0, 10.0, "Travelers Umbrella product"),
    ("Chubb", "Direct Appointment", "Auto,BOP,Umbrella", 15.0, 15.0, "Chubb Auto/BOP/Umbrella products"),
    ("Chubb", "Direct Appointment", "Cyber", 18.0, 15.0, "Chubb Cyber Liability"),
    ("National General", "Direct Appointment", None, 12.0, 12.0, "National General standard rate"),
    ("Wright Flood", "Direct Appointment", None, 15.0, 15.0, "Wright Flood standard rate"),
    ("Neptune", "Direct Appointment", None, 12.0, 12.0, "Neptune flood insurance"),
]

# Generate SQL
print("-- COMPLETE IMPORT SCRIPT FOR DEMO ACCOUNT")
print("-- Run this in Supabase SQL Editor")
print()

# Step 1: Clean existing demo data
print("-- Step 1: Clean existing demo data")
print("DELETE FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com';")
print("DELETE FROM carrier_mga_relationships WHERE user_email = 'Demo@AgentCommissionTracker.com';")
print("DELETE FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com';")
print("DELETE FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com';")
print()

# Step 2: Insert carriers
print("-- Step 2: Insert all carriers")
for carrier_name, naic_code, producer_code in CARRIERS:
    naic = f"'{naic_code}'" if naic_code else "NULL"
    prod = f"'{producer_code}'" if producer_code else "NULL"
    print(f"INSERT INTO carriers (carrier_id, carrier_name, naic_code, producer_code, status, user_email) VALUES (gen_random_uuid(), '{carrier_name}', {naic}, {prod}, 'Active', 'Demo@AgentCommissionTracker.com');")
print()

# Step 3: Insert MGAs
print("-- Step 3: Insert all MGAs")
for mga_name in MGAS:
    print(f"INSERT INTO mgas (mga_id, mga_name, status, user_email) VALUES (gen_random_uuid(), '{mga_name}', 'Active', 'Demo@AgentCommissionTracker.com');")
print()

# Step 4: Insert commission rules
print("-- Step 4: Insert commission rules")
print("-- Note: These use subqueries to find the carrier and MGA IDs")
for carrier, mga, policy_type, new_rate, renewal_rate, desc in COMMISSION_RULES:
    carrier_subquery = f"(SELECT carrier_id FROM carriers WHERE carrier_name = '{carrier}' AND user_email = 'Demo@AgentCommissionTracker.com')"
    mga_subquery = f"(SELECT mga_id FROM mgas WHERE mga_name = '{mga}' AND user_email = 'Demo@AgentCommissionTracker.com')" if mga != "Direct Appointment" else f"(SELECT mga_id FROM mgas WHERE mga_name = '{mga}' AND user_email = 'Demo@AgentCommissionTracker.com')"
    policy_type_val = f"'{policy_type}'" if policy_type else "NULL"
    desc_val = f"'{desc}'" if desc else "NULL"
    
    print(f"INSERT INTO commission_rules (carrier_id, mga_id, state, policy_type, new_rate, renewal_rate, rule_description, user_email, is_default, is_active) VALUES ({carrier_subquery}, {mga_subquery}, 'FL', {policy_type_val}, {new_rate}, {renewal_rate}, {desc_val}, 'Demo@AgentCommissionTracker.com', false, true);")

print()
print("-- Step 5: Verify import")
print("SELECT 'Import complete!' as status;")
print("SELECT 'Carriers: ' || COUNT(*) FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com'")
print("UNION ALL SELECT 'MGAs: ' || COUNT(*) FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com'")
print("UNION ALL SELECT 'Commission Rules: ' || COUNT(*) FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com';")