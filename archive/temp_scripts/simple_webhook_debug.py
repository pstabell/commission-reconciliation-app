import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    """Debug webhook to see what's happening."""
    print("\n" + "="*50)
    print("WEBHOOK HIT - DEBUG VERSION")
    print("="*50)
    
    # Get basic info
    sig_header = request.headers.get('Stripe-Signature')
    print(f"Signature present: {'YES' if sig_header else 'NO'}")
    print(f"Webhook secret configured: {'YES' if os.getenv('STRIPE_WEBHOOK_SECRET') else 'NO'}")
    
    # Parse the payload without verification
    try:
        payload = request.data
        event = json.loads(payload)
        print(f"Event type: {event.get('type', 'Unknown')}")
        print(f"Event ID: {event.get('id', 'Unknown')}")
        
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            email = session.get('customer_details', {}).get('email', 'No email')
            print(f"Customer email: {email}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    print("="*50)
    return jsonify({'received': True}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"Debug webhook starting on port {port}")
    app.run(host='0.0.0.0', port=port)