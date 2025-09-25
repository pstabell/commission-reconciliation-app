#!/usr/bin/env python3
"""
Fix script to populate empty policy_types arrays with default values.
This solves the "No policy types found" issue in the Admin Panel.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_utils import get_supabase_client

def fix_empty_policy_types():
    """Update records with empty policy_types to have default values."""
    
    print("=== Fixing Empty Policy Types ===\n")
    
    try:
        supabase = get_supabase_client()
        
        # Default policy types (from user_policy_types_db.py)
        default_policy_types = [
            {'code': 'AUTOP', 'name': 'AUTOP', 'active': True, 'category': 'Other'},
            {'code': 'HOME', 'name': 'HOME', 'active': True, 'category': 'Personal Property'},
            {'code': 'DFIRE', 'name': 'DFIRE', 'active': True, 'category': 'Personal Property'},
            {'code': 'WC', 'name': 'WC', 'active': True, 'category': 'Other'},
            {'code': 'AUTOB', 'name': 'AUTOB', 'active': True, 'category': 'Other'},
            {'code': 'GL', 'name': 'GL', 'active': True, 'category': 'Other'},
            {'code': 'FLOOD', 'name': 'FLOOD', 'active': True, 'category': 'Specialty'},
            {'code': 'BOAT', 'name': 'BOAT', 'active': True, 'category': 'Specialty'},
            {'code': 'CONDO', 'name': 'CONDO', 'active': True, 'category': 'Personal Property'},
            {'code': 'PROP-C', 'name': 'PROP-C', 'active': True, 'category': 'Other'},
            {'code': 'PACKAGE-P', 'name': 'PACKAGE-P', 'active': True, 'category': 'Other'},
            {'code': 'UMB-P', 'name': 'UMB-P', 'active': True, 'category': 'Other'},
            {'code': 'IM-C', 'name': 'IM-C', 'active': True, 'category': 'Other'},
            {'code': 'GARAGE', 'name': 'GARAGE', 'active': True, 'category': 'Other'},
            {'code': 'UMB-C', 'name': 'UMB-C', 'active': True, 'category': 'Other'},
            {'code': 'OCEAN MARINE', 'name': 'OCEAN MARINE', 'active': True, 'category': 'Other'},
            {'code': 'WIND-P', 'name': 'WIND-P', 'active': True, 'category': 'Other'},
            {'code': 'PL', 'name': 'PL', 'active': True, 'category': 'Other'},
            {'code': 'COLLECTOR', 'name': 'COLLECTOR', 'active': True, 'category': 'Other'},
            {'code': 'PACKAGE-C', 'name': 'PACKAGE-C', 'active': True, 'category': 'Commercial'},
            {'code': 'FLOOD-C', 'name': 'FLOOD-C', 'active': True, 'category': 'Other'},
            {'code': 'BOP', 'name': 'BOP', 'active': True, 'category': 'Commercial'},
            {'code': 'BPP', 'name': 'BPP', 'active': True, 'category': 'Other'},
            {'code': 'EXCESS', 'name': 'EXCESS', 'active': True, 'category': 'Other'},
            {'code': 'CYBER', 'name': 'CYBER', 'active': True, 'category': 'Commercial'},
            {'code': 'D&O', 'name': 'D&O', 'active': True, 'category': 'Other'},
            {'code': 'CYCLE', 'name': 'CYCLE', 'active': True, 'category': 'Personal Auto'},
            {'code': 'AUTO', 'name': 'AUTO', 'active': True, 'category': 'Personal Auto'},
            {'code': 'RV', 'name': 'RV', 'active': True, 'category': 'Personal Auto'},
            {'code': 'RENTERS', 'name': 'RENTERS', 'active': True, 'category': 'Personal Property'},
            {'code': 'UMBRELLA', 'name': 'UMBRELLA-C', 'active': True, 'category': 'Commercial'},
            {'code': 'MOBILE', 'name': 'MOBILE', 'active': True, 'category': 'Personal Property'},
            {'code': 'WIND', 'name': 'WIND', 'active': True, 'category': 'Specialty'},
            {'code': 'UMBRELLA-P', 'name': 'UMBRELLA-P', 'active': True, 'category': 'Personal'}
        ]
        
        # First, find all records with empty or null policy_types
        print("1. Finding records with empty policy_types...")
        response = supabase.table('user_policy_types').select('id, user_email, policy_types').execute()
        
        empty_records = []
        if response.data:
            for record in response.data:
                policy_types = record.get('policy_types', None)
                
                # Check if empty (None, empty string, empty array, or '[]' string)
                is_empty = (
                    policy_types is None or
                    policy_types == [] or
                    policy_types == '[]' or
                    (isinstance(policy_types, str) and len(policy_types.strip()) == 0)
                )
                
                if is_empty:
                    empty_records.append(record)
        
        print(f"   Found {len(empty_records)} records with empty policy_types\n")
        
        if empty_records:
            print("2. Updating empty records with default policy types...")
            
            success_count = 0
            for record in empty_records:
                try:
                    # Update with default policy types
                    update_response = supabase.table('user_policy_types').update({
                        'policy_types': default_policy_types
                    }).eq('id', record['id']).execute()
                    
                    print(f"   ✓ Updated {record['user_email']}")
                    success_count += 1
                except Exception as e:
                    print(f"   ✗ Failed to update {record['user_email']}: {e}")
            
            print(f"\n3. Summary:")
            print(f"   - Total records found: {len(empty_records)}")
            print(f"   - Successfully updated: {success_count}")
            print(f"   - Failed updates: {len(empty_records) - success_count}")
        else:
            print("   No empty records found - all users have policy types configured!")
            
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_empty_policy_types()