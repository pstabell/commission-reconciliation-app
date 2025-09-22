"""
User-specific PRL (Producer Revenue List) templates using database storage.
These templates allow users to save and reuse column configurations for their reports.
"""

import streamlit as st
from typing import Dict, List, Optional, Any
from database_utils import get_supabase_client
import json
from datetime import datetime

class UserPRLTemplates:
    """Handle user-specific PRL templates stored in database."""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self._templates_cache = None
        self._cache_user_id = None
    
    def get_user_templates(self) -> Dict[str, Any]:
        """Get PRL templates for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        # Return empty dict if no user
        if not user_id and not user_email:
            return {}
        
        # Check cache
        if self._templates_cache and self._cache_user_id == user_id:
            return self._templates_cache
        
        try:
            # Try to get user's templates from database
            if user_id:
                response = self.supabase.table('user_prl_templates').select('*').eq('user_id', user_id).execute()
            else:
                response = self.supabase.table('user_prl_templates').select('*').eq('user_email', user_email).execute()
            
            if response.data:
                # Convert list of template records to dict format
                templates = {}
                for template in response.data:
                    template_name = template.get('template_name')
                    if template_name:
                        templates[template_name] = {
                            'columns': template.get('columns', []),
                            'created': template.get('created_at', ''),
                            'view_mode': template.get('view_mode', 'all')
                        }
                
                self._templates_cache = templates
                self._cache_user_id = user_id
                return templates
            
            return {}
            
        except Exception as e:
            print(f"Error loading user PRL templates: {e}")
            return {}
    
    def save_template(self, template_name: str, columns: List[str], view_mode: str = 'all') -> bool:
        """Save a new PRL template for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        if not user_id and not user_email:
            return False
        
        try:
            # Prepare the data
            data = {
                'template_name': template_name,
                'columns': columns,
                'view_mode': view_mode,
                'user_email': user_email,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            if user_id:
                data['user_id'] = user_id
            
            # Insert new template
            response = self.supabase.table('user_prl_templates').insert(data).execute()
            
            # Clear cache to force reload
            self._templates_cache = None
            
            return True
            
        except Exception as e:
            print(f"Error saving PRL template: {e}")
            return False
    
    def update_template(self, template_name: str, columns: List[str], view_mode: str = 'all') -> bool:
        """Update an existing PRL template for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        if not user_id and not user_email:
            return False
        
        try:
            # Build the update query
            update_data = {
                'columns': columns,
                'view_mode': view_mode,
                'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Update existing template
            if user_id:
                response = self.supabase.table('user_prl_templates').update(update_data).eq('user_id', user_id).eq('template_name', template_name).execute()
            else:
                response = self.supabase.table('user_prl_templates').update(update_data).eq('user_email', user_email).eq('template_name', template_name).execute()
            
            # Clear cache to force reload
            self._templates_cache = None
            
            return True
            
        except Exception as e:
            print(f"Error updating PRL template: {e}")
            return False
    
    def delete_template(self, template_name: str) -> bool:
        """Delete a PRL template for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        if not user_id and not user_email:
            return False
        
        try:
            # Delete the template
            if user_id:
                response = self.supabase.table('user_prl_templates').delete().eq('user_id', user_id).eq('template_name', template_name).execute()
            else:
                response = self.supabase.table('user_prl_templates').delete().eq('user_email', user_email).eq('template_name', template_name).execute()
            
            # Clear cache to force reload
            self._templates_cache = None
            
            return True
            
        except Exception as e:
            print(f"Error deleting PRL template: {e}")
            return False
    
    def template_exists(self, template_name: str) -> bool:
        """Check if a template with the given name already exists for the user."""
        templates = self.get_user_templates()
        return template_name in templates
    
    def get_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific template by name."""
        templates = self.get_user_templates()
        return templates.get(template_name)
    
    def clear_cache(self):
        """Clear the templates cache."""
        self._templates_cache = None
        self._cache_user_id = None

# Create a global instance
user_prl_templates = UserPRLTemplates()

# Convenience functions
def get_user_prl_templates() -> Dict[str, Any]:
    """Get all PRL templates for the current user."""
    return user_prl_templates.get_user_templates()

def save_prl_template(template_name: str, columns: List[str], view_mode: str = 'all') -> bool:
    """Save a new PRL template."""
    return user_prl_templates.save_template(template_name, columns, view_mode)

def update_prl_template(template_name: str, columns: List[str], view_mode: str = 'all') -> bool:
    """Update an existing PRL template."""
    return user_prl_templates.update_template(template_name, columns, view_mode)

def delete_prl_template(template_name: str) -> bool:
    """Delete a PRL template."""
    return user_prl_templates.delete_template(template_name)

def prl_template_exists(template_name: str) -> bool:
    """Check if a PRL template exists."""
    return user_prl_templates.template_exists(template_name)

def get_prl_template(template_name: str) -> Optional[Dict[str, Any]]:
    """Get a specific PRL template."""
    return user_prl_templates.get_template(template_name)