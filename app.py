from flask import Flask, request, jsonify
from flask_cors import CORS
from new import process_card_checkout
import os
import time

app = Flask(__name__)
CORS(app)

def extract_card_details_and_proxy(card_string):
    """Extract card details and optional proxy from format: CARD|MM|YY|CVV/proxy:port:username:password"""
    try:
        # Check if proxy is included (separated by /)
        if '/' in card_string:
            card_part, proxy_part = card_string.split('/', 1)
        else:
            card_part = card_string
            proxy_part = None
        
        # Extract card details
        if '|' in card_part:
            parts = card_part.split('|')
        else:
            if len(card_part) >= 16:
                card_number = card_part[:16]
                remaining = card_part[16:]
                if len(remaining) >= 4:
                    exp_month = remaining[:2]
                    exp_year = remaining[2:4]
                    cvv = remaining[4:]
                    parts = [card_number, exp_month, exp_year, cvv]
                else:
                    return None, None
            else:
                return None, None
        
        if len(parts) != 4:
            return None, None
        
        # Parse proxy if provided
        proxy_config = None
        if proxy_part:
            proxy_parts = proxy_part.split(':')
            if len(proxy_parts) == 4:
                # Format: ip:port:username:password
                proxy_config = {
                    'http': f"http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}",
                    'https': f"http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}"
                }
            elif len(proxy_parts) == 2:
                # Format: ip:port (no auth)
                proxy_config = {
                    'http': f"http://{proxy_parts[0]}:{proxy_parts[1]}",
                    'https': f"http://{proxy_parts[0]}:{proxy_parts[1]}"
                }
        
        card_info = {
            'card_number': parts[0].strip(),
            'exp_month': parts[1].strip(),
            'exp_year': parts[2].strip(),
            'cvv': parts[3].strip()
        }
        
        return card_info, proxy_config
        
    except Exception as e:
        print(f"Error parsing input: {e}")
        return None, None

@app.route('/')
def home():
    return jsonify({
        "message": "Card Checker API with Proxy Support",
        "endpoints": {
            "check_card": "GET /<card_details>",
            "check_card_with_proxy": "GET /<card_details>/<proxy>",
            "example_proxyless": "/4111111111111111|04|25|123",
            "example_with_proxy": "/4111111111111111|04|25|123/43.159.29.246:9999:td-customer-K17667574031427-country-us:K17667574031427",
            "proxy_format": "IP:PORT:USERNAME:PASSWORD or IP:PORT",
            "status": "GET /status",
            "health": "GET /health"
        }
    })

@app.route('/<path:input_data>')
def process_card_route(input_data):
    """Process card with optional proxy from URL path"""
    print(f"Processing input: {input_data}")
    
    card_info, proxy_config = extract_card_details_and_proxy(input_data)
    
    if not card_info:
        return jsonify({
            "success": False,
            "message": "Invalid format",
            "expected_formats": [
                "CARD|MM|YY|CVV",
                "CARD|MM|YY|CVV/IP:PORT:USERNAME:PASSWORD",
                "CARD|MM|YY|CVV/IP:PORT"
            ],
            "examples": [
                "/4111111111111111|04|25|123",
                "/4111111111111111|04|25|123/43.159.29.246:9999:td-customer-K17667574031427-country-us:K17667574031427",
                "/4111111111111111|04|25|123/43.159.29.246:9999"
            ],
            "received": input_data
        }), 400
    
    try:
        print(f"Processing card: {card_info['card_number'][:6]}******{card_info['card_number'][-4:]}")
        if proxy_config:
            print(f"Using proxy: {proxy_config.get('http', 'N/A')}")
        else:
            print("No proxy - running proxyless")
        
        result = process_card_checkout(
            card_number=card_info['card_number'],
            exp_month=card_info['exp_month'],
            exp_year=card_info['exp_year'],
            cvv=card_info['cvv'],
            proxy_config=proxy_config  # Pass proxy config to the function
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}",
            "card": f"{card_info['card_number'][:6]}******{card_info['card_number'][-4:]}",
            "email": "",
            "raw_response": str(e),
            "status": 500,
            "time_elapsed": 0
        }), 500

@app.route('/status')
def status():
    return jsonify({
        "success": True,
        "status": "online",
        "timestamp": time.time()
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/ping')
def ping():
    return jsonify({"message": "pong"}), 200

# CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting Card Checker API on port {port}...")
    print(f"Test URLs:")
    print(f"  Proxyless: http://localhost:{port}/4111111111111111|04|25|123")
    print(f"  With proxy: http://localhost:{port}/4111111111111111|04|25|123/43.159.29.246:9999:username:password")
    app.run(host='0.0.0.0', port=port, debug=False)
