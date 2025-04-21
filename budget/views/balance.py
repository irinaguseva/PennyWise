from django.db.models import Sum
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.models import Transaction


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        total_income = (
            Transaction.objects.filter(user=user, type="income").aggregate(
                Sum("amount")
            )["amount__sum"]
            or 0
        )

        total_expense = (
            Transaction.objects.filter(user=user, type="expense").aggregate(
                Sum("amount")
            )["amount__sum"]
            or 0
        )

        balance = total_income - total_expense

        return Response(
            {
                "total_income": total_income,
                "total_expense": total_expense,
                "balance": balance,
            },
            status=status.HTTP_200_OK,
        )
