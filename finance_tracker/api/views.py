from django.shortcuts import render
from rest_framework import viewsets
from .models import Expense, Budget, SavingsGoal, FinancialBook
from .serializers import ExpenseSerializer, BudgetSerializer, SavingsGoalSerializer, FinancialBookSerializer

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

class FinancialBookViewSet(viewsets.ModelViewSet):
    queryset = FinancialBook.objects.all()
    serializer_class = FinancialBookSerializer