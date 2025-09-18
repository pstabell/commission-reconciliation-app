#!/usr/bin/env python3
"""Test script to verify demo account can access carriers."""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Get Supabase credentials
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")

if not url or not key:
    print("ERROR: Missing SUPABASE_URL or SUPABASE_ANON_KEY in .env file")
    exit(1)

# Create Supabase client
supabase: Client = create_client(url, key)

print("Testing Supabase connection with anon key...")
print(f"URL: {url}")
print(f"Key: {key[:10]}...{key[-10:]}")  # Show partial key for verification

# Test 1: Direct query for demo carriers
print("\n1. Testing direct query for demo carriers:")
try:
    response = supabase.table('carriers').select("*").eq('user_email', 'Demo@AgentCommissionTracker.com').execute()
    print(f"   - Found {len(response.data)} carriers for demo user")
    if response.data:
        print(f"   - First carrier: {response.data[0]['carrier_name']}")
        print(f"   - Status: {response.data[0]['status']}")
except Exception as e:
    print(f"   - ERROR: {e}")

# Test 2: Count active carriers
print("\n2. Testing active carriers count:")
try:
    response = supabase.table('carriers').select("*").eq('user_email', 'Demo@AgentCommissionTracker.com').eq('status', 'Active').execute()
    print(f"   - Found {len(response.data)} active carriers")
except Exception as e:
    print(f"   - ERROR: {e}")

# Test 3: Check if RLS is blocking
print("\n3. Testing without user_email filter (to check RLS):")
try:
    response = supabase.table('carriers').select("*").limit(1).execute()
    if response.data:
        print(f"   - Can see carriers without filter: YES")
        print(f"   - Sample: {response.data[0]['carrier_name']} ({response.data[0]['user_email']})")
    else:
        print(f"   - Can see carriers without filter: NO (RLS might be blocking)")
except Exception as e:
    print(f"   - ERROR: {e}")

# Test 4: Check MGAs
print("\n4. Testing MGAs for demo:")
try:
    response = supabase.table('mgas').select("*").eq('user_email', 'Demo@AgentCommissionTracker.com').execute()
    print(f"   - Found {len(response.data)} MGAs for demo user")
except Exception as e:
    print(f"   - ERROR: {e}")

# Test 5: Check commission rules
print("\n5. Testing commission rules for demo:")
try:
    response = supabase.table('commission_rules').select("*").eq('user_email', 'Demo@AgentCommissionTracker.com').execute()
    print(f"   - Found {len(response.data)} commission rules for demo user")
except Exception as e:
    print(f"   - ERROR: {e}")

print("\nTest complete.")