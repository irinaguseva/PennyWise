import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

from rest_framework.response import Response

from budget.utils.excel_pie_chart_report_generator import \
    generate_excel_with_pie_chart
from budget.utils.excel_report_generator import generate_excel_report
from budget.utils.get_data_for_report import get_user_data_for_report


class CategoryReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info("Запрос получен. Параметры: %s", request.query_params)

        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")
        format_type = request.query_params.get("forma")
        plot_type = request.query_params.get("plot")

        report_data = get_user_data_for_report(start_date_str, end_date_str, request.user)

        if format_type == "excel" and plot_type == "table":
            generate_excel_report(report_data)
        elif format_type == "excel" and plot_type == "pie":
            income_data, expense_data = self._prepare_data_for_pie_report(report_data)
            generate_excel_with_pie_chart(income_data, expense_data)

        return Response(report_data)

    def _prepare_data_for_pie_report(self, report_data):
        income_data = [("Type of Income", "Amount Received")]
        for cat in report_data["categories"]:
            income_data.append((cat, int(report_data["categories"][cat]["income"])))
        expense_data = [("Type of Expense", "Amount Spent")]
        for cat in report_data["categories"]:
            expense_data.append((cat, int(report_data["categories"][cat]["expense"])))
        return income_data, expense_data
