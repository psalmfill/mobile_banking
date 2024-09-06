from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transfer/', views.transfer, name='transfer'),
    path('bill_payment/', views.bill_payment, name='bill_payment'),
    path('account_management/', views.account_management, name='account_management'),
    path('customer_support/', views.customer_support, name='customer_support'),
]
