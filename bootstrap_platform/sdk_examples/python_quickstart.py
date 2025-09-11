"""
Commission Intelligence Platform - Python SDK Quickstart
This example demonstrates basic usage of the Commission IQ API
"""

import os
import json
from datetime import datetime, timedelta
import httpx

# Configuration
API_KEY = os.environ.get("COMMISSION_IQ_API_KEY", "demo_key_12345")
BASE_URL = "https://api.commission-intelligence.io/v1"

# For local development
# BASE_URL = "http://localhost:8000/api/v1"


class CommissionIQClient:
    """Simple client for Commission IQ API"""
    
    def __init__(self, api_key: str, base_url: str = BASE_URL):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30.0
        )
    
    def list_policies(self, **params):
        """List policies with optional filtering"""
        response = self.client.get(f"{self.base_url}/policies", params=params)
        response.raise_for_status()
        return response.json()
    
    def create_policy(self, policy_data):
        """Create a new policy"""
        response = self.client.post(f"{self.base_url}/policies", json=policy_data)
        response.raise_for_status()
        return response.json()
    
    def calculate_commission(self, premium: float, rate: float, type: str = "NEW"):
        """Calculate commission for given parameters"""
        data = {
            "premium": premium,
            "rate": rate,
            "type": type
        }
        response = self.client.post(f"{self.base_url}/commissions/calculate", json=data)
        response.raise_for_status()
        return response.json()
    
    def get_dashboard_metrics(self, period: str = "month"):
        """Get dashboard analytics"""
        response = self.client.get(f"{self.base_url}/analytics/dashboard", params={"period": period})
        response.raise_for_status()
        return response.json()
    
    def get_integrations(self):
        """List available integrations"""
        response = self.client.get(f"{self.base_url}/integrations")
        response.raise_for_status()
        return response.json()
    
    def close(self):
        """Close the client connection"""
        self.client.close()


def main():
    """Example usage of the Commission IQ API"""
    
    # Initialize client
    client = CommissionIQClient(API_KEY)
    
    try:
        print("Commission Intelligence Platform - API Demo\n")
        
        # 1. List existing policies
        print("1. Fetching existing policies...")
        policies = client.list_policies(status="active", page=1, per_page=5)
        print(f"   Found {policies['pagination']['total']} total policies")
        print(f"   Total premium: ${policies['summary']['total_premium']:,.2f}")
        print(f"   Total commission: ${policies['summary']['total_commission']:,.2f}\n")
        
        # 2. Create a new policy
        print("2. Creating a new policy...")
        new_policy = {
            "policy_number": f"DEMO-{datetime.now().strftime('%Y%m%d%H%M')}",
            "customer": "Demo Insurance Agency",
            "carrier": "Progressive",
            "policy_type": "AUTO",
            "premium": 3500.00,
            "effective_date": datetime.now().date().isoformat(),
            "expiration_date": (datetime.now() + timedelta(days=365)).date().isoformat(),
            "commission_rate": 12.5
        }
        
        created = client.create_policy(new_policy)
        if created['success']:
            print(f"   ✓ Created policy {created['data']['policy_number']}")
            print(f"   Commission amount: ${created['data']['commission_amount']:,.2f}\n")
        
        # 3. Calculate commission scenarios
        print("3. Commission calculations:")
        scenarios = [
            {"premium": 5000, "rate": 15, "type": "NEW", "desc": "New auto policy"},
            {"premium": 8000, "rate": 10, "type": "RENEWAL", "desc": "Home renewal"},
            {"premium": 2000, "rate": 20, "type": "ENDORSEMENT", "desc": "Policy endorsement"}
        ]
        
        for scenario in scenarios:
            result = client.calculate_commission(
                premium=scenario['premium'],
                rate=scenario['rate'],
                type=scenario['type']
            )
            print(f"   {scenario['desc']}:")
            print(f"     Premium: ${scenario['premium']:,}")
            print(f"     Agent commission: ${result['results']['agent_commission']:,.2f}")
            print(f"     Agency commission: ${result['results']['agency_commission']:,.2f}")
        
        print()
        
        # 4. Get dashboard metrics
        print("4. Dashboard analytics:")
        metrics = client.get_dashboard_metrics(period="month")
        
        print(f"   Active policies: {metrics['metrics']['active_policies']:,}")
        print(f"   Renewal rate: {metrics['metrics']['renewal_rate']:.1f}%")
        print(f"   Monthly growth: {metrics['trends']['monthly_growth']:.1f}%")
        
        print("\n   Top carriers by commission:")
        for carrier in metrics['top_carriers'][:3]:
            print(f"     - {carrier['name']}: ${carrier['commission']:,.2f}")
        
        print("\n   Top agents:")
        for agent in metrics['top_agents'][:3]:
            print(f"     - {agent['name']}: ${agent['commission']:,.2f} ({agent['policies']} policies)")
        
        print()
        
        # 5. Check available integrations
        print("5. Available integrations:")
        integrations = client.get_integrations()
        
        for integration in integrations['integrations']:
            status_emoji = "✓" if integration['status'] == "available" else "⏳"
            print(f"   {status_emoji} {integration['name']} ({integration['category']})")
            print(f"      Setup fee: ${integration['setup_fee']:,}")
            for feature in integration['features'][:2]:
                print(f"      - {feature}")
        
        print(f"\n   Total: {integrations['summary']['available']} available, "
              f"{integrations['summary']['coming_soon']} coming soon")
        
        # 6. Webhook testing
        print("\n6. Testing webhook delivery...")
        # Note: In production, you'd register a real webhook endpoint
        print("   Webhook functionality ready for production use")
        
        # Summary
        print("\n" + "="*50)
        print("Demo completed successfully!")
        print("Ready to integrate? Visit https://commission-intelligence.io/api/docs")
        
    except httpx.HTTPStatusError as e:
        print(f"API Error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client.close()


if __name__ == "__main__":
    main()