from django.db import models
from apps.common.models import BaseModel
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import transaction, IntegrityError
from decimal import Decimal


# Create your models here.


class Wallet(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='wallet')
    name = models.CharField(_('Name'), max_length=255, unique=True, default='default',help_text=_('Name of the Wallet'))
    balance = models.DecimalField(_('Wallet Balance'), max_digits=10, decimal_places=2, default=0)

    @transaction.atomic
    def deposit(self, amount):
        amount = Decimal(amount)
        self.transaction_set.create(
            amount=amount,
            running_balance=self.balance + amount
        )
        self.balance += amount
        self.save()

    @transaction.atomic
    def withdraw(self, amount):
        amount = Decimal(amount)
        if amount > self.balance:
            raise IntegrityError("Insufficient Balance")
        self.transaction_set.create(
            amount=-amount,
            running_balance=self.balance - amount
        )
        self.balance -= amount
        self.save()

    class Meta:
        unique_together = [['user', 'name']]

    
    def __str__(self):
        return self.name
        


class Transaction(BaseModel):
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2, default=0)
    running_balance = models.DecimalField(_('Wallet Balance at the thime of transaction'), max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.wallet.name
    
        

