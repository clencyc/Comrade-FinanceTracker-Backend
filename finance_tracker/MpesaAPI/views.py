from django.shortcuts import render
import requests
from django.http import JsonResponse
from .models import MpesaTransaction
from django.db.models import Sum
from rest_framework.decorators import api_view
from .utils import get_access_token, categorize_transaction
# Create your views here.

access_token = "9ieOPkhAAnIWW8J7IcoDkjyR6kNe"

@api_view(['GET'])
def mpesa_token_view(request):
    """Get and return the M-Pesa access token"""
    try:
        access_token = get_access_token()
        return JsonResponse({"access_token": access_token})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def generate_insights(request):
    insights = MpesaTransaction.objects.values('category').annotate(total=Sum('amount'))
    return JsonResponse(list(insights), safe=False)

def fetch_transaction_status(request, transaction_id):
    access_token = get_access_token()
    url = f"https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query"
    headers = {
        'Authorization' : f'Bearer {access_token}',
        'Content-Type' : 'application/json'
    }
    payload = {
        "Initiator": "testapi",
        "SecurityCredential": "password1234",
        "CommandID": "TransactionStatusQuery",
        "TransactionID": transaction_id,
        "PartyA": "600000",
        "IdentifierType": "4",
        "ResultURL": "https://yourdomain.com/result",
        "QueueTimeOutURL": "https://yourdomain.com/timeout",
        "Remarks": "Check transaction status",
        "Occasion": "Transaction status check"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        if data.get('TransactionID') is None:
            return JsonResponse({"error": "TransactionID not found in response"}, status=400)


    # Save transaction to database
        transaction = MpesaTransaction(
            transaction_id=data.get('TransactionID'),
            amount=data.get('Amount'),
            description=data.get('TransactionDescription'),
            category=categorize_transaction(data.get('TransactionDescription')),
        )
        transaction.save()

        return JsonResponse(data)
    
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Request failed: {str(e)}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)