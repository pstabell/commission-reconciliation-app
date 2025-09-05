import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'status': 'running'}), 200

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    # Just acknowledge receipt for now
    return jsonify({'status': 'received'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)