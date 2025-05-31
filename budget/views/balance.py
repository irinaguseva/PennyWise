from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .tools.get_financial_data import get_total_by_type


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        total_income = get_total_by_type(user=user, transaction_type="income")
        total_expense = get_total_by_type(user=user, transaction_type="expense")

        balance = total_income - total_expense

        return Response(
            {
                "total_income": total_income,
                "total_expense": total_expense,
                "balance": balance,

            },
            status=status.HTTP_200_OK,
        )
