import logging
from datetime import datetime

from django.db.models import Sum
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.views import APIView

from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer

logger = logging.getLogger(__name__)

from django.http import HttpResponse
from rest_framework.response import Response

from .test_xl import generate_test_excel


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


class CategoryReportView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]  # Явно указываем renderers
    parser_classes = [JSONParser]

    def get(self, request):
        # Получаем параметры запроса
        logger.info("Запрос получен. Параметры: %s", request.query_params)

        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        format_type = request.query_params.get('forma')

        # Парсим даты
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

        # Формируем отчет
        report_data = {
            "period": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None,
            },
            "categories": {},
            "total": {"income": 0, "expense": 0, "balance": 0}
        }

        # Заполняем данные
        transactions = Transaction.objects.filter(
            user=request.user,
            date__gte=start_date,
            date__lte=end_date
        )

        for transaction in transactions:
            category_name = transaction.category.name if transaction.category else "Uncategorized"
            if category_name not in report_data['categories']:
                report_data['categories'][category_name] = {"income": 0, "expense": 0}

            if transaction.type == Transaction.INCOME:
                report_data['categories'][category_name]['income'] += transaction.amount
                report_data['total']['income'] += transaction.amount
            else:
                report_data['categories'][category_name]['expense'] += transaction.amount
                report_data['total']['expense'] += transaction.amount

        report_data['total']['balance'] = report_data['total']['income'] - report_data['total']['expense']

        if format_type == 'excel':
            buffer = generate_test_excel(report_data)
            #buffer = generate_category_report_excel(report_data)
            response = HttpResponse(
                buffer.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            filename = f"report_{report_data['period']['start']}_to_{report_data['period']['end']}.xlsx"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        return Response(report_data)



