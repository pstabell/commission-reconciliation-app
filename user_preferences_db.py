"""
User-specific preferences using database storage instead of global JSON files.
Each user has their own preferences including color theme.
"""

import streamlit as st
import os
from typing import Dict, Optional
from database_utils import get_supabase_client

class UserPreferences:
    """Handle user-specific preferences stored in database."""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self._preferences_cache = None
        self._cache_user_id = None
    
    def get_user_preferences(self) -> Dict:
        """Get preferences for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        # Return default preferences if no user
        if not user_id and not user_email:
            return self._get_default_preferences()
        
        # Check cache
        if self._preferences_cache and self._cache_user_id == user_id:
            return self._preferences_cache
        
        try:
            # Try to get user's preferences from database
            if user_id:
                response = self.supabase.table('user_preferences').select('*').eq('user_id', user_id).execute()
            else:
                response = self.supabase.table('user_preferences').select('*').eq('user_email', user_email).execute()
            
            if response.data and len(response.data) > 0:
                prefs = response.data[0]
                result = {
                    'color_theme': prefs.get('color_theme', 'light'),
                    'other_preferences': prefs.get('other_preferences', {})
                }
                self._preferences_cache = result
                self._cache_user_id = user_id
                return result
            
            # No preferences found, create default for user
            return self._create_user_preferences()
            
        except Exception as e:
            print(f"Error loading user preferences: {e}")
            return self._get_default_preferences()
    
    def save_user_preferences(self, color_theme: str = None, other_preferences: dict = None) -> bool:
        """Save preferences for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        if not user_id and not user_email:
            return False
        
        try:
            # Get current preferences
            current_prefs = self.get_user_preferences()
            
            # Update only provided values
            if color_theme is not None:
                current_prefs['color_theme'] = color_theme
            if other_preferences is not None:
                current_prefs['other_preferences'] = other_preferences
            
            # Prepare the data
            data = {
                'color_theme': current_prefs['color_theme'],
                'other_preferences': current_prefs.get('other_preferences', {}),
                'user_email': user_email
            }
            if user_id:
                data['user_id'] = user_id
            
            # Try to update existing record
            if user_id:
                response = self.supabase.table('user_preferences').upsert(data, on_conflict='user_id').execute()
            else:
                # Check if record exists
                check_response = self.supabase.table('user_preferences').select('id').eq('user_email', user_email).execute()
                if check_response.data:
                    # Update existing
                    response = self.supabase.table('user_preferences').update(data).eq('user_email', user_email).execute()
                else:
                    # Insert new
                    response = self.supabase.table('user_preferences').insert(data).execute()
            
            # Clear cache to force reload
            self._preferences_cache = None
            self._cache_user_id = None
            
            return True
            
        except Exception as e:
            print(f"Error saving user preferences: {e}")
            return False
    
    def get_color_theme(self) -> str:
        """Get the user's color theme preference."""
        prefs = self.get_user_preferences()
        return prefs.get('color_theme', 'light')
    
    def set_color_theme(self, theme: str) -> bool:
        """Set the user's color theme preference."""
        return self.save_user_preferences(color_theme=theme)
    
    def _create_user_preferences(self) -> Dict:
        """Create default preferences for a new user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        default_prefs = self._get_default_preferences()
        
        # Save the default preferences for this user
        data = {
            'color_theme': default_prefs['color_theme'],
            'other_preferences': default_prefs['other_preferences'],
            'user_email': user_email
        }
        if user_id:
            data['user_id'] = user_id
        
        try:
            self.supabase.table('user_preferences').insert(data).execute()
        except:
            # Might already exist, try upsert
            if user_id:
                self.supabase.table('user_preferences').upsert(data, on_conflict='user_id').execute()
        
        return default_prefs
    
    def _get_default_preferences(self) -> Dict:
        """Get default preferences."""
        return {
            'color_theme': 'light',
            'other_preferences': {}
        }

# Create a global instance
user_preferences = UserPreferences()

# Backward compatible functions
def load_user_preferences() -> Dict:
    """Load preferences for current user."""
    return user_preferences.get_user_preferences()

def save_user_preferences(prefs_dict: Dict) -> bool:
    """Save preferences for current user."""
    color_theme = prefs_dict.get('color_theme')
    other_prefs = {k: v for k, v in prefs_dict.items() if k != 'color_theme'}
    return user_preferences.save_user_preferences(
        color_theme=color_theme, 
        other_preferences=other_prefs if other_prefs else None
    )

def get_color_theme() -> str:
    """Get user's color theme."""
    return user_preferences.get_color_theme()

def set_color_theme(theme: str) -> bool:
    """Set user's color theme."""
    return user_preferences.set_color_theme(theme)