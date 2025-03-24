from datetime import datetime
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

        if transaction.type == Transaction.INCOME:
            user.budget += transaction.amount
        elif transaction.type == Transaction.EXPENSE:
            user.budget -= transaction.amount

        user.save()


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


class CategoryReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)

        transactions = Transaction.objects.filter(user=request.user)

        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)

        report = {
            'period': {
                'start': start_date.isoformat() if start_date else None,
                'end': end_date.isoformat() if end_date else None
            },
            'categories': {}
        }

        income_by_category = transactions.filter(type='income').values('category').annotate(
            total=Sum('amount')
        )
        for item in income_by_category:
            report['categories'][item['category']] = {
                'income': float(item['total']),
                'expense': 0.0
            }

        expense_by_category = transactions.filter(type='expense').values('category').annotate(
            total=Sum('amount')
        )
        for item in expense_by_category:
            if item['category'] in report['categories']:
                report['categories'][item['category']]['expense'] = float(item['total'])
            else:
                report['categories'][item['category']] = {
                    'income': 0.0,
                    'expense': float(item['total'])
                }

        report['total'] = {
            'income': sum(cat['income'] for cat in report['categories'].values()),
            'expense': sum(cat['expense'] for cat in report['categories'].values())
        }
        report['total']['balance'] = report['total']['income'] - report['total']['expense']

        return Response(report)
