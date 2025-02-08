# this is a serializer to convert Django model instances into
# JSON and vice versa. 
from rest_framework import serializers
from .models import Expense, Budget, SavingsGoal, FinancialBook, Transaction

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

class SavingsGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsGoal
        fields = '__all__'

class FinancialBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialBook
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'