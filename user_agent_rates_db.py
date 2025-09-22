"""
User-specific default agent commission rates using database storage.
Each user can set their own default rates for new business and renewals.
"""

import streamlit as st
from typing import Dict, Tuple
from database_utils import get_supabase_client

class UserDefaultAgentRates:
    """Handle user-specific default agent commission rates stored in database."""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self._rates_cache = None
        self._cache_user_id = None
    
    def get_user_rates(self) -> Dict[str, float]:
        """Get default agent commission rates for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        # Return default rates if no user
        if not user_id and not user_email:
            return self._get_default_rates()
        
        # Check cache
        if self._rates_cache and self._cache_user_id == user_id:
            return self._rates_cache
        
        try:
            # Try to get user's rates from database
            if user_id:
                response = self.supabase.table('user_default_agent_rates').select('*').eq('user_id', user_id).execute()
            else:
                response = self.supabase.table('user_default_agent_rates').select('*').eq('user_email', user_email).execute()
            
            if response.data and len(response.data) > 0:
                rates_data = response.data[0]
                result = {
                    'new_business': float(rates_data.get('new_business_rate', 50.0)),
                    'renewal': float(rates_data.get('renewal_rate', 25.0))
                }
                self._rates_cache = result
                self._cache_user_id = user_id
                return result
            
            # No rates found, create default for user
            return self._create_user_rates()
            
        except Exception as e:
            print(f"Error loading user default agent rates: {e}")
            return self._get_default_rates()
    
    def save_user_rates(self, new_business_rate: float, renewal_rate: float) -> bool:
        """Save default agent commission rates for the current user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        if not user_id and not user_email:
            return False
        
        # Validate rates
        if not (0 <= new_business_rate <= 100) or not (0 <= renewal_rate <= 100):
            return False
        
        try:
            # Prepare the data
            data = {
                'new_business_rate': new_business_rate,
                'renewal_rate': renewal_rate,
                'user_email': user_email
            }
            if user_id:
                data['user_id'] = user_id
            
            # Try to update existing record
            if user_id:
                response = self.supabase.table('user_default_agent_rates').upsert(data, on_conflict='user_id').execute()
            else:
                # Check if record exists
                check_response = self.supabase.table('user_default_agent_rates').select('id').eq('user_email', user_email).execute()
                if check_response.data:
                    # Update existing
                    response = self.supabase.table('user_default_agent_rates').update({
                        'new_business_rate': new_business_rate,
                        'renewal_rate': renewal_rate
                    }).eq('user_email', user_email).execute()
                else:
                    # Insert new
                    response = self.supabase.table('user_default_agent_rates').insert(data).execute()
            
            # Clear cache to force reload
            self._rates_cache = None
            self._cache_user_id = None
            
            return True
            
        except Exception as e:
            print(f"Error saving user default agent rates: {e}")
            return False
    
    def get_rates_tuple(self) -> Tuple[float, float]:
        """Get rates as a tuple (new_business, renewal)."""
        rates = self.get_user_rates()
        return (rates['new_business'], rates['renewal'])
    
    def _create_user_rates(self) -> Dict[str, float]:
        """Create default rates for a new user."""
        user_id = st.session_state.get('user_id')
        user_email = st.session_state.get('user_email', '').lower()
        
        default_rates = self._get_default_rates()
        
        # Save the default rates for this user
        data = {
            'new_business_rate': default_rates['new_business'],
            'renewal_rate': default_rates['renewal'],
            'user_email': user_email
        }
        if user_id:
            data['user_id'] = user_id
        
        try:
            self.supabase.table('user_default_agent_rates').insert(data).execute()
        except:
            # Might already exist, try upsert
            if user_id:
                self.supabase.table('user_default_agent_rates').upsert(data, on_conflict='user_id').execute()
        
        return default_rates
    
    def _get_default_rates(self) -> Dict[str, float]:
        """Get default rates."""
        return {
            'new_business': 50.0,
            'renewal': 25.0
        }

# Create a global instance
user_agent_rates = UserDefaultAgentRates()

# Backward compatible functions
def load_default_agent_rates() -> Dict[str, float]:
    """Load default agent commission rates for current user."""
    return user_agent_rates.get_user_rates()

def save_default_agent_rates(rates: Dict[str, float]) -> bool:
    """Save default agent commission rates for current user."""
    return user_agent_rates.save_user_rates(
        rates.get('new_business', 50.0),
        rates.get('renewal', 25.0)
    )

def get_default_rates() -> Tuple[float, float]:
    """Get default rates as tuple (new_business, renewal)."""
    return user_agent_rates.get_rates_tuple()