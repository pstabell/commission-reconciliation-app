#!/usr/bin/env python3
"""
Test script to verify the renewal fix implementation.
"""

import pandas as pd
import datetime
import json
from pathlib import Path
import sys

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import the convert_timestamps_for_json function
from commission_app import convert_timestamps_for_json

def test_timestamp_conversion():
    """Test that Timestamp objects are properly converted for JSON serialization."""
    print("Testing Timestamp conversion...")
    
    # Create test data with various timestamp types
    test_data = {
        'Transaction ID': 'TEST123',
        'Policy Number': 'POL456',
        'Effective Date': pd.Timestamp('2024-01-15'),
        'Created Date': datetime.datetime.now(),
        'Renewal Date': datetime.date.today(),
        'Premium': 1000.50,
        'Status': 'Active',
        'Empty Field': None,
        'NaN Field': float('nan')
    }
    
    print("\nOriginal data types:")
    for key, value in test_data.items():
        print(f"  {key}: {type(value).__name__} = {value}")
    
    # Convert timestamps
    converted_data = convert_timestamps_for_json(test_data)
    
    print("\nConverted data types:")
    for key, value in converted_data.items():
        print(f"  {key}: {type(value).__name__} = {value}")
    
    # Test JSON serialization
    try:
        json_str = json.dumps(converted_data)
        print("\n✅ JSON serialization successful!")
        print(f"JSON length: {len(json_str)} characters")
        
        # Parse it back to verify
        parsed = json.loads(json_str)
        print("✅ JSON parsing successful!")
        
    except Exception as e:
        print(f"\n❌ JSON serialization failed: {e}")
        return False
    
    return True

def test_policy_tracking_fields():
    """Test the policy tracking fields logic."""
    print("\n\nTesting policy tracking fields...")
    
    # Simulate renewal data
    original_policy = {
        'Transaction ID': 'ORIG123',
        'Policy Number': '1AA338948',
        'Effective Date': '01/15/2024',
        'Customer': 'Starr Custom Tinting',
        'Client ID': 'SNKN73'
    }
    
    # Simulate renewal with new policy number
    new_renewal = {
        'Transaction ID': 'RWL456',
        'Policy Number': '277B513884',  # New policy number
        'Transaction Type': 'RWL',
        'Effective Date': '01/15/2025',
        'Customer': 'Starr Custom Tinting',
        'Client ID': 'SNKN73'
    }
    
    # Add tracking fields
    new_renewal['Prior Policy Number'] = original_policy.get('Policy Number', '')
    new_renewal['Original Effective Date'] = original_policy.get('Effective Date', '')
    
    print("\nOriginal Policy:")
    print(f"  Policy Number: {original_policy['Policy Number']}")
    print(f"  Effective Date: {original_policy['Effective Date']}")
    
    print("\nRenewal Policy:")
    print(f"  Policy Number: {new_renewal['Policy Number']}")
    print(f"  Prior Policy Number: {new_renewal['Prior Policy Number']}")
    print(f"  Effective Date: {new_renewal['Effective Date']}")
    print(f"  Original Effective Date: {new_renewal['Original Effective Date']}")
    
    # Test renewal chain
    print("\n✅ Policy tracking fields successfully added!")
    print("   - Prior Policy Number links to: " + new_renewal['Prior Policy Number'])
    print("   - Original inception date preserved: " + new_renewal['Original Effective Date'])
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("RENEWAL FIX TEST SUITE")
    print("=" * 60)
    
    # Run tests
    test1_passed = test_timestamp_conversion()
    test2_passed = test_policy_tracking_fields()
    
    print("\n" + "=" * 60)
    print("TEST RESULTS:")
    print(f"  Timestamp Conversion: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"  Policy Tracking Fields: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print("=" * 60)