from django.conf import settings
import google.generativeai as genai
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Expense, Budget, SavingsGoal, FinancialBook, Transaction, DailySavings
from rest_framework.decorators import api_view
from .serializers import ExpenseSerializer, BudgetSerializer, SavingsGoalSerializer, TransactionSerializer, DailySavingsSerializer, FinancialBookSerializer
import re
from datetime import date


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
    """Generate financial book recommendations using Gemini AI"""
   
    user_query = request.data.get('query', 'Recommend 10 financial books for students')


    if not user_query:
        return Response({"error": "Query cannot be empty"}, status=400)
    
    # to check if there are existing books in the database with the same genre
    existing_books = FinancialBook.objects.filter(genre__icontains=user_query)

    if existing_books.exists():
        # Return existing books if found
        books = existing_books.values('title', 'author', 'genre', 'difficulty_level', 'rating')
        return Response({"books": list(books)}, status=200)
    
    # Example logic to create a new book entry with a default rating
    new_book = FinancialBook.objects.create(
        title="Example Book Title",
        author="Unknown",
        genre=user_query,
        description="I want beginner-level books on investing",
        published_date=date.today(),  # Set default published_date
        difficulty_level="Beginner",
        rating=5.0  # Set default rating
    )

    return Response({"message": "New book entry created", "book": new_book.title}, status=201)


# TODO - Add cover image to book reccommendation API
# Add a financial quote
# Add a chatbot