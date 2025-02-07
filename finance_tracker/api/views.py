from django.conf import settings
import google.generativeai as genai
from django.conf import settings
from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Expense, Budget, SavingsGoal, FinancialBook
from rest_framework.decorators import api_view
from .serializers import ExpenseSerializer, BudgetSerializer, SavingsGoalSerializer
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

@api_view(['POST'])
def generate_book_recommendations(request):
    """Generate financial book recommendations using Gemini AI"""
   
    user_query = request.data.get('query', 'Recommend financial books for students')

    if not user_query:
        return Response({"error": "Query cannot be empty"}, status=400)
    
    # to check if there are existing books in the database
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