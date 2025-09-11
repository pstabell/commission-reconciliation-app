"""
Base Integration Class for Commission Intelligence Platform
All integrations inherit from this base class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import aiohttp
import asyncio
from datetime import datetime
import json
import os
import sys
sys.path.append('../..')
from commission_app import get_supabase_client

class BaseIntegration(ABC):
    """Abstract base class for all integrations."""
    
    def __init__(self, user_email: str, config: Dict[str, Any]):
        self.user_email = user_email
        self.config = config
        self.supabase = get_supabase_client()
        self.name = self.__class__.__name__
        
    @abstractmethod
    async def test_connection(self) -> Dict[str, Any]:
        """Test if the integration connection is working."""
        pass
    
    @abstractmethod
    async def sync_policies(self, since_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Sync policies from the external system."""
        pass
    
    @abstractmethod
    async def push_commission(self, commission_data: Dict[str, Any]) -> Dict[str, Any]:
        """Push commission data to the external system."""
        pass
    
    async def log_activity(self, action: str, status: str, details: Dict[str, Any] = None):
        """Log integration activity."""
        log_data = {
            'user_email': self.user_email,
            'integration': self.name,
            'action': action,
            'status': status,
            'details': json.dumps(details or {}),
            'timestamp': datetime.now().isoformat()
        }
        
        # In production, this would write to an integration_logs table
        print(f"[{self.name}] {action}: {status}")
        
    def map_fields(self, source_data: Dict[str, Any], field_mapping: Dict[str, str]) -> Dict[str, Any]:
        """Map fields from source to destination format."""
        mapped_data = {}
        for source_field, dest_field in field_mapping.items():
            if source_field in source_data:
                mapped_data[dest_field] = source_data[source_field]
        return mapped_data
    
    async def make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with error handling."""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, url, **kwargs) as response:
                    data = await response.json()
                    if response.status >= 400:
                        raise Exception(f"API Error: {response.status} - {data}")
                    return data
            except Exception as e:
                await self.log_activity(f"{method} {url}", "error", {"error": str(e)})
                raise