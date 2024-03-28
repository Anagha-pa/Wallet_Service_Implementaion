from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework import exceptions
from apps.common.serializers import PaginatedSerializer
# Create your views here.

API_PAGE_COUNT_DEFAULT = getattr(settings, 'API_PAGE_COUNT_DEFAULT', 25)
API_PAGE_COUNT_MAX = getattr(settings, 'API_PAGE_COUNT_MAX', 25)



class WalletBalance(APIView):
    permission_classes = (IsAuthenticated)
    serializer_class = WalletSerializer

    def post(self, request):
        wallet = request.user.get_wallet()
        data = {}
        if wallet:
            data = self.serializer_class(wallet).data
            return Response(data=data, status=True, status_code=status.HTTP_200_OK)


class DepositAmount(APIView):
    permission_classes = (IsAuthenticated)

    def post(self, request):
        amount = request.data.get('amount', None)
        success, error_msg, data = True, None, {}
        
        if (not amount) or (amount<=0):
            success = False
            error_msg = "Invalid amount"
        
        if success:
            wallet = request.user.get_wallet()

            if not wallet:
                success = False
                error_msg = "Wallet doesnot exist for user"

        if success:
            with transaction.atomic():
                wallet.deposit(amount)
            data = WalletSerializer(wallet).data
        return Response(
            data=data,
            error_msg=error_msg,
            status=success,
            status_code=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        )
        


class WithdrawAmount(APIView):
    permission_classes = (IsAuthenticated)

    def post(self, request):
        amount = request.data.get('amount', None)
        success, error_msg, data = True, None, {}

        if (not amount) or (amount<=0):
            success = False
            error_msg = "Invalid amonut"

        if success:
            wallet = request.user.get_wallet()

            if not wallet:
                success = False
                error_msg = "Wallet does not exist for user."
        if success:
            wallet.withdraw(amount)
            data = WalletSerializer(wallet).data
        
        return Response(
            data=data,
            error_msg=error_msg,
            status=success,
            status_code=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        )


class GetMiniStatement(APIView):
    permission_classes = (IsAuthenticated)
    serializer_class = MiniStatementSerializer

    def post(self, request):
        wallet = request.user.get_wallet()
        data = {}

        if wallet:
            data = self.serializer_class(wallet).data
        return Response(
            data=data,
            status=True,
            status_code=status.HTTP_200_OK
        )
    


class ListTransactions(APIView):
    permission_classes = (IsAuthenticated)
    serializer_class = TransactionSerializer

    def post(self,request,pk):
        if request.user.is_staff:
            transactions = Transaction.objects.filter(wallet_id=pk).order_by('-timestamp_created')
        else:
            wallet = request.user.get_wallet()
            if not wallet:
                raise exceptions.APIException("Wallet nit found")
            if wallet.id != pk:
                raise exceptions.PermissionDenied()
            
            transactions = wallet.transaction_set.order_by('-timestamp_created')
        
        count = int(request.GET.get('count', API_PAGE_COUNT_DEFAULT))
        page = int(request.GET.get('page', 1))

        data = PaginatedSerializer(
            queryset=transactions,
            num=min(count, API_PAGE_COUNT_MAX),
            page=page,
            serializer_method=self.serializer_class
        ).data

        return Response(data=data, status=True, status_code=status.HTTP_200_OK)

            
