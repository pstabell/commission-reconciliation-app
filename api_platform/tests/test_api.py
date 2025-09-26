"""
Test suite for Commission Intelligence Platform API
Run with: pytest test_api.py
"""
import pytest
import asyncio
from datetime import datetime, date
from fastapi.testclient import TestClient
import sys
sys.path.append('..')
from api_server import app, CommissionCalculateRequest

# Test client
client = TestClient(app)

# Mock API key for testing
TEST_API_KEY = "test_key_12345"

@pytest.fixture
def mock_auth(monkeypatch):
    """Mock authentication for tests."""
    def mock_verify():
        return {"user_email": "test@example.com", "api_key": TEST_API_KEY}
    monkeypatch.setattr("api_server.verify_api_key", mock_verify)

class TestBasicEndpoints:
    """Test basic API endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Commission Intelligence Platform API"
        assert "version" in data
        assert data["status"] == "operational"
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

class TestPolicyEndpoints:
    """Test policy-related endpoints."""
    
    def test_list_policies(self, mock_auth):
        """Test listing policies."""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        response = client.get("/v1/policies", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_policy(self, mock_auth):
        """Test creating a policy."""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        policy_data = {
            "policy_number": "TEST-123456",
            "customer": "Test Customer",
            "effective_date": "2025-09-01",
            "premium": 1000.0,
            "policy_type": "AUTO",
            "carrier": "Test Carrier",
            "transaction_type": "NEW"
        }
        
        response = client.post("/v1/policies", json=policy_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["policy_number"] == "TEST-123456"
        assert data["customer"] == "Test Customer"
    
    def test_create_policy_invalid_data(self, mock_auth):
        """Test creating policy with invalid data."""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        invalid_data = {
            "customer": "Test Customer"  # Missing required fields
        }
        
        response = client.post("/v1/policies", json=invalid_data, headers=headers)
        assert response.status_code == 422  # Validation error

class TestCommissionEndpoints:
    """Test commission calculation endpoints."""
    
    def test_calculate_commission(self, mock_auth):
        """Test commission calculation."""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        calc_data = {
            "premium": 1000.0,
            "commission_rate": 10.0,
            "policy_type": "AUTO",
            "transaction_type": "NEW"
        }
        
        response = client.post("/v1/commissions/calculate", json=calc_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["gross_commission"] == 100.0
        assert data["agent_commission"] == 50.0  # 50% split for NEW
        assert data["agency_commission"] == 50.0
    
    def test_calculate_cancellation_commission(self, mock_auth):
        """Test negative commission for cancellation."""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        calc_data = {
            "premium": 1000.0,
            "commission_rate": 10.0,
            "policy_type": "AUTO",
            "transaction_type": "CXL"
        }
        
        response = client.post("/v1/commissions/calculate", json=calc_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["gross_commission"] == -100.0  # Negative for cancellation

class TestWebhookEndpoints:
    """Test webhook management endpoints."""
    
    def test_create_webhook(self, mock_auth):
        """Test webhook creation."""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        webhook_data = {
            "url": "https://example.com/webhook",
            "events": ["policy.created", "commission.calculated"]
        }
        
        response = client.post("/v1/webhooks", json=webhook_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["url"] == "https://example.com/webhook"
        assert len(data["events"]) == 2
        assert data["is_active"] == True
    
    def test_list_webhooks(self, mock_auth):
        """Test listing webhooks."""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        response = client.get("/v1/webhooks", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestAnalyticsEndpoints:
    """Test analytics endpoints."""
    
    def test_analytics_summary(self, mock_auth):
        """Test analytics summary endpoint."""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        response = client.get(
            "/v1/analytics/summary",
            params={"start_date": "2025-09-01", "end_date": "2025-09-31"},
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "totals" in data
        assert "by_type" in data
        assert "by_carrier" in data

class TestAuthenticationAndSecurity:
    """Test authentication and security features."""
    
    def test_unauthorized_access(self):
        """Test access without API key."""
        response = client.get("/v1/policies")
        assert response.status_code == 403  # Forbidden without auth
    
    def test_invalid_api_key(self):
        """Test with invalid API key."""
        headers = {"Authorization": "Bearer invalid_key"}
        response = client.get("/v1/policies", headers=headers)
        assert response.status_code == 401  # Unauthorized
    
    def test_rate_limiting(self, mock_auth):
        """Test rate limiting (if implemented)."""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        # Make many requests quickly
        for _ in range(10):
            response = client.get("/v1/policies", headers=headers)
        # Should still work within rate limit
        assert response.status_code == 200

class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_search(self, mock_auth):
        """Test search with empty query."""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        response = client.get("/v1/search", params={"q": ""}, headers=headers)
        assert response.status_code in [200, 422]  # May validate or return empty
    
    def test_future_date_renewal(self, mock_auth):
        """Test renewal search with extreme date."""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        response = client.get(
            "/v1/renewals/upcoming",
            params={"days_ahead": 9999},
            headers=headers
        )
        assert response.status_code == 200
    
    def test_batch_with_mixed_valid_invalid(self, mock_auth):
        """Test batch creation with some invalid policies."""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        policies = [
            {  # Valid
                "policy_number": "BATCH-001",
                "customer": "Customer 1",
                "effective_date": "2025-09-01",
                "premium": 1000.0
            },
            {  # Invalid - missing required field
                "customer": "Customer 2"
            }
        ]
        
        response = client.post("/v1/policies/batch", json=policies, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success_count"] >= 0
        assert data["error_count"] >= 0

# Performance tests
class TestPerformance:
    """Test API performance characteristics."""
    
    def test_large_policy_list(self, mock_auth):
        """Test handling large result sets."""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        response = client.get(
            "/v1/policies",
            params={"per_page": 100},
            headers=headers
        )
        assert response.status_code == 200
        # Should handle pagination properly
    
    def test_concurrent_requests(self, mock_auth):
        """Test handling concurrent requests."""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        
        async def make_request():
            return client.get("/v1/policies", headers=headers)
        
        # Simulate concurrent requests
        loop = asyncio.new_event_loop()
        tasks = [make_request() for _ in range(5)]
        # All should succeed
        results = loop.run_until_complete(asyncio.gather(*tasks))
        for result in results:
            assert result.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])