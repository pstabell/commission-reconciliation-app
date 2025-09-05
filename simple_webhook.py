import os
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    """Root endpoint."""
    return jsonify({
        'service': 'Commission Tracker Webhook Handler',
        'status': 'running',
        'endpoints': ['/health', '/stripe-webhook']
    })

@app.route('/health')
def health_check():
    """Health check endpoint for Render."""
    return jsonify({'status': 'healthy'}), 200

@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events - simplified version."""
    print("Webhook received!")
    
    # For now, just acknowledge receipt
    return jsonify({'status': 'received'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"Starting simple webhook server on port {port}")
    app.run(host='0.0.0.0', port=port)