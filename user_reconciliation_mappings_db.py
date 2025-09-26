"""
User-specific reconciliation column mappings using database storage.
These mappings are used during CSV/Excel imports on the reconciliation page to map
statement columns to system fields.
"""

import streamlit as st
from typing import Dict, Optional, List
from database_utils import get_supabase_client
import json
from datetime import datetime

class UserReconciliationMappings:
    """Handle user-specific reconciliation column mappings stored in database."""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self._mappings_cache = None
        self._cache_user_id = None
    
    def get_user_reconciliation_mappings(self) -> Dict[str, Dict]:
        """Get all reconciliation column mappings for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        # Return empty dict if no user
        if not user_id and not user_email:
            return {}
        
        # Check cache
        if self._mappings_cache and self._cache_user_id == user_id:
            return self._mappings_cache
        
        try:
            # Try to get user's mappings from database
            if user_id:
                response = self.supabase.table('user_reconciliation_mappings').select('*').eq('user_id', user_id).execute()
            else:
                response = self.supabase.table('user_reconciliation_mappings').select('*').eq('user_email', user_email).execute()
            
            if response.data:
                # Convert list of mappings to dict keyed by mapping_name
                result = {}
                for mapping in response.data:
                    mapping_name = mapping.get('mapping_name')
                    if mapping_name:
                        result[mapping_name] = {
                            'mapping': mapping.get('column_mappings', {}),
                            'created': mapping.get('created_at', ''),
                            'field_count': len(mapping.get('column_mappings', {}))
                        }
                
                self._mappings_cache = result
                self._cache_user_id = user_id
                return result
            
            return {}
            
        except Exception as e:
            print(f"Error loading user reconciliation mappings: {e}")
            return {}
    
    def save_reconciliation_mapping(self, mapping_name: str, column_mappings: Dict[str, str]) -> bool:
        """Save or update a reconciliation column mapping for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        if not user_id and not user_email:
            return False
        
        try:
            # Prepare the data
            data = {
                'mapping_name': mapping_name,
                'column_mappings': column_mappings,
                'user_email': user_email
            }
            if user_id:
                data['user_id'] = user_id
            
            # Check if this mapping already exists
            if user_id:
                existing = self.supabase.table('user_reconciliation_mappings').select('id').eq('user_id', user_id).eq('mapping_name', mapping_name).execute()
            else:
                existing = self.supabase.table('user_reconciliation_mappings').select('id').eq('user_email', user_email).eq('mapping_name', mapping_name).execute()
            
            if existing.data:
                # Update existing
                if user_id:
                    response = self.supabase.table('user_reconciliation_mappings').update({
                        'column_mappings': column_mappings
                    }).eq('user_id', user_id).eq('mapping_name', mapping_name).execute()
                else:
                    response = self.supabase.table('user_reconciliation_mappings').update({
                        'column_mappings': column_mappings
                    }).eq('user_email', user_email).eq('mapping_name', mapping_name).execute()
            else:
                # Insert new
                response = self.supabase.table('user_reconciliation_mappings').insert(data).execute()
            
            # Clear cache to force reload
            self._mappings_cache = None
            
            return True
            
        except Exception as e:
            print(f"Error saving user reconciliation mapping: {e}")
            return False
    
    def delete_reconciliation_mapping(self, mapping_name: str) -> bool:
        """Delete a reconciliation mapping for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        if not user_id and not user_email:
            return False
        
        try:
            if user_id:
                response = self.supabase.table('user_reconciliation_mappings').delete().eq('user_id', user_id).eq('mapping_name', mapping_name).execute()
            else:
                response = self.supabase.table('user_reconciliation_mappings').delete().eq('user_email', user_email).eq('mapping_name', mapping_name).execute()
            
            # Clear cache
            self._mappings_cache = None
            
            return True
            
        except Exception as e:
            print(f"Error deleting reconciliation mapping: {e}")
            return False
    
    def get_mapping_names(self) -> List[str]:
        """Get list of mapping names for current user."""
        mappings = self.get_user_reconciliation_mappings()
        return list(mappings.keys())

# Create a global instance
user_reconciliation_mappings = UserReconciliationMappings()

# Backward compatible functions that replace the session state approach
def load_saved_column_mappings() -> Dict[str, Dict]:
    """Load saved reconciliation column mappings from database."""
    return user_reconciliation_mappings.get_user_reconciliation_mappings()

def save_column_mappings_to_file(mappings: Dict[str, Dict]) -> bool:
    """This function is deprecated - use save_reconciliation_column_mapping instead."""
    # Convert the old format to new format and save each mapping
    try:
        for mapping_name, mapping_data in mappings.items():
            if isinstance(mapping_data, dict) and 'mapping' in mapping_data:
                user_reconciliation_mappings.save_reconciliation_mapping(
                    mapping_name, 
                    mapping_data['mapping']
                )
        return True
    except Exception as e:
        print(f"Error in compatibility save: {e}")
        return False

def save_reconciliation_column_mapping(mapping_name: str, column_mappings: Dict[str, str]) -> bool:
    """Save a reconciliation column mapping to database."""
    return user_reconciliation_mappings.save_reconciliation_mapping(mapping_name, column_mappings)

def delete_reconciliation_column_mapping(mapping_name: str) -> bool:
    """Delete a reconciliation column mapping from database."""
    return user_reconciliation_mappings.delete_reconciliation_mapping(mapping_name)