from rest_framework import serializers
from ..models import *

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'name', 'balance')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'running_balance', 'timestam_created')  


class MiniStatementSerializer(serializers.ModelSerializer):

    recent_transactions = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ('name', 'balance', 'recent_transactions')   

        def get_recent_transactions(self, wallet):
            return TransactionSerializer(
                wallet.transaction_set.order_by('-timestamp_created')[:10],many=True
            ).data
            
