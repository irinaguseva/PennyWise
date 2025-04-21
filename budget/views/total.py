from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from categories.models import Category
from transactions.models import Transaction


class CategoryTotalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        category_ex = Category.objects.get(name=category)
        income = (
            Transaction.objects.filter(
                user=request.user, type="income", category=category_ex
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        expense = (
            Transaction.objects.filter(
                user=request.user, type="expense", category=category_ex
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        last_transaction = Transaction.objects.filter(
            user=request.user, category=category_ex
        ).order_by("-date")[:1]

        response_data = {
            "transaction": category,
            "income_in_category": float(income),
            "expense_in_category": float(expense),
            "total": float(income - expense),
            "last_transaction_in_category": [
                {
                    "type": t.type,
                    "amount": t.amount,
                    "description": t.description,
                    "date": t.date,
                }
                for t in last_transaction
            ],
        }

        return Response(response_data)
