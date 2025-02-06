from openai import OpenAI
from django.conf import settings
#import openai
client = OpenAI(api_key=settings.OPENAI_API_KEY)
from django.conf import settings
from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Expense, Budget, SavingsGoal, FinancialBook
from rest_framework.decorators import api_view
from .serializers import ExpenseSerializer, BudgetSerializer, SavingsGoalSerializer, FinancialBookSerializer

#openai.api_key = settings.OPENAI_API_KEY
# Create your views here.
# using Django restframework viewsets to handle CRUD operations

# compare these viewsets with api.urls.py
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

class SavingsGoalViewSet(viewsets.ModelViewSet):
    queryset = SavingsGoal.objects.all()
    serializer_class = SavingsGoalSerializer

@api_view(['POST'])
def ai_book_recommendation(request):
    user_query = request.data.get('query', '')

    if not user_query:
        return Response({'error': 'Please provide a query'}, status=status.HTTP_400_BAD_REQUEST)

    # this is the GPT-4 API call
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in financial book recommendations."},
                {"role": "user", "content": f"Recommend financial books for this request: {user_query}"}
            ],
            max_tokens=50
        )
        recommendations = response.choices[0].message.content

        return Response({"recommendations": recommendations})
        # return Response(response.choices[0].text.strip(), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)