"""
User-specific mappings for policy types and transaction types using database storage.
These mappings are used during CSV imports and reconciliation to standardize data.
"""

import streamlit as st
from typing import Dict, Optional
from database_utils import get_supabase_client
import json

class UserMappings:
    """Handle user-specific type mappings stored in database."""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self._policy_mappings_cache = None
        self._transaction_mappings_cache = None
        self._cache_user_id = None
    
    # Policy Type Mappings
    def get_user_policy_type_mappings(self) -> Dict[str, str]:
        """Get policy type mappings for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        # Return default mappings if no user
        if not user_id and not user_email:
            return self._get_default_policy_mappings()
        
        # Check cache
        if self._policy_mappings_cache and self._cache_user_id == user_id:
            return self._policy_mappings_cache
        
        try:
            # Try to get user's mappings from database
            if user_id:
                response = self.supabase.table('user_policy_type_mappings').select('*').eq('user_id', user_id).execute()
            else:
                response = self.supabase.table('user_policy_type_mappings').select('*').eq('user_email', user_email).execute()
            
            if response.data and len(response.data) > 0:
                mappings_data = response.data[0]
                result = mappings_data.get('mappings', {})
                self._policy_mappings_cache = result
                self._cache_user_id = user_id
                return result
            
            # No mappings found, create default for user
            return self._create_user_policy_mappings()
            
        except Exception as e:
            print(f"Error loading user policy type mappings: {e}")
            return self._get_default_policy_mappings()
    
    def save_user_policy_type_mappings(self, mappings: Dict[str, str]) -> bool:
        """Save policy type mappings for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        if not user_id and not user_email:
            return False
        
        try:
            # Prepare the data
            data = {
                'mappings': mappings,
                'user_email': user_email
            }
            if user_id:
                data['user_id'] = user_id
            
            # Try to update existing record
            if user_id:
                response = self.supabase.table('user_policy_type_mappings').upsert(data, on_conflict='user_id').execute()
            else:
                # Check if record exists
                check_response = self.supabase.table('user_policy_type_mappings').select('id').eq('user_email', user_email).execute()
                if check_response.data:
                    # Update existing
                    response = self.supabase.table('user_policy_type_mappings').update({
                        'mappings': mappings
                    }).eq('user_email', user_email).execute()
                else:
                    # Insert new
                    response = self.supabase.table('user_policy_type_mappings').insert(data).execute()
            
            # Clear cache to force reload
            self._policy_mappings_cache = None
            
            return True
            
        except Exception as e:
            print(f"Error saving user policy type mappings: {e}")
            return False
    
    # Transaction Type Mappings
    def get_user_transaction_type_mappings(self) -> Dict[str, str]:
        """Get transaction type mappings for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        # Return default mappings if no user
        if not user_id and not user_email:
            return self._get_default_transaction_mappings()
        
        # Check cache
        if self._transaction_mappings_cache and self._cache_user_id == user_id:
            return self._transaction_mappings_cache
        
        try:
            # Try to get user's mappings from database
            if user_id:
                response = self.supabase.table('user_transaction_type_mappings').select('*').eq('user_id', user_id).execute()
            else:
                response = self.supabase.table('user_transaction_type_mappings').select('*').eq('user_email', user_email).execute()
            
            if response.data and len(response.data) > 0:
                mappings_data = response.data[0]
                result = mappings_data.get('mappings', {})
                self._transaction_mappings_cache = result
                self._cache_user_id = user_id
                return result
            
            # No mappings found, create default for user
            return self._create_user_transaction_mappings()
            
        except Exception as e:
            print(f"Error loading user transaction type mappings: {e}")
            return self._get_default_transaction_mappings()
    
    def save_user_transaction_type_mappings(self, mappings: Dict[str, str]) -> bool:
        """Save transaction type mappings for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        if not user_id and not user_email:
            return False
        
        try:
            # Prepare the data
            data = {
                'mappings': mappings,
                'user_email': user_email
            }
            if user_id:
                data['user_id'] = user_id
            
            # Try to update existing record
            if user_id:
                response = self.supabase.table('user_transaction_type_mappings').upsert(data, on_conflict='user_id').execute()
            else:
                # Check if record exists
                check_response = self.supabase.table('user_transaction_type_mappings').select('id').eq('user_email', user_email).execute()
                if check_response.data:
                    # Update existing
                    response = self.supabase.table('user_transaction_type_mappings').update({
                        'mappings': mappings
                    }).eq('user_email', user_email).execute()
                else:
                    # Insert new
                    response = self.supabase.table('user_transaction_type_mappings').insert(data).execute()
            
            # Clear cache to force reload
            self._transaction_mappings_cache = None
            
            return True
            
        except Exception as e:
            print(f"Error saving user transaction type mappings: {e}")
            return False
    
    # Helper methods
    def add_policy_mapping(self, from_type: str, to_type: str) -> bool:
        """Add a single policy type mapping."""
        mappings = self.get_user_policy_type_mappings()
        mappings[from_type] = to_type
        return self.save_user_policy_type_mappings(mappings)
    
    def add_transaction_mapping(self, from_type: str, to_type: str) -> bool:
        """Add a single transaction type mapping."""
        mappings = self.get_user_transaction_type_mappings()
        mappings[from_type] = to_type
        return self.save_user_transaction_type_mappings(mappings)
    
    def _create_user_policy_mappings(self) -> Dict[str, str]:
        """Create default policy type mappings for a new user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        default_mappings = self._get_default_policy_mappings()
        
        # Save the default mappings for this user
        data = {
            'mappings': default_mappings,
            'user_email': user_email
        }
        if user_id:
            data['user_id'] = user_id
        
        try:
            self.supabase.table('user_policy_type_mappings').insert(data).execute()
        except:
            # Might already exist, try upsert
            if user_id:
                self.supabase.table('user_policy_type_mappings').upsert(data, on_conflict='user_id').execute()
        
        return default_mappings
    
    def _create_user_transaction_mappings(self) -> Dict[str, str]:
        """Create default transaction type mappings for a new user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        default_mappings = self._get_default_transaction_mappings()
        
        # Save the default mappings for this user
        data = {
            'mappings': default_mappings,
            'user_email': user_email
        }
        if user_id:
            data['user_id'] = user_id
        
        try:
            self.supabase.table('user_transaction_type_mappings').insert(data).execute()
        except:
            # Might already exist, try upsert
            if user_id:
                self.supabase.table('user_transaction_type_mappings').upsert(data, on_conflict='user_id').execute()
        
        return default_mappings
    
    def _get_default_policy_mappings(self) -> Dict[str, str]:
        """Get default policy type mappings."""
        return {
            "HO3": "HOME",
            "HOME": "HOME",
            "PAWN": "PROP-C",
            "AUTOP": "AUTOP",
            "AUTOB": "AUTOB",
            "PL": "PL",
            "DFIRE": "DFIRE",
            "WORK": "WC",
            "CONDP": "CONDO",
            "FLODC": "FLOOD",
            "FLOOD": "FLOOD",
            "BOAT": "BOAT",
            "GL": "GL",
            "WC": "WC"
        }
    
    def _get_default_transaction_mappings(self) -> Dict[str, str]:
        """Get default transaction type mappings."""
        return {
            "STL": "PMT",
            "NBS": "NEW",
            "XLC": "CAN",
            "RWL": "RWL",
            "PCH": "END"
        }

# Create a global instance
user_mappings = UserMappings()

# Backward compatible functions
def load_policy_type_mappings() -> Dict[str, str]:
    """Load policy type mappings for current user."""
    return user_mappings.get_user_policy_type_mappings()

def save_policy_type_mappings(mappings: Dict[str, str]) -> bool:
    """Save policy type mappings for current user."""
    return user_mappings.save_user_policy_type_mappings(mappings)

def load_transaction_type_mappings() -> Dict[str, str]:
    """Load transaction type mappings for current user."""
    return user_mappings.get_user_transaction_type_mappings()

def save_transaction_type_mappings(mappings: Dict[str, str]) -> bool:
    """Save transaction type mappings for current user."""
    return user_mappings.save_user_transaction_type_mappings(mappings)