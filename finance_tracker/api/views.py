from django.conf import settings
import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Expense, Budget, SavingsGoal, FinancialBook, Transaction, DailySavings
from rest_framework.decorators import api_view
from .serializers import ExpenseSerializer, BudgetSerializer, SavingsGoalSerializer, TransactionSerializer, DailySavingsSerializer, FinancialBookSerializer
import re
from datetime import date
from .services import get_book_recommendations, fetch_financial_books
import logging

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)

genai.configure(api_key=settings.GEMINI_API_KEY)
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

# retrieve financial books from the database
class FinancialBookViewSet(viewsets.ModelViewSet):
    queryset = FinancialBook.objects.all()
    serializer_class = FinancialBookSerializer

class UploadTransactionView(APIView):
    def post(self, request):
        data = request.data.copy()
        
        if 'details' in data:
            data['details'] = re.sub(r'\d+', '', data['details'])[:250]  # Clean details

        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            transaction = serializer.save()
            transaction.categorize_transaction()
            transaction.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DailySavingsCreateView(generics.CreateAPIView):
    queryset = DailySavings.objects.all()
    serializer_class = DailySavingsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
def generate_book_recommendations(request):
    user_query = request.data.get('query', '')

    if not user_query:
        return Response({"error": "Query parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)

    existing_books = FinancialBook.objects.filter(genre__icontains=user_query)

    if existing_books.exists():
        first_book = existing_books.first()
        title = first_book.title
    else:
        title = 'Unknown Title'

    recommendations = get_book_recommendations(user_query)

    if not recommendations:
        return Response({"error": "No recommendations found"}, status=status.HTTP_404_NOT_FOUND)

    first_book = recommendations[0]  # Assuming recommendations is a list of book dictionaries
    if isinstance(first_book, dict):
        new_book = FinancialBook.objects.create(
            title=first_book.get('title', 'Unknown Title'),
            author=first_book.get('author', 'Unknown Author'),
            genre=first_book.get('genre', 'Unknown Genre'),
            description=first_book.get('description', ''),
            difficulty_level=first_book.get('difficulty_level', 'Beginner'),
            rating=first_book.get('rating', 5.0),
            image_url=first_book.get('image_url', '')
        )
    else:
        return Response({"error": "Invalid recommendation format"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(recommendations)

# view to fetch books from google books api
@api_view(['GET'])
def get_books(request):
    query = request.GET.get('query', 'finance')
    result = fetch_financial_books(query)
    return JsonResponse(result, safe=False)