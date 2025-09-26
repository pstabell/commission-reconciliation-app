"""
Webhook event handler for Commission Intelligence Platform
Processes and delivers webhook events to registered endpoints
"""
import asyncio
import aiohttp
import hashlib
import hmac
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
import os
import sys
sys.path.append('..')
from commission_app import get_supabase_client

class WebhookHandler:
    """Handles webhook event processing and delivery."""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self.retry_delays = [60, 300, 900, 3600]  # 1min, 5min, 15min, 1hr
        
    async def trigger_event(self, event_type: str, payload: Dict[str, Any], user_email: str = None):
        """Trigger a webhook event for all subscribed endpoints."""
        # Get active webhooks subscribed to this event
        query = self.supabase.table('webhook_endpoints').select("*").eq('is_active', True)
        
        if user_email:
            query = query.eq('user_email', user_email)
        
        # Check if event_type is in the events array
        webhooks = []
        all_webhooks = query.execute()
        
        for webhook in all_webhooks.data:
            if event_type in webhook.get('events', []) or '*' in webhook.get('events', []):
                webhooks.append(webhook)
        
        # Create event logs and deliver
        tasks = []
        for webhook in webhooks:
            event_log = self._create_event_log(webhook['id'], event_type, payload)
            tasks.append(self._deliver_webhook(webhook, event_log))
        
        # Process all webhooks concurrently
        if tasks:
            await asyncio.gather(*tasks)
    
    def _create_event_log(self, webhook_id: str, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a webhook event log entry."""
        event_data = {
            'webhook_id': webhook_id,
            'event_type': event_type,
            'payload': json.dumps(payload),
            'status': 'pending',
            'attempts': 0,
            'created_at': datetime.now().isoformat()
        }
        
        result = self.supabase.table('webhook_event_logs').insert(event_data).execute()
        return result.data[0] if result.data else event_data
    
    async def _deliver_webhook(self, webhook: Dict[str, Any], event_log: Dict[str, Any]):
        """Deliver a webhook event with retries."""
        max_attempts = len(self.retry_delays) + 1
        
        for attempt in range(max_attempts):
            try:
                # Prepare webhook payload
                payload = {
                    'id': event_log['id'],
                    'event': event_log['event_type'],
                    'created_at': event_log['created_at'],
                    'data': json.loads(event_log['payload'])
                }
                
                # Calculate signature if secret exists
                headers = {
                    'Content-Type': 'application/json',
                    'X-Webhook-Event': event_log['event_type'],
                    'X-Webhook-ID': event_log['id']
                }
                
                if webhook.get('secret'):
                    signature = self._calculate_signature(json.dumps(payload), webhook['secret'])
                    headers['X-Webhook-Signature'] = signature
                
                # Make HTTP request
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        webhook['url'],
                        json=payload,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        response_text = await response.text()
                        
                        # Update event log
                        update_data = {
                            'attempts': attempt + 1,
                            'last_attempt': datetime.now().isoformat(),
                            'response_code': response.status,
                            'response_body': response_text[:1000]  # Limit response size
                        }
                        
                        if response.status >= 200 and response.status < 300:
                            # Success
                            update_data['status'] = 'delivered'
                            self._update_webhook_stats(webhook['id'], success=True)
                        else:
                            # Failed, but got response
                            if attempt < max_attempts - 1:
                                update_data['status'] = 'pending'
                                update_data['next_retry'] = (
                                    datetime.now() + timedelta(seconds=self.retry_delays[attempt])
                                ).isoformat()
                            else:
                                update_data['status'] = 'failed'
                                self._update_webhook_stats(webhook['id'], success=False)
                        
                        self.supabase.table('webhook_event_logs').update(update_data).eq('id', event_log['id']).execute()
                        
                        if update_data['status'] == 'delivered':
                            break
                            
            except Exception as e:
                # Network or other error
                update_data = {
                    'attempts': attempt + 1,
                    'last_attempt': datetime.now().isoformat(),
                    'response_body': str(e)[:1000]
                }
                
                if attempt < max_attempts - 1:
                    update_data['status'] = 'pending'
                    update_data['next_retry'] = (
                        datetime.now() + timedelta(seconds=self.retry_delays[attempt])
                    ).isoformat()
                else:
                    update_data['status'] = 'failed'
                    self._update_webhook_stats(webhook['id'], success=False)
                
                self.supabase.table('webhook_event_logs').update(update_data).eq('id', event_log['id']).execute()
            
            # Wait before retry if not last attempt
            if attempt < max_attempts - 1 and update_data.get('status') != 'delivered':
                await asyncio.sleep(self.retry_delays[attempt])
    
    def _calculate_signature(self, payload: str, secret: str) -> str:
        """Calculate HMAC-SHA256 signature for webhook payload."""
        return hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _update_webhook_stats(self, webhook_id: str, success: bool):
        """Update webhook delivery statistics."""
        webhook = self.supabase.table('webhook_endpoints').select("*").eq('id', webhook_id).execute()
        
        if webhook.data:
            current = webhook.data[0]
            update_data = {
                'last_triggered': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            if success:
                update_data['success_count'] = current.get('success_count', 0) + 1
            else:
                update_data['failure_count'] = current.get('failure_count', 0) + 1
            
            self.supabase.table('webhook_endpoints').update(update_data).eq('id', webhook_id).execute()

# Common webhook events
class WebhookEvents:
    """Standard webhook event types."""
    
    POLICY_CREATED = "policy.created"
    POLICY_UPDATED = "policy.updated"
    POLICY_RENEWED = "policy.renewed"
    POLICY_CANCELLED = "policy.cancelled"
    
    COMMISSION_CALCULATED = "commission.calculated"
    COMMISSION_PAID = "commission.paid"
    COMMISSION_ADJUSTED = "commission.adjusted"
    
    RECONCILIATION_STARTED = "reconciliation.started"
    RECONCILIATION_COMPLETED = "reconciliation.completed"
    
    RENEWAL_UPCOMING = "renewal.upcoming"
    RENEWAL_MISSED = "renewal.missed"

# Example usage
async def example_webhook_usage():
    """Example of triggering webhook events."""
    handler = WebhookHandler()
    
    # Policy created event
    await handler.trigger_event(
        WebhookEvents.POLICY_CREATED,
        {
            "policy": {
                "id": "123",
                "policy_number": "AUTO-456789",
                "customer": "John Doe",
                "premium": 1200.00,
                "commission": 144.00,
                "effective_date": "2025-09-01"
            }
        },
        user_email="user@example.com"
    )
    
    # Commission calculated event
    await handler.trigger_event(
        WebhookEvents.COMMISSION_CALCULATED,
        {
            "policy_id": "123",
            "calculation": {
                "premium": 1200.00,
                "rate": 12.0,
                "gross_commission": 144.00,
                "agent_commission": 72.00
            }
        }
    )

if __name__ == "__main__":
    # Test webhook handler
    asyncio.run(example_webhook_usage())