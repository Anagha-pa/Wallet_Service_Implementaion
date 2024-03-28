from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from apps.common.admin import NonEditableAdmin,NonEditableTabularInlineAdmin
from .models import Wallet,Transaction
# Register your models here.


class TransactionInline(NonEditableTabularInlineAdmin):
    model = Transaction
    min_num = 0
    extra = 0
    max_num = 100

    fields = ['id', 'timestamp_created', 'amount', 'running_balance']
    readonly_fields = ['timestamp_created']

    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-timestamp_created')
    

@admin.register(Wallet)
class WalletAdmin(NonEditableAdmin):
    list_display = ('id', 'user', 'name', 'balance')

    inlines = [TransactionInline]

    def has_add_permission(self, request, obj=None):
        return True