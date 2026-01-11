from flask import Flask, request, jsonify
from flask_cors import CORS
from new import process_card_checkout
import os
import time

app = Flask(__name__)
CORS(app)

def extract_card_details(card_string):
    """Extract card details from the format: 4112502772184364|09|29|416"""
    try:
        if '|' in card_string:
            parts = card_string.split('|')
        else:
            if len(card_string) >= 16:
                card_number = card_string[:16]
                remaining = card_string[16:]
                if len(remaining) >= 4:
                    exp_month = remaining[:2]
                    exp_year = remaining[2:4]
                    cvv = remaining[4:]
                    parts = [card_number, exp_month, exp_year, cvv]
                else:
                    return None
            else:
                return None
        
        if len(parts) != 4:
            return None
            
        return {
            'card_number': parts[0].strip(),
            'exp_month': parts[1].strip(),
            'exp_year': parts[2].strip(),
            'cvv': parts[3].strip()
        }
    except Exception as e:
        print(f"Error parsing card: {e}")
        return None

@app.route('/')
def home():
    return jsonify({
        "message": "Epicalarc Card Checker API",
        "endpoints": {
            "check_card": "GET /<card_details>",
            "example": "https://surprising-willette-golmal-0ba321df.koyeb.app/4111111111111111|04|25|123",
            "format": "CARDNUMBER|MM|YY|CVV",
            "status": "GET /status",
            "health": "GET /health"
        },
        "gateway": "epicalarc.com"
    })

@app.route('/<path:card_details>')
def process_card_route(card_details):
    """Process card with details from URL path"""
    print(f"Processing card: {card_details}")
    
    card_info = extract_card_details(card_details)
    
    if not card_info:
        return jsonify({
            "success": False,
            "message": "Invalid card format",
            "expected_format": "CARDNUMBER|MM|YY|CVV",
            "example": "4112502772184364|09|29|416",
            "received": card_details
        }), 400
    
    try:
        print(f"Processing card: {card_info['card_number'][:6]}******{card_info['card_number'][-4:]}")
        
        result = process_card_checkout(
            card_number=card_info['card_number'],
            exp_month=card_info['exp_month'],
            exp_year=card_info['exp_year'],
            cvv=card_info['cvv']
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}",
            "card": f"{card_info['card_number'][:6]}******{card_info['card_number'][-4:]}",
            "email": "",
            "gateway": "epicalarc.com"
        }), 500

@app.route('/status')
def status():
    return jsonify({
        "success": True,
        "status": "online",
        "gateway": "epicalarc.com",
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
    print(f"Starting Epicalarc Card Checker API on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
