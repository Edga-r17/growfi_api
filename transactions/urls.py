from django.urls import path
from transactions.views import TransactionCreateView, TransactionSummaryView

urlpatterns = [
    path('transacciones/', TransactionCreateView.as_view(), name='TransactionCreateView'),
    path('resumen/<int:user_id>/', TransactionSummaryView.as_view(), name='TransactionSummaryView'),
]