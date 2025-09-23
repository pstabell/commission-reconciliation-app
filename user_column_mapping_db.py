"""
User-specific column mapping using database storage instead of global JSON files.
Each user has their own column display preferences.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Optional
import json
from database_utils import get_supabase_client

class UserColumnMapper:
    """Handle user-specific column mappings stored in database."""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self._mapping_cache = None
        self._cache_user_id = None
    
    def get_user_mapping(self) -> Dict[str, str]:
        """Get column mappings for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        # Return default mapping if no user
        if not user_id and not user_email:
            return self._get_default_mapping()
        
        # Check cache
        if self._mapping_cache and self._cache_user_id == user_id:
            return self._mapping_cache
        
        try:
            # Try to get user's mapping from database
            if user_id:
                response = self.supabase.table('user_column_mappings').select('column_mappings').eq('user_id', user_id).execute()
            else:
                response = self.supabase.table('user_column_mappings').select('column_mappings').eq('user_email', user_email).execute()
            
            if response.data and len(response.data) > 0:
                mapping = response.data[0].get('column_mappings', {})
                if mapping:
                    self._mapping_cache = mapping
                    self._cache_user_id = user_id
                    return mapping
            
            # No mapping found, create default for user
            return self._create_user_mapping()
            
        except Exception as e:
            print(f"Error loading user column mapping: {e}")
            return self._get_default_mapping()
    
    def save_user_mapping(self, new_mapping: Dict[str, str]) -> bool:
        """Save column mappings for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        if not user_id and not user_email:
            return False
        
        try:
            # Prepare the data
            data = {
                'column_mappings': new_mapping,
                'user_email': user_email
            }
            if user_id:
                data['user_id'] = user_id
            
            # Try to update existing record
            if user_id:
                response = self.supabase.table('user_column_mappings').upsert(data, on_conflict='user_id').execute()
            else:
                # Check if record exists
                check_response = self.supabase.table('user_column_mappings').select('id').eq('user_email', user_email).execute()
                if check_response.data:
                    # Update existing
                    response = self.supabase.table('user_column_mappings').update({'column_mappings': new_mapping}).eq('user_email', user_email).execute()
                else:
                    # Insert new
                    response = self.supabase.table('user_column_mappings').insert(data).execute()
            
            # Clear cache to force reload
            self._mapping_cache = None
            self._cache_user_id = None
            
            return True
            
        except Exception as e:
            print(f"Error saving user column mapping: {e}")
            return False
    
    def get_mapped_column(self, db_column: str) -> str:
        """Get the display name for a database column."""
        mapping = self.get_user_mapping()
        return mapping.get(db_column, db_column)
    
    def get_reverse_mapping(self) -> Dict[str, str]:
        """Get display name to database column mapping."""
        mapping = self.get_user_mapping()
        return {v: k for k, v in mapping.items()}
    
    def _create_user_mapping(self) -> Dict[str, str]:
        """Create default mapping for a new user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        default_mapping = self._get_default_mapping()
        
        # Save the default mapping for this user
        data = {
            'column_mappings': default_mapping,
            'user_email': user_email
        }
        if user_id:
            data['user_id'] = user_id
        
        try:
            self.supabase.table('user_column_mappings').insert(data).execute()
        except:
            # Might already exist, try upsert
            if user_id:
                self.supabase.table('user_column_mappings').upsert(data, on_conflict='user_id').execute()
        
        return default_mapping
    
    def _get_default_mapping(self) -> Dict[str, str]:
        """Get default column mappings."""
        return {
            "Transaction ID": "Transaction ID",
            "Client ID": "Client ID",
            "Customer": "Customer",
            "Prior Policy Number": "Prior Policy Number",
            "Policy Number": "Policy Number",
            "Policy Type": "Policy Type",
            "Policy Term": "Policy Term",
            "Policy Origination Date": "Policy Origination Date",
            "Carrier Name": "Carrier Name",
            "MGA": "MGA",
            "Transaction Type": "Transaction Type",
            "Effective Date": "Effective Date",
            "X-DATE": "X-DATE",
            "Premium Sold": "Premium Sold",
            "Policy Gross Comm %": "Policy Gross Comm %",
            "Agency Estimated Comm/Revenue (CRM)": "Agency Estimated Comm/Revenue (CRM)",
            "Agent Comm %": "Agent Comm %",
            "Agent Estimated Comm $": "Agent Estimated Comm $",
            "Agency Comm Received (STMT)": "Agency Comm Received (STMT)",
            "Agent Paid Amount (STMT)": "Agent Paid Amount (STMT)",
            "Policy Balance Due": "Policy Balance Due",
            "STMT DATE": "STMT DATE",
            "NOTES": "NOTES",
            "user_email": "User Email",
            "user_id": "User ID",
            "created_at": "Created At",
            "updated_at": "Updated At",
            "_id": "Internal ID"
        }

# Create a global instance for backward compatibility
user_column_mapper = UserColumnMapper()

# Backward compatible functions
def get_mapped_column(db_column: str) -> str:
    """Get display name for a database column."""
    return user_column_mapper.get_mapped_column(db_column)

def get_reverse_mapping() -> Dict[str, str]:
    """Get display name to database column mapping."""
    return user_column_mapper.get_reverse_mapping()

def save_column_mapping(new_mapping: Dict[str, str]) -> bool:
    """Save column mapping for current user."""
    return user_column_mapper.save_user_mapping(new_mapping)

def get_ui_field_name(db_column: str) -> str:
    """Get UI field name for a database column (alias for get_mapped_column)."""
    return user_column_mapper.get_mapped_column(db_column)

def is_calculated_field(ui_field: str) -> bool:
    """Check if a field is calculated/virtual."""
    # List of calculated fields that don't exist in database
    calculated_fields = {
        "Policy Balance Due",
        "Agent Estimated Comm $",
        "Agency Estimated Comm/Revenue (CRM)",
        "Commissionable Premium",
        "Broker Fee Agent Comm",
        "Total Agent Comm"
    }
    return ui_field in calculated_fields

def safe_column_reference(df, ui_field: str, default_value=None, return_series: bool = True):
    """
    Safely reference a column in a DataFrame using UI field name.
    
    Args:
        df: DataFrame to reference
        ui_field: UI field name 
        default_value: Value to return/fill if column not found
        return_series: If True, return Series; if False, return values
        
    Returns:
        Series or values from the mapped column, or default_value if not found
    """
    import pandas as pd
    
    # Get the database column name
    mapping = user_column_mapper.get_user_mapping()
    db_col = mapping.get(ui_field, ui_field)
    
    if db_col and db_col in df.columns:
        if return_series:
            return df[db_col]
        else:
            return df[db_col].values
    else:
        if return_series:
            return pd.Series([default_value] * len(df), index=df.index)
        else:
            return [default_value] * len(df)