"""
HubSpot Integration for Commission Intelligence Platform
Syncs client data and renewal opportunities with HubSpot CRM
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base_integration import BaseIntegration

class HubSpotIntegration(BaseIntegration):
    """HubSpot CRM integration."""
    
    def __init__(self, user_email: str, config: Dict[str, Any]):
        super().__init__(user_email, config)
        self.base_url = "https://api.hubapi.com"
        self.api_key = config.get('api_key')
        
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for HubSpot API."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test HubSpot API connection."""
        try:
            response = await self.make_request(
                "GET",
                f"{self.base_url}/account-info/v3/details",
                headers=self._get_auth_headers()
            )
            
            await self.log_activity("test_connection", "success", {"portal_id": response.get("portalId")})
            return {
                "success": True,
                "portal_id": response.get("portalId"),
                "account_type": response.get("accountType")
            }
        except Exception as e:
            await self.log_activity("test_connection", "error", {"error": str(e)})
            return {"success": False, "error": str(e)}
    
    async def sync_policies(self, since_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Sync contacts from HubSpot as potential policies."""
        policies = []
        
        try:
            # Search for contacts with insurance-related properties
            response = await self.make_request(
                "POST",
                f"{self.base_url}/crm/v3/objects/contacts/search",
                headers=self._get_auth_headers(),
                json={
                    "filterGroups": [{
                        "filters": [
                            {
                                "propertyName": "insurance_policy_number",
                                "operator": "HAS_PROPERTY"
                            }
                        ]
                    }],
                    "properties": [
                        "firstname", "lastname", "email",
                        "insurance_policy_number", "insurance_carrier",
                        "insurance_premium", "insurance_effective_date",
                        "insurance_expiration_date"
                    ],
                    "limit": 100
                }
            )
            
            # Map HubSpot contacts to policy format
            for contact in response.get("results", []):
                properties = contact.get("properties", {})
                
                policy = {
                    "policy_number": properties.get("insurance_policy_number"),
                    "customer": f"{properties.get('firstname', '')} {properties.get('lastname', '')}".strip(),
                    "email": properties.get("email"),
                    "carrier": properties.get("insurance_carrier"),
                    "premium": float(properties.get("insurance_premium", 0)),
                    "effective_date": properties.get("insurance_effective_date"),
                    "expiration_date": properties.get("insurance_expiration_date"),
                    "external_id": f"hubspot_{contact.get('id')}",
                    "api_source": "hubspot"
                }
                
                if policy["policy_number"]:  # Only include if has policy number
                    policies.append(policy)
            
            await self.log_activity("sync_policies", "success", {"count": len(policies)})
            
        except Exception as e:
            await self.log_activity("sync_policies", "error", {"error": str(e)})
            raise
        
        return policies
    
    async def push_commission(self, commission_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update HubSpot contact with commission data."""
        try:
            contact_id = commission_data.get("external_id", "").replace("hubspot_", "")
            
            # Update contact properties
            update_data = {
                "properties": {
                    "insurance_commission_earned": commission_data.get("commission"),
                    "insurance_commission_paid": commission_data.get("paid", False),
                    "insurance_last_commission_date": datetime.now().isoformat(),
                    "insurance_total_lifetime_commission": commission_data.get("lifetime_total", 0)
                }
            }
            
            response = await self.make_request(
                "PATCH",
                f"{self.base_url}/crm/v3/objects/contacts/{contact_id}",
                headers=self._get_auth_headers(),
                json=update_data
            )
            
            await self.log_activity(
                "push_commission",
                "success",
                {"contact_id": contact_id, "commission": commission_data.get("commission")}
            )
            
            return {"success": True, "external_id": f"hubspot_{contact_id}"}
            
        except Exception as e:
            await self.log_activity("push_commission", "error", {"error": str(e)})
            return {"success": False, "error": str(e)}
    
    async def create_renewal_task(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a task in HubSpot for policy renewal."""
        try:
            task_data = {
                "properties": {
                    "hs_task_subject": f"Policy Renewal: {policy_data.get('policy_number')}",
                    "hs_task_body": (
                        f"Policy {policy_data.get('policy_number')} for "
                        f"{policy_data.get('customer')} expires on "
                        f"{policy_data.get('expiration_date')}. "
                        f"Premium: ${policy_data.get('premium')}. "
                        f"Contact customer for renewal."
                    ),
                    "hs_task_priority": "HIGH",
                    "hs_task_status": "NOT_STARTED",
                    "hs_timestamp": policy_data.get("renewal_reminder_date")
                }
            }
            
            # Create task
            task_response = await self.make_request(
                "POST",
                f"{self.base_url}/crm/v3/objects/tasks",
                headers=self._get_auth_headers(),
                json=task_data
            )
            
            # Associate with contact if exists
            if policy_data.get("external_id"):
                contact_id = policy_data.get("external_id").replace("hubspot_", "")
                await self.make_request(
                    "PUT",
                    f"{self.base_url}/crm/v3/objects/tasks/{task_response['id']}/associations/contacts/{contact_id}/task_to_contact",
                    headers=self._get_auth_headers()
                )
            
            return {"success": True, "task_id": task_response.get("id")}
            
        except Exception as e:
            await self.log_activity("create_renewal_task", "error", {"error": str(e)})
            return {"success": False, "error": str(e)}