from django.urls import path
from .views import * 

urlpatterns = [
    path('balance/', WalletBalance.as_view(), name='balance'),
    path('withdraw/', WithdrawAmount.as_view(), name='withdraw'),
    path('deposit/', DepositAmount.as_view(), name='deposit'),
    path('statement/', GetMiniStatement.as_view(), name='get-mini-statement'),
    path('transactions/<int:pk>/',ListTransactions.as_view, name='list-all-transactions')
]