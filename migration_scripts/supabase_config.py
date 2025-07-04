# Supabase Configuration File
# Sales Commission Tracker - Cloud Database Configuration
# =======================================================

import os
from supabase import create_client, Client
from typing import Optional
import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseConfig:
    """
    Supabase configuration and connection management
    """
    
    def __init__(self):
        self.url: Optional[str] = None
        self.key: Optional[str] = None
        self.client: Optional[Client] = None
        self._load_config()
    
    def _load_config(self):
        """Load Supabase configuration from environment variables or Streamlit secrets"""
        try:
            # Try to load from Streamlit secrets first (for cloud deployment)
            if hasattr(st, 'secrets') and 'supabase' in st.secrets:
                self.url = st.secrets.supabase.url
                self.key = st.secrets.supabase.anon_key
                logger.info("Loaded Supabase config from Streamlit secrets")
            
            # Fallback to environment variables (for local development)
            elif 'SUPABASE_URL' in os.environ and 'SUPABASE_ANON_KEY' in os.environ:
                self.url = os.environ.get('SUPABASE_URL')
                self.key = os.environ.get('SUPABASE_ANON_KEY')
                logger.info("Loaded Supabase config from environment variables")
            
            else:
                logger.warning("Supabase configuration not found in secrets or environment variables")
                self.url = None
                self.key = None
                
        except Exception as e:
            logger.error(f"Error loading Supabase configuration: {e}")
            self.url = None
            self.key = None
    
    def get_client(self) -> Optional[Client]:
        """
        Get authenticated Supabase client
        Returns None if configuration is missing
        """
        if not self.url or not self.key:
            logger.error("Supabase URL or API key is missing")
            return None
        
        try:
            if not self.client:
                self.client = create_client(self.url, self.key)
                logger.info("Supabase client created successfully")
            return self.client
        
        except Exception as e:
            logger.error(f"Failed to create Supabase client: {e}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test the Supabase connection
        Returns True if connection is successful, False otherwise
        """
        try:
            client = self.get_client()
            if not client:
                return False
            
            # Test with a simple query
            response = client.table('policies').select('count', count='exact').execute()
            logger.info(f"Connection test successful. Policies table count: {response.count}")
            return True
            
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def is_configured(self) -> bool:
        """Check if Supabase is properly configured"""
        return self.url is not None and self.key is not None

# Global instance
supabase_config = SupabaseConfig()

def get_supabase_client() -> Optional[Client]:
    """
    Convenience function to get Supabase client
    """
    return supabase_config.get_client()

def is_supabase_available() -> bool:
    """
    Check if Supabase is configured and available
    """
    return supabase_config.is_configured() and supabase_config.test_connection()
