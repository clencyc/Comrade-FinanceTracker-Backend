from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, BudgetViewSet, SavingsGoalViewSet, generate_book_recommendations, UploadTransactionView, DailySavingsCreateView, FinancialBookViewSet, get_books

# using Django restframework DefaultRouter to handle CRUD operations
# the DefaultRouter class automatically creates the API root view for us
# and also generates the URL conf for us

# The r in front of the string is a Python raw string literal. It changes the way the string literal is interpreted.
# and help avoid issues like '\' 

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet)
router.register(r'budgets', BudgetViewSet)
router.register(r'goals', SavingsGoalViewSet)
router.register(r'books', FinancialBookViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('book-recommend/', generate_book_recommendations, name='geminibook'),
    path('transaction/', UploadTransactionView.as_view(), name='transaction'),
    path('savings/', DailySavingsCreateView.as_view(), name='savings'),
    # path('books/', FinancialBookViewSet.as_view(), name='books'),
    path('bookss/', get_books, name='bookss'),


]

    



# additional documentation:
#      Expense Endpoints:
#           GET /expenses/ → List all expenses
#           POST /expenses/ → Create a new expense
#           GET /expenses/{id}/ → Retrieve a specific expense
#           PUT /expenses/{id}/ → Update a specific expense
#           DELETE /expenses/{id}/ → Delete a specific expense 
#The same applies to Budget and SavingsGoal endpoints.