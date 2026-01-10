from flask import Flask, request, jsonify
import threading
import re
import json

# Import the card processing function from new.py
# We'll need to restructure new.py to be importable
from new import process_card_checkout  # We'll create this function in new.py

app = Flask(__name__)

def extract_card_details(card_string):
    """Extract card details from the format: 4112502772184364|09|29|416"""
    try:
        # Split by pipe or any other separator
        if '|' in card_string:
            parts = card_string.split('|')
        else:
            # Try to parse without separators (assuming fixed lengths)
            if len(card_string) >= 16:
                parts = [
                    card_string[:16],  # card number
                    card_string[16:18],  # month
                    card_string[18:20],  # year
                    card_string[20:]  # cvv
                ]
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
    except:
        return None

@app.route('/')
def hello():
    return jsonify({
        "message": "Card Processing API",
        "usage": "Use /<card> endpoint where card format is: CARDNUMBER|MM|YY|CVV",
        "example": "https://your-domain.com/4112502772184364|09|29|416"
    })

@app.route('/<path:card_details>')
def process_card_route(card_details):
    """Process card with details from URL path"""
    # Extract card details from the URL
    card_info = extract_card_details(card_details)
    
    if not card_info:
        return jsonify({
            "error": "Invalid card format",
            "expected_format": "CARDNUMBER|MM|YY|CVV",
            "example": "4112502772184364|09|29|416",
            "received": card_details
        }), 400
    
    # Process the card using the imported function
    try:
        result = process_card_checkout(
            card_number=card_info['card_number'],
            exp_month=card_info['exp_month'],
            exp_year=card_info['exp_year'],
            cvv=card_info['cvv']
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            "card_used": f"{card_info['card_number'][:6]}******{card_info['card_number'][-4:]}",
            "email": "",
            "response": f"Error processing card: {str(e)}",
            "status": 500
        }), 500

# For CORS support if needed
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)