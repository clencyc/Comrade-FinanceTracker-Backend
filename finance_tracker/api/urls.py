from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, BudgetViewSet, SavingsGoalViewSet, generate_book_recommendations

# using Django restframework DefaultRouter to handle CRUD operations
# the DefaultRouter class automatically creates the API root view for us
# and also generates the URL conf for us

# The r in front of the string is a Python raw string literal. It changes the way the string literal is interpreted.
# and help avoid issues like '\' 

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet)
router.register(r'budgets', BudgetViewSet)
router.register(r'goals', SavingsGoalViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('book-recommend/', generate_book_recommendations, name='geminibook')
]


# additional documentation:
#      Expense Endpoints:
#           GET /expenses/ → List all expenses
#           POST /expenses/ → Create a new expense
#           GET /expenses/{id}/ → Retrieve a specific expense
#           PUT /expenses/{id}/ → Update a specific expense
#           DELETE /expenses/{id}/ → Delete a specific expense 
#The same applies to Budget and SavingsGoal endpoints.