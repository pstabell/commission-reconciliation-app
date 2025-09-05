#!/bin/bash

# Supabase credentials
SUPABASE_URL="https://ddiahkzvmymacejqlnvc.supabase.co"
SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRkaWFoa3p2bXltYWNlanFsbnZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTExNjU2MTUsImV4cCI6MjA2Njc0MTYxNX0.KgBeoRKsQO6WsQ0TzlC772fY8gAoXJonuS4M1Mi3BLs"

echo "Listing available tables in Supabase..."
echo "====================================="

# Try to get schema information
curl -s -X GET "${SUPABASE_URL}/rest/v1/" \
     -H "apikey: ${SUPABASE_ANON_KEY}" \
     -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
     -H "Content-Type: application/json" | python3 -m json.tool