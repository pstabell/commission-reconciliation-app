#!/usr/bin/env python3
"""
Simple test to demonstrate the renewal fix logic.
"""

import json
import datetime

def test_renewal_logic():
    """Demonstrate the renewal tracking logic."""
    print("RENEWAL TRACKING DEMONSTRATION")
    print("=" * 60)
    
    # Original policy
    original_policy = {
        'Transaction ID': 'ORIG123',
        'Policy Number': '1AA338948',
        'Effective Date': '01/15/2024',
        'Customer': 'Starr Custom Tinting',
        'Client ID': 'SNKN73',
        'Carrier Name': 'Surplus Lines Carrier',
        'Transaction Type': 'NEW'
    }
    
    print("\n1. ORIGINAL POLICY:")
    for key, value in original_policy.items():
        print(f"   {key}: {value}")
    
    # First renewal (policy number changes)
    renewal_1 = {
        'Transaction ID': 'RWL456',
        'Policy Number': '277B513884',  # New policy number!
        'Prior Policy Number': '1AA338948',  # Links to original
        'Original Effective Date': '01/15/2024',  # Preserves inception date
        'Effective Date': '01/15/2025',
        'Customer': 'Starr Custom Tinting',
        'Client ID': 'SNKN73',
        'Carrier Name': 'Surplus Lines Carrier',
        'Transaction Type': 'RWL'
    }
    
    print("\n2. FIRST RENEWAL (Policy number changed):")
    for key, value in renewal_1.items():
        if key in ['Policy Number', 'Prior Policy Number', 'Original Effective Date']:
            print(f"   {key}: {value} ⭐")  # Highlight key fields
        else:
            print(f"   {key}: {value}")
    
    # Second renewal (policy number changes again)
    renewal_2 = {
        'Transaction ID': 'RWL789',
        'Policy Number': '399C624995',  # Another new policy number!
        'Prior Policy Number': '277B513884',  # Links to previous renewal
        'Original Effective Date': '01/15/2024',  # Still preserves original inception
        'Effective Date': '01/15/2026',
        'Customer': 'Starr Custom Tinting',
        'Client ID': 'SNKN73',
        'Carrier Name': 'Surplus Lines Carrier',
        'Transaction Type': 'RWL'
    }
    
    print("\n3. SECOND RENEWAL (Policy number changed again):")
    for key, value in renewal_2.items():
        if key in ['Policy Number', 'Prior Policy Number', 'Original Effective Date']:
            print(f"   {key}: {value} ⭐")
        else:
            print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)
    print("POLICY CHAIN TRACKING:")
    print(f"  Original Policy: {original_policy['Policy Number']} (Inception: {original_policy['Effective Date']})")
    print(f"  ↓")
    print(f"  1st Renewal: {renewal_1['Policy Number']} (Prior: {renewal_1['Prior Policy Number']})")
    print(f"  ↓")
    print(f"  2nd Renewal: {renewal_2['Policy Number']} (Prior: {renewal_2['Prior Policy Number']})")
    print(f"\n  ✅ Original inception date preserved throughout: {renewal_2['Original Effective Date']}")
    print("=" * 60)

if __name__ == "__main__":
    test_renewal_logic()