from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import re
import base64
import json
from bs4 import BeautifulSoup
import time
import random
import os

app = Flask(__name__)
CORS(app)

# Simple HTML page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Card Checker API</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
        input, button { padding: 10px; margin: 5px; width: 100%; box-sizing: border-box; }
        .result { background: white; padding: 15px; margin-top: 20px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🃏 Card Checker API</h1>
        <p>Status: <span style="color:green">✅ Online</span></p>
        
        <h3>Test Card Check:</h3>
        <input type="text" id="card" placeholder="4111111111111111|04|25|123">
        <button onclick="checkCard()">Check Card</button>
        
        <div id="loading" style="display:none;">Checking...</div>
        <div id="result" class="result"></div>
        
        <h3>API Endpoints:</h3>
        <ul>
            <li><code>POST /api/check</code> - Check a card</li>
            <li><code>GET /api/bin/411111</code> - BIN lookup</li>
            <li><code>GET /api/status</code> - Service status</li>
        </ul>
    </div>
    
    <script>
        async function checkCard() {
            const card = document.getElementById('card').value;
            if(!card) return alert('Enter card details');
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').innerHTML = '';
            
            try {
                const response = await fetch('/api/check', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({card: card})
                });
                const data = await response.json();
                
                document.getElementById('loading').style.display = 'none';
                if(data.success) {
                    document.getElementById('result').innerHTML = 
                        `<h4>✅ Success</h4><pre>${data.result || data.message}</pre>`;
                } else {
                    document.getElementById('result').innerHTML = 
                        `<h4>❌ Error</h4><pre>${data.message || data.error}</pre>`;
                }
            } catch(error) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('result').innerHTML = 
                    `<h4>❌ Network Error</h4><pre>${error.message}</pre>`;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/check', methods=['POST'])
def check_card():
    try:
        data = request.get_json()
        card_input = data.get('card', '').strip()
        
        if not card_input:
            return jsonify({'success': False, 'message': 'No card provided'}), 400
        
        # Simulate card checking (replace with your actual logic)
        return jsonify({
            'success': True,
            'message': 'Card check completed',
            'result': f'Checked: {card_input}',
            'status': 'Approved ✅'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/bin/<bin_number>')
def bin_lookup(bin_number):
    try:
        return jsonify({
            'success': True,
            'bin': bin_number,
            'brand': 'VISA',
            'type': 'CREDIT',
            'bank': 'Sample Bank',
            'country': 'USA'
        })
    except:
        return jsonify({'success': False, 'message': 'BIN lookup failed'}), 500

@app.route('/api/status')
def status():
    return jsonify({
        'success': True,
        'status': 'online',
        'timestamp': time.time()
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

# Koyeb-specific: Use PORT environment variable
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
