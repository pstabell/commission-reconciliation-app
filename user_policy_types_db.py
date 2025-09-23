"""
User-specific policy types using database storage.
Each user can manage their own policy types for dropdowns and categorization.
"""

import streamlit as st
from typing import Dict, List, Optional, Any
from database_utils import get_supabase_client
import json

class UserPolicyTypes:
    """Handle user-specific policy types stored in database."""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self._types_cache = None
        self._cache_user_id = None
    
    def get_user_policy_types(self) -> Dict[str, Any]:
        """Get policy types configuration for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        # Return default types if no user
        if not user_id and not user_email:
            return self._get_default_policy_types()
        
        # Check cache
        if self._types_cache and self._cache_user_id == user_id:
            return self._types_cache
        
        try:
            # Try to get user's policy types from database
            if user_id:
                response = self.supabase.table('user_policy_types').select('*').eq('user_id', user_id).execute()
            else:
                response = self.supabase.table('user_policy_types').select('*').eq('user_email', user_email).execute()
            
            if response.data and len(response.data) > 0:
                types_data = response.data[0]
                # Build result with only existing columns
                result = {
                    'policy_types': types_data.get('policy_types', [])
                }
                
                # Add optional fields if they exist
                if 'default_type' in types_data:
                    result['default'] = types_data['default_type']
                else:
                    result['default'] = 'HO3'  # Use default value
                
                if 'categories' in types_data:
                    result['categories'] = types_data['categories']
                else:
                    result['categories'] = self._get_default_categories()
                
                if 'version' in types_data:
                    result['version'] = types_data['version']
                else:
                    result['version'] = '1.0.0'
                
                self._types_cache = result
                self._cache_user_id = user_id
                return result
            
            # No types found, create default for user
            return self._create_user_types()
            
        except Exception as e:
            print(f"Error loading user policy types: {e}")
            return self._get_default_policy_types()
    
    def save_user_policy_types(self, policy_types: List[Dict], default_type: str = 'HO3', categories: Optional[List[str]] = None) -> bool:
        """Save policy types configuration for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        if not user_id and not user_email:
            return False
        
        try:
            # Prepare minimal required data first
            data = {
                'policy_types': policy_types,
                'user_email': user_email
            }
            if user_id:
                data['user_id'] = user_id
            
            # Optional fields to try adding
            optional_fields = []
            if default_type:
                optional_fields.append(('default_type', default_type))
            optional_fields.append(('version', '1.0.0'))
            if categories is not None:
                optional_fields.append(('categories', categories))
            
            # Function to try saving with different column combinations
            def try_save_with_columns(base_data, optional_cols):
                """Try to save with progressively fewer optional columns."""
                for i in range(len(optional_cols) + 1):
                    test_data = base_data.copy()
                    # Add optional columns for this attempt
                    for j in range(len(optional_cols) - i):
                        col_name, col_value = optional_cols[j]
                        test_data[col_name] = col_value
                    
                    try:
                        if user_id:
                            return self.supabase.table('user_policy_types').upsert(test_data, on_conflict='user_id').execute()
                        else:
                            # For email-based, we need to check if exists first
                            check = self.supabase.table('user_policy_types').select('id').eq('user_email', user_email).execute()
                            if check.data:
                                # Update existing - only include updateable fields
                                update_data = {'policy_types': policy_types}
                                for col_name, col_value in optional_cols[:len(optional_cols) - i]:
                                    if col_name != 'version':  # Don't update version on updates
                                        update_data[col_name] = col_value
                                return self.supabase.table('user_policy_types').update(update_data).eq('user_email', user_email).execute()
                            else:
                                # Insert new
                                return self.supabase.table('user_policy_types').insert(test_data).execute()
                    except Exception as e:
                        if i == len(optional_cols):  # Last attempt with minimal columns
                            raise e
                        print(f"Save attempt {i + 1} failed: {str(e)}")
                        continue
            
            # Try to save
            response = try_save_with_columns(data, optional_fields)
            # The try_save_with_columns function above handles all cases
            
            # Clear cache to force reload
            self._types_cache = None
            self._cache_user_id = None
            
            return True
            
        except Exception as e:
            print(f"Error saving user policy types: {e}")
            return False
    
    def get_policy_types_list(self) -> List[str]:
        """Get list of active policy type codes."""
        config = self.get_user_policy_types()
        return [pt['code'] for pt in config['policy_types'] if pt.get('active', True)]
    
    def get_policy_type_names(self) -> Dict[str, str]:
        """Get mapping of policy type codes to display names."""
        config = self.get_user_policy_types()
        return {pt['code']: pt['name'] for pt in config['policy_types']}
    
    def add_policy_type(self, code: str, name: str, category: str = 'Other', active: bool = True) -> bool:
        """Add a new policy type."""
        config = self.get_user_policy_types()
        
        # Check if already exists
        for pt in config['policy_types']:
            if pt['code'] == code:
                return False  # Already exists
        
        # Add new type
        config['policy_types'].append({
            'code': code,
            'name': name,
            'category': category,
            'active': active
        })
        
        # Save
        return self.save_user_policy_types(
            config['policy_types'], 
            config['default'], 
            config.get('categories')
        )
    
    def merge_policy_types(self, old_types: List[str], new_type: str) -> bool:
        """Merge multiple policy types into one."""
        # This would need to update the actual policies in the database
        # For now, just update the configuration
        config = self.get_user_policy_types()
        
        # Remove old types from config
        config['policy_types'] = [
            pt for pt in config['policy_types'] 
            if pt['code'] not in old_types
        ]
        
        # Make sure new type exists
        if not any(pt['code'] == new_type for pt in config['policy_types']):
            # Add it if it doesn't exist
            self.add_policy_type(new_type, new_type)
        
        return True
    
    def remove_policy_type(self, code: str) -> bool:
        """Remove a policy type if it's not a system default."""
        # List of protected system defaults that cannot be removed
        protected_types = ["GL", "WC", "BOP", "CPK", "CARGO", "AUTO", "EXCESS", "CYBER", "D&O", "E&O", "EPLI", "OTHER"]
        
        if code in protected_types:
            return False  # Cannot remove protected types
        
        config = self.get_user_policy_types()
        
        # Filter out the type to remove
        original_count = len(config['policy_types'])
        config['policy_types'] = [
            pt for pt in config['policy_types'] 
            if pt['code'] != code
        ]
        
        # Check if anything was removed
        if len(config['policy_types']) == original_count:
            return False  # Type didn't exist
        
        # Save the updated configuration
        return self.save_user_policy_types(config)
    
    def _create_user_types(self) -> Dict[str, Any]:
        """Create default policy types for a new user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        default_config = self._get_default_policy_types()
        
        # Save the default configuration for this user
        # Start with minimal required data
        data = {
            'policy_types': default_config['policy_types'],
            'user_email': user_email
        }
        if user_id:
            data['user_id'] = user_id
        
        # Try to save with progressive fallback
        columns_to_try = [
            ('categories', default_config['categories']),
            ('default_type', default_config['default']),
            ('version', '1.0.0')
        ]
        
        for attempt in range(len(columns_to_try) + 1):
            try:
                # Add optional columns based on attempt number
                test_data = data.copy()
                for i in range(len(columns_to_try) - attempt):
                    col_name, col_value = columns_to_try[i]
                    test_data[col_name] = col_value
                
                # Try to insert
                self.supabase.table('user_policy_types').insert(test_data).execute()
                return default_config
            except Exception as e:
                error_str = str(e)
                print(f"Insert attempt {attempt + 1} failed: {error_str}")
                
                # If it's the last attempt with minimal data, try upsert
                if attempt == len(columns_to_try):
                    try:
                        if user_id:
                            self.supabase.table('user_policy_types').upsert(data, on_conflict='user_id').execute()
                        else:
                            # For email-only, check if exists first
                            check = self.supabase.table('user_policy_types').select('id').eq('user_email', user_email).execute()
                            if not check.data:
                                raise e  # Re-raise if doesn't exist
                        return default_config
                    except:
                        print(f"Failed to create user policy types: {e}")
                        pass
        
        return default_config
    
    def _get_default_policy_types(self) -> Dict[str, Any]:
        """Get default policy types configuration."""
        return {
            'policy_types': [
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
            ],
            'default': 'HO3',
            'categories': self._get_default_categories(),
            'version': '1.0.0'
        }
    
    def _get_default_categories(self) -> List[str]:
        """Get default policy categories."""
        return [
            'Personal Property',
            'Personal Auto',
            'Commercial',
            'Specialty',
            'Personal',
            'Other'
        ]

# Create a global instance
user_policy_types = UserPolicyTypes()

# Backward compatible functions
def load_policy_types() -> Dict[str, Any]:
    """Load policy types configuration for current user."""
    return user_policy_types.get_user_policy_types()

def save_policy_types(config: Dict[str, Any]) -> bool:
    """Save policy types configuration for current user."""
    return user_policy_types.save_user_policy_types(
        config.get('policy_types', []),
        config.get('default', 'HO3'),
        config.get('categories')
    )

def get_policy_types_list() -> List[str]:
    """Get list of active policy type codes."""
    return user_policy_types.get_policy_types_list()

def get_policy_type_names() -> Dict[str, str]:
    """Get mapping of policy type codes to display names."""
    return user_policy_types.get_policy_type_names()