from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .tools.get_financial_data import get_total_by_type
from categories.models import Category


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        category_name = request.query_params.get("category")

        total_income = get_total_by_type(user=user, transaction_type="income")
        total_expense = get_total_by_type(user=user, transaction_type="expense")
        balance = total_income - total_expense

        response_body = {
                "total_income": total_income,
                "total_expense": total_expense,
                "balance": balance,
            }
        if category_name:
            category = Category.objects.get(name=category_name)
            total_expense_by_cat = get_total_by_type(user=user, transaction_type="expense", category=category)
            response_body[f"total_expense_in_category_{category_name}"] = total_expense_by_cat
            total_income_by_cat = get_total_by_type(user=user, transaction_type="income", category=category)
            response_body[f"total_income_in_category_{category_name}"] = total_income_by_cat

        return Response(
            response_body,
            status=status.HTTP_200_OK,
        )
