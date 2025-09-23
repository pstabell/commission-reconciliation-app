"""
Database utilities for user-specific modules.
Provides access to Supabase client with proper environment handling.
"""

import os
from supabase import create_client, Client


def get_supabase_client() -> Client:
    """Get cached Supabase client based on environment."""
    app_mode = os.getenv("APP_ENVIRONMENT")
    
    if app_mode == "PRODUCTION":
        # Use production database credentials
        url = os.getenv("PRODUCTION_SUPABASE_URL", os.getenv("SUPABASE_URL"))
        # Try service role key first (bypasses RLS), fall back to anon key
        # Also check for shorter env var names in case of Render issues
        service_key = os.getenv("PRODUCTION_SUPABASE_SERVICE_ROLE_KEY") or os.getenv("PROD_SERVICE_KEY")
        anon_key = os.getenv("PRODUCTION_SUPABASE_ANON_KEY", os.getenv("SUPABASE_ANON_KEY"))
        key = service_key or anon_key
        
        # Debug logging
        if service_key:
            print("Using PRODUCTION service role key (RLS bypassed)")
        else:
            print("Using PRODUCTION anon key (RLS enforced)")
    else:
        # Use personal database credentials (default)
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", os.getenv("SUPABASE_ANON_KEY"))
    
    if not url or not key:
        raise ValueError("Supabase URL and key must be set in environment variables")
    
    # Create client instance
    supabase: Client = create_client(url, key)
    return supabase