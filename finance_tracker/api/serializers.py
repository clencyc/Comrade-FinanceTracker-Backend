# this is a serializer to convert Django model instances into
# JSON and vice versa. 
from rest_framework import serializers
from .models import Expense, Budget, SavingsGoal, FinancialBook, Transaction, DailySavings
from django.contrib.auth import get_user_model


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


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

class DailySavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySavings
        fields = '__all__'