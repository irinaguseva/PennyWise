from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer

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