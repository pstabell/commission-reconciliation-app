"""
Commission Intelligence Platform Python SDK
Easy-to-use client for integrating with the Commission Tracker API
"""
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime, date
import json

class CommissionTrackerClient:
    """Python client for Commission Intelligence Platform API."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.commissiontracker.io"):
        """
        Initialize the Commission Tracker client.
        
        Args:
            api_key: Your API key from the Commission Tracker dashboard
            base_url: API base URL (defaults to production)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "CommissionTrackerSDK/Python/1.0"
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to API."""
        url = f"{self.base_url}{endpoint}"
        
        # Convert dates to ISO format
        if "json" in kwargs:
            kwargs["json"] = self._serialize_dates(kwargs["json"])
        
        response = self.session.request(method, url, **kwargs)
        
        if response.status_code >= 400:
            error_msg = f"API Error {response.status_code}: {response.text}"
            raise CommissionTrackerError(error_msg, response.status_code)
        
        return response.json()
    
    def _serialize_dates(self, obj: Any) -> Any:
        """Recursively convert date objects to ISO format."""
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: self._serialize_dates(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_dates(item) for item in obj]
        return obj
    
    # Policy Management
    def list_policies(self, page: int = 1, per_page: int = 20, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all policies."""
        params = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        
        return self._request("GET", "/v1/policies", params=params)
    
    def get_policy(self, policy_id: str) -> Dict[str, Any]:
        """Get a specific policy."""
        return self._request("GET", f"/v1/policies/{policy_id}")
    
    def create_policy(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new policy."""
        return self._request("POST", "/v1/policies", json=policy_data)
    
    def update_policy(self, policy_id: str, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing policy."""
        return self._request("PUT", f"/v1/policies/{policy_id}", json=policy_data)
    
    def delete_policy(self, policy_id: str) -> Dict[str, Any]:
        """Delete a policy."""
        return self._request("DELETE", f"/v1/policies/{policy_id}")
    
    # Commission Calculations
    def calculate_commission(self, premium: float, rate: float, 
                           policy_type: str = "AUTO", 
                           transaction_type: str = "NEW") -> Dict[str, Any]:
        """Calculate commission for given parameters."""
        data = {
            "premium": premium,
            "commission_rate": rate,
            "policy_type": policy_type,
            "transaction_type": transaction_type
        }
        return self._request("POST", "/v1/commissions/calculate", json=data)
    
    def reconcile_commissions(self, statement_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Reconcile commission statement."""
        return self._request("POST", "/v1/commissions/reconcile", json={"statements": statement_data})
    
    def get_pending_commissions(self) -> List[Dict[str, Any]]:
        """Get all pending commissions."""
        return self._request("GET", "/v1/commissions/pending")
    
    # Analytics
    def get_analytics_summary(self, start_date: Optional[date] = None, 
                            end_date: Optional[date] = None) -> Dict[str, Any]:
        """Get analytics summary for date range."""
        params = {}
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
        
        return self._request("GET", "/v1/analytics/summary", params=params)
    
    def get_agent_performance(self, agent_id: str, period: str = "month") -> Dict[str, Any]:
        """Get performance metrics for specific agent."""
        return self._request("GET", f"/v1/analytics/agent/{agent_id}", params={"period": period})
    
    # Webhooks
    def create_webhook(self, url: str, events: List[str], secret: Optional[str] = None) -> Dict[str, Any]:
        """Create a new webhook."""
        data = {"url": url, "events": events}
        if secret:
            data["secret"] = secret
        
        return self._request("POST", "/v1/webhooks", json=data)
    
    def list_webhooks(self) -> List[Dict[str, Any]]:
        """List all webhooks."""
        return self._request("GET", "/v1/webhooks")
    
    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete a webhook."""
        return self._request("DELETE", f"/v1/webhooks/{webhook_id}")
    
    def test_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Send test event to webhook."""
        return self._request("POST", f"/v1/webhooks/{webhook_id}/test")

class CommissionTrackerError(Exception):
    """Commission Tracker API error."""
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

# Example usage
if __name__ == "__main__":
    # Initialize client
    client = CommissionTrackerClient("your_api_key_here")
    
    # List policies
    policies = client.list_policies()
    print(f"Found {len(policies)} policies")
    
    # Create a policy
    new_policy = client.create_policy({
        "policy_number": "AUTO-123456",
        "customer": "John Doe",
        "effective_date": date(2025, 1, 1),
        "premium": 1200.00,
        "commission_rate": 12.0
    })
    print(f"Created policy: {new_policy['id']}")
    
    # Calculate commission
    commission = client.calculate_commission(
        premium=1200.00,
        rate=12.0,
        policy_type="AUTO",
        transaction_type="NEW"
    )
    print(f"Commission: ${commission['agent_commission']}")