from django.db.models import Sum
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.models import Transaction
from .tools.get_financial_data import get_total_by_type


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # def get_total_by_type(user, tx_type):
        #     return (
        #             Transaction.objects.filter(user=user, type=tx_type)
        #             .aggregate(total=Sum("amount"))
        #             .get("total") or 0
        #     )

        total_income = get_total_by_type(user=user, tx_type="income")
        total_expense = get_total_by_type(user=user, tx_type="expense")

        balance = total_income - total_expense

        return Response(
            {
                "total_income": total_income,
                "total_expense": total_expense,
                "balance": balance,
            },
            status=status.HTTP_200_OK,
        )
