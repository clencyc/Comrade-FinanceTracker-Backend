import google.generativeai as genai
from django.conf import settings
import requests
genai.configure(api_key=settings.GOOGLE_API_KEY)
import base64


model = genai.GenerativeModel('gemini-pro')
genai.configure(api_key=settings.GOOGLE_API_KEY)


# def get_visa_exchange_rate(source_currency, target_currency):
#     url = "https://sandbox.api.visa.comcdsapi/commercial/v1/ob/starterdata"
#     headers = {
#         'Authorization': f'Basic {base64.b64encode(f"{settings.VISA_API_KEY}:{settings.VISA_SHARED_SECRET}".encode()).decode()}',
#         'Accept': 'application/json',
#         'Content-Type': 'application/json'
#     }
#     payload = {
#         "sourceCurrencyCode": source_currency,
#         "destinationCurrencyCodes": [target_currency]
#     }
#     response = requests.post(url, headers=headers, json=payload)
#     if response.status_code == 200:
#         data = response.json()
#         return data['forexRates'][0]['rate']
#     else:
#         return None

def get_chatbot_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
    