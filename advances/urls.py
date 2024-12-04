from django.urls import path
from . import views

urlpatterns = [
    path('portfolio/', views.portfolio, name='portfolio'),
    path('apply-loan/', views.apply_loan, name='apply_loan'),
    path('loan-status/<int:loan_id>/', views.loan_status, name='loan_status'),
]