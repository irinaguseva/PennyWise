from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from rest_framework.views import APIView


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        transaction = serializer.save(user=user)

        # Обновляем бюджет пользователя
        if transaction.type == Transaction.INCOME:
            user.budget += transaction.amount
        elif transaction.type == Transaction.EXPENSE:
            user.budget -= transaction.amount

        user.save()


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Сумма доходов
        total_income = (
            Transaction.objects.filter(user=user, type="income").aggregate(
                Sum("amount")
            )["amount__sum"]
            or 0
        )

        # Сумма расходов
        total_expense = (
            Transaction.objects.filter(user=user, type="expense").aggregate(
                Sum("amount")
            )["amount__sum"]
            or 0
        )

        # Текущий баланс
        balance = total_income - total_expense

        return Response(
            {
                "total_income": total_income,
                "total_expense": total_expense,
                "balance": balance,
            },
            status=status.HTTP_200_OK,
        )
