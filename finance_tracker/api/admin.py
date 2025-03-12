from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Expense, Budget, SavingsGoal, FinancialBook, CustomUser

# Register your models here.
admin.site.register(Expense)
admin.site.register(Budget)
admin.site.register(SavingsGoal)
admin.site.register(FinancialBook)
admin.site.register(CustomUser, UserAdmin)