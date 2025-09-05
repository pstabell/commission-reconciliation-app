import os
import stripe
import json
from flask import Flask, request, jsonify
from supabase import create_client, Client
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

# Initialize Supabase (production database)
def get_supabase_client():
    """Get Supabase client for production database."""
    url = os.getenv("PRODUCTION_SUPABASE_URL", os.getenv("SUPABASE_URL"))
    key = os.getenv("PRODUCTION_SUPABASE_ANON_KEY", os.getenv("SUPABASE_ANON_KEY"))
    if not url or not key:
        print("Warning: Supabase credentials not configured")
        return None
    return create_client(url, key)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render."""
    return jsonify({'status': 'healthy'}), 200

@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events."""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    # Log webhook received
    print(f"\n{'='*50}")
    print(f"Webhook received at {datetime.now()}")
    print(f"Signature header present: {'Yes' if sig_header else 'No'}")
    
    # Check if webhook secret is configured
    if not webhook_secret:
        print("WARNING: STRIPE_WEBHOOK_SECRET not configured!")
        # For testing, parse without verification
        try:
            event = json.loads(payload)
        except Exception as e:
            print(f"Failed to parse payload: {e}")
            return jsonify({'error': 'Invalid JSON'}), 400
    else:
        try:
            # Verify webhook signature
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as e:
            print(f"Invalid payload: {e}")
            return jsonify({'error': 'Invalid payload'}), 400
        except stripe.error.SignatureVerificationError as e:
            print(f"Invalid signature: {e}")
            return jsonify({'error': 'Invalid signature'}), 400
    
    # Log event type
    print(f"Event type: {event['type']}")
    print(f"Event ID: {event.get('id', 'Unknown')}")
    
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Extract relevant data
        stripe_customer_id = session.get('customer')
        customer_email = session.get('customer_details', {}).get('email')
        subscription_id = session.get('subscription')
        
        print(f"Payment successful:")
        print(f"  Customer ID: {stripe_customer_id}")
        print(f"  Email: {customer_email}")
        print(f"  Subscription ID: {subscription_id}")
        
        # Update database (if Supabase is configured)
        supabase = get_supabase_client()
        print(f"Supabase client: {'Connected' if supabase else 'Not connected'}")
        
        if supabase and customer_email:
            try:
                # Check if user exists
                result = supabase.table('users').select("*").eq('email', customer_email).execute()
                
                if result.data:
                    # Update existing user
                    update_data = {
                        'stripe_customer_id': stripe_customer_id,
                        'subscription_id': subscription_id,
                        'subscription_status': 'active',
                        'subscription_updated_at': datetime.now().isoformat()
                    }
                    supabase.table('users').update(update_data).eq('email', customer_email).execute()
                    print(f"Updated user: {customer_email}")
                else:
                    # Create new user
                    user_data = {
                        'email': customer_email,
                        'stripe_customer_id': stripe_customer_id,
                        'subscription_id': subscription_id,
                        'subscription_status': 'active',
                        'created_at': datetime.now().isoformat()
                    }
                    supabase.table('users').insert(user_data).execute()
                    print(f"Created new user: {customer_email}")
                    
            except Exception as e:
                print(f"Database error: {e}")
    
    # Handle subscription updated
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        status = subscription.get('status')
        customer_id = subscription.get('customer')
        
        print(f"Subscription updated: Customer {customer_id}, Status: {status}")
        
        # Update subscription status in database
        supabase = get_supabase_client()
        if supabase:
            try:
                supabase.table('users').update({
                    'subscription_status': status,
                    'subscription_updated_at': datetime.now().isoformat()
                }).eq('stripe_customer_id', customer_id).execute()
            except Exception as e:
                print(f"Database error: {e}")
    
    # Handle subscription deleted
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        customer_id = subscription.get('customer')
        
        print(f"Subscription cancelled: Customer {customer_id}")
        
        # Update subscription status to cancelled
        supabase = get_supabase_client()
        if supabase:
            try:
                supabase.table('users').update({
                    'subscription_status': 'cancelled',
                    'subscription_updated_at': datetime.now().isoformat()
                }).eq('stripe_customer_id', customer_id).execute()
            except Exception as e:
                print(f"Database error: {e}")
    
    # Handle payment failed
    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        customer_id = invoice.get('customer')
        
        print(f"Payment failed: Customer {customer_id}")
        
        # You might want to send an email or update status
        # For now, just log it
    
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"Webhook server starting on port {port}")
    print("Environment variables:")
    print(f"  STRIPE_SECRET_KEY: {'Set' if os.getenv('STRIPE_SECRET_KEY') else 'Not set'}")
    print(f"  STRIPE_WEBHOOK_SECRET: {'Set' if os.getenv('STRIPE_WEBHOOK_SECRET') else 'Not set'}")
    print(f"  PRODUCTION_SUPABASE_URL: {'Set' if os.getenv('PRODUCTION_SUPABASE_URL') else 'Not set'}")
    app.run(host='0.0.0.0', port=port, debug=False)