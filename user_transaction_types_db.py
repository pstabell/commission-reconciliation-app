"""
User-specific transaction types using database storage.
Each user can manage their own transaction types for categorization.
"""

import streamlit as st
from typing import Dict, Optional
from database_utils import get_supabase_client
import json

class UserTransactionTypes:
    """Handle user-specific transaction types stored in database."""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self._types_cache = None
        self._cache_user_id = None
    
    def get_user_transaction_types(self) -> Dict[str, Dict[str, any]]:
        """Get transaction types for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        # Return default types if no user
        if not user_id and not user_email:
            return self._get_default_transaction_types()
        
        # Check cache
        if self._types_cache and self._cache_user_id == user_id:
            return self._types_cache
        
        try:
            # Try to get user's transaction types from database
            if user_id:
                response = self.supabase.table('user_transaction_types').select('*').eq('user_id', user_id).execute()
            else:
                response = self.supabase.table('user_transaction_types').select('*').eq('user_email', user_email).execute()
            
            if response.data and len(response.data) > 0:
                types_data = response.data[0]
                result = types_data.get('transaction_types', {})
                self._types_cache = result
                self._cache_user_id = user_id
                return result
            
            # No types found, create default for user
            return self._create_user_types()
            
        except Exception as e:
            print(f"Error loading user transaction types: {e}")
            return self._get_default_transaction_types()
    
    def save_user_transaction_types(self, transaction_types: Dict[str, Dict[str, any]]) -> bool:
        """Save transaction types for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        if not user_id and not user_email:
            return False
        
        try:
            # Prepare the data
            data = {
                'transaction_types': transaction_types,
                'user_email': user_email
            }
            if user_id:
                data['user_id'] = user_id
            
            # Try to update existing record
            if user_id:
                response = self.supabase.table('user_transaction_types').upsert(data, on_conflict='user_id').execute()
            else:
                # Check if record exists
                check_response = self.supabase.table('user_transaction_types').select('id').eq('user_email', user_email).execute()
                if check_response.data:
                    # Update existing
                    response = self.supabase.table('user_transaction_types').update({
                        'transaction_types': transaction_types
                    }).eq('user_email', user_email).execute()
                else:
                    # Insert new
                    response = self.supabase.table('user_transaction_types').insert(data).execute()
            
            # Clear cache to force reload
            self._types_cache = None
            self._cache_user_id = None
            
            return True
            
        except Exception as e:
            print(f"Error saving user transaction types: {e}")
            return False
    
    def add_transaction_type(self, code: str, description: str, active: bool = True) -> bool:
        """Add a new transaction type."""
        types = self.get_user_transaction_types()
        
        # Add new type
        types[code] = {
            'description': description,
            'active': active
        }
        
        # Save
        return self.save_user_transaction_types(types)
    
    def merge_transaction_types(self, old_codes: list, new_code: str, new_description: str) -> bool:
        """Merge multiple transaction types into one."""
        types = self.get_user_transaction_types()
        
        # Remove old types
        for code in old_codes:
            if code in types:
                del types[code]
        
        # Add new type
        types[new_code] = {
            'description': new_description,
            'active': True
        }
        
        # Save
        return self.save_user_transaction_types(types)
    
    def get_active_types(self) -> Dict[str, str]:
        """Get active transaction types as code: description mapping."""
        types = self.get_user_transaction_types()
        return {
            code: info['description'] 
            for code, info in types.items() 
            if info.get('active', True)
        }
    
    def _create_user_types(self) -> Dict[str, Dict[str, any]]:
        """Create default transaction types for a new user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        default_types = self._get_default_transaction_types()
        
        # Save the default types for this user
        data = {
            'transaction_types': default_types,
            'user_email': user_email
        }
        if user_id:
            data['user_id'] = user_id
        
        try:
            self.supabase.table('user_transaction_types').insert(data).execute()
        except:
            # Might already exist, try upsert
            if user_id:
                self.supabase.table('user_transaction_types').upsert(data, on_conflict='user_id').execute()
        
        return default_types
    
    def _get_default_transaction_types(self) -> Dict[str, Dict[str, any]]:
        """Get default transaction types."""
        return {
            "BOR": {
                "description": "Broker of Record",
                "active": True
            },
            "CAN": {
                "description": "Cancellation",
                "active": True
            },
            "END": {
                "description": "Endorsement",
                "active": True
            },
            "NBS": {
                "description": "New Policy",
                "active": True
            },
            "NEW": {
                "description": "New Policy",
                "active": True
            },
            "PCH": {
                "description": "Policy Change",
                "active": True
            },
            "PMT": {
                "description": "Commission on Policy Payment",
                "active": True
            },
            "REI": {
                "description": "Policy Reinstatement",
                "active": True
            },
            "REWRITE": {
                "description": "Policy Rewrite",
                "active": True
            },
            "RWL": {
                "description": "Policy Renewal",
                "active": True
            },
            "XCL": {
                "description": "Policy Cancelled",
                "active": True
            }
        }

# Create a global instance
user_transaction_types = UserTransactionTypes()

# Backward compatible functions
def load_transaction_types() -> Dict[str, Dict[str, any]]:
    """Load transaction types for current user."""
    return user_transaction_types.get_user_transaction_types()

def save_transaction_types(types: Dict[str, Dict[str, any]]) -> bool:
    """Save transaction types for current user."""
    return user_transaction_types.save_user_transaction_types(types)

def get_active_transaction_types() -> Dict[str, str]:
    """Get active transaction types as code: description mapping."""
    return user_transaction_types.get_active_types()