from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import google.generativeai as genai
import uuid
from django.contrib.auth.models import AbstractUser

genai.configure(api_key=settings.GEMINI_API_KEY)

# Authentication model
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


# expense models
class Expense(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True,  null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"
    
# Budget models
# Budgets for weeks, months, semesters

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.category} Budget"
    
class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def __str__(self):
        return self.goal
    
class FinancialBook(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    difficulty_level = models.CharField(max_length=50, default='Beginner', choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ])
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    

# TODO add saving endpoint.
class DailySavings(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    savings_goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE)
    amount_saved = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.savings_goal} - {self.amount_saved}"
        # return f"{self.user.username} saved {self.amount_saved} on {self.date}"


class Transaction(models.Model):
    receipt_no = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    completion_time = models.DateTimeField(default=timezone.now)
    details = models.CharField(max_length=500, default='No details provided')
    transaction_status = models.CharField(max_length=50, default='Pending')
    paid_in = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    withdrawn = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    category = models.CharField(max_length=250, blank=True, null=True)

    def categorize_transaction(self):
        """Automatically categorize transaction based on details"""
        details_lower = self.details.lower()
        if "bundle" in details_lower:
            return "Data Purchase"
        elif "merchant payment" in details_lower:
            return "Shopping"
        elif "pay bill" in details_lower:
            return "Utilities"
        elif "customer transfer" in details_lower:
            return "Transfer"
        else:
            return "Other"
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.category:
            self.category = self.categorize_transaction()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.receipt_no} - {self.category}"

    def __str__(self):
        return f"{self.transaction_id} - {self.amount}"
    
    def categorize_transaction(transaction_details):
        """Uses Gemini AI to classify transaction details into a financial category."""
        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            
            prompt = f"""
            Categorize this financial transaction into one of the following categories:
            - Data Purchase
            - Merchant Payment
            - Utility Bill Payment
            - Fund Transfer
            - Business Payment
            - Other

            Transaction Details: {transaction_details}

            Return only the category name.
            """
            response = model.generate_content(prompt)

            return response.text.strip() if response.text else "Other"

        except Exception as e:
            print(f"AI categorization failed: {e}")
            return "Other"  # Default category in case of failure