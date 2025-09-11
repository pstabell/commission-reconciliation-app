"""
EZLynx Integration for Commission Intelligence Platform
Handles policy sync and commission data exchange with EZLynx
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import base64
from .base_integration import BaseIntegration

class EZLynxIntegration(BaseIntegration):
    """EZLynx API integration."""
    
    def __init__(self, user_email: str, config: Dict[str, Any]):
        super().__init__(user_email, config)
        self.base_url = "https://api.ezlynx.com/v2"
        self.api_key = config.get('api_key')
        self.username = config.get('username')
        self.password = config.get('password')
        
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for EZLynx API."""
        # EZLynx uses basic auth
        credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
        return {
            "Authorization": f"Basic {credentials}",
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test EZLynx API connection."""
        try:
            # Test with a simple API call
            response = await self.make_request(
                "GET",
                f"{self.base_url}/agencies/current",
                headers=self._get_auth_headers()
            )
            
            await self.log_activity("test_connection", "success", {"agency": response.get("name")})
            return {
                "success": True,
                "agency_name": response.get("name"),
                "agency_id": response.get("id")
            }
        except Exception as e:
            await self.log_activity("test_connection", "error", {"error": str(e)})
            return {"success": False, "error": str(e)}
    
    async def sync_policies(self, since_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Sync policies from EZLynx."""
        if not since_date:
            since_date = datetime.now() - timedelta(days=30)
        
        policies = []
        
        try:
            # EZLynx policies endpoint
            response = await self.make_request(
                "GET",
                f"{self.base_url}/policies",
                headers=self._get_auth_headers(),
                params={
                    "modifiedSince": since_date.isoformat(),
                    "includeDetails": "true",
                    "pageSize": 100
                }
            )
            
            # Map EZLynx fields to our format
            field_mapping = {
                "policyNumber": "policy_number",
                "insuredName": "customer",
                "effectiveDate": "effective_date",
                "expirationDate": "expiration_date",
                "premium": "premium",
                "lineOfBusiness": "policy_type",
                "carrierName": "carrier",
                "agentCode": "agent_id"
            }
            
            for ezlynx_policy in response.get("policies", []):
                # Map basic fields
                policy = self.map_fields(ezlynx_policy, field_mapping)
                
                # Add calculated fields
                policy["external_id"] = f"ezlynx_{ezlynx_policy.get('id')}"
                policy["api_source"] = "ezlynx"
                
                # Calculate commission if rate available
                if "commissionRate" in ezlynx_policy:
                    policy["commission_rate"] = ezlynx_policy["commissionRate"]
                    policy["commission"] = (
                        float(policy["premium"]) * float(ezlynx_policy["commissionRate"]) / 100
                    )
                
                policies.append(policy)
            
            await self.log_activity(
                "sync_policies", 
                "success", 
                {"count": len(policies), "since": since_date.isoformat()}
            )
            
        except Exception as e:
            await self.log_activity("sync_policies", "error", {"error": str(e)})
            raise
        
        return policies
    
    async def push_commission(self, commission_data: Dict[str, Any]) -> Dict[str, Any]:
        """Push commission data to EZLynx."""
        try:
            # EZLynx commission update endpoint
            policy_id = commission_data.get("external_id", "").replace("ezlynx_", "")
            
            ezlynx_data = {
                "commissionAmount": commission_data.get("commission"),
                "commissionPaidDate": commission_data.get("paid_date"),
                "commissionStatus": "Paid" if commission_data.get("paid") else "Pending",
                "notes": commission_data.get("notes", "Updated from Commission Intelligence Platform")
            }
            
            response = await self.make_request(
                "PUT",
                f"{self.base_url}/policies/{policy_id}/commission",
                headers=self._get_auth_headers(),
                json=ezlynx_data
            )
            
            await self.log_activity(
                "push_commission",
                "success",
                {"policy_id": policy_id, "amount": commission_data.get("commission")}
            )
            
            return {"success": True, "external_id": f"ezlynx_{policy_id}"}
            
        except Exception as e:
            await self.log_activity("push_commission", "error", {"error": str(e)})
            return {"success": False, "error": str(e)}
    
    async def get_carriers(self) -> List[Dict[str, str]]:
        """Get list of carriers from EZLynx."""
        try:
            response = await self.make_request(
                "GET",
                f"{self.base_url}/carriers",
                headers=self._get_auth_headers()
            )
            
            carriers = []
            for carrier in response.get("carriers", []):
                carriers.append({
                    "id": carrier.get("id"),
                    "name": carrier.get("name"),
                    "naic_code": carrier.get("naicCode")
                })
            
            return carriers
            
        except Exception as e:
            await self.log_activity("get_carriers", "error", {"error": str(e)})
            return []