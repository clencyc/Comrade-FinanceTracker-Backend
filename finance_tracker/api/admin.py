from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Expense, Budget, SavingsGoal, FinancialBook

# Register your models here.
admin.site.register(Expense)
admin.site.register(Budget)
admin.site.register(SavingsGoal)
admin.site.register(FinancialBook)
admin.site.register(UserRegistration)
admin.site.register(UserLogin) 