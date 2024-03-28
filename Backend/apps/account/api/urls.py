from django.urls import path
from .views import ListAccounts


urlpatterns = [
    #List all registered accounts
    path('list-accounts', ListAccounts.as_view(), name='list-accounts')

    
]