#!/usr/bin/env python3
"""Test environment and demo access."""

import os

# Check environment
print("ENVIRONMENT CHECK:")
print(f"APP_ENVIRONMENT = {os.getenv('APP_ENVIRONMENT')}")
print(f"APP_ENVIRONMENT == 'PRODUCTION': {os.getenv('APP_ENVIRONMENT') == 'PRODUCTION'}")

# Simulate get_normalized_user_email
def get_normalized_user_email(email):
    if email.lower() == 'demo@agentcommissiontracker.com':
        return 'Demo@AgentCommissionTracker.com'
    return email

# Test normalization
test_email = 'demo@agentcommissiontracker.com'
normalized = get_normalized_user_email(test_email)
print(f"\nEMAIL NORMALIZATION:")
print(f"Input: {test_email}")
print(f"Normalized: {normalized}")

# Check session state condition
print(f"\nCONDITION CHECK:")
has_email = True  # Simulating user_email in session_state
print(f"os.getenv('APP_ENVIRONMENT') == 'PRODUCTION' and has_email: {os.getenv('APP_ENVIRONMENT') == 'PRODUCTION' and has_email}")

# What query would run?
if os.getenv("APP_ENVIRONMENT") == "PRODUCTION" and has_email:
    print(f"\nWould query: WHERE user_email = '{normalized}'")
else:
    print("\nWould query: ALL carriers (no filter)")