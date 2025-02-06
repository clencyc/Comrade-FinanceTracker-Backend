from django.urls import path
from .views import fetch_transaction_status, generate_insights, mpesa_token_view

urlpatterns = [
    path('transaction-status/<str:transaction_id>/', fetch_transaction_status, name='fetch_transaction_status'),
    path('insights/', generate_insights, name='generate_insights'),
    path("token/", mpesa_token_view, name="mpesa_token"),
]