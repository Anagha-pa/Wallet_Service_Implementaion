from rest_framework import serializers
from ..models import UserAccount
from apps.wallet.api.serializers import WalletSerializer


class AccountSerializer(serializers.ModelSerializer):

    wallet = serializers.SerializerMethodField

    class Meta:
        model = UserAccount
        fields = (
            'id', 'first_name', 'last_name', 'last_login', 
            'is_active', 'date_joined', 'email', 'wallet'  
        )
    
    def get_wallet(self,account):
        return WalletSerializer(
            account.wallet).data if hasattr(account, 'wallet') else {}