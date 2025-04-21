import logging
from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from transactions.models import Transaction

logger = logging.getLogger(__name__)

from rest_framework.response import Response

from budget.utils.excel_report_generator import generate_test_excel


class CategoryReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info("Запрос получен. Параметры: %s", request.query_params)

        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")
        format_type = request.query_params.get("forma")

        start_date = (
            datetime.strptime(start_date_str, "%Y-%m-%d").date()
            if start_date_str
            else None
        )
        end_date = (
            datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
        )

        report_data = {
            "period": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None,
            },
            "categories": {},
            "total": {"income": 0, "expense": 0, "balance": 0},
        }

        transactions = Transaction.objects.filter(
            user=request.user, date__gte=start_date, date__lte=end_date
        )

        for transaction in transactions:
            category_name = (
                transaction.category.name if transaction.category else "Uncategorized"
            )
            if category_name not in report_data["categories"]:
                report_data["categories"][category_name] = {"income": 0, "expense": 0}

            if transaction.type == Transaction.INCOME:
                report_data["categories"][category_name]["income"] += transaction.amount
                report_data["total"]["income"] += transaction.amount
            else:
                report_data["categories"][category_name][
                    "expense"
                ] += transaction.amount
                report_data["total"]["expense"] += transaction.amount

        report_data["total"]["balance"] = (
            report_data["total"]["income"] - report_data["total"]["expense"]
        )

        if format_type == "excel":
            generate_test_excel(report_data)

        return Response(report_data)
