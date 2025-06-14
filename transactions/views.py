from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from transactions.models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        transaction = serializer.save(user=user)

        if transaction.type == Transaction.INCOME:
            user.budget += transaction.amount
        elif transaction.type == Transaction.EXPENSE:
            user.budget -= transaction.amount

        user.save()
