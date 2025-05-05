import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

from rest_framework.response import Response

from budget.utils.excel_report_generator import generate_test_excel
from budget.utils.get_data_for_report import get_user_data_for_report


class CategoryReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info("Запрос получен. Параметры: %s", request.query_params)

        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")
        format_type = request.query_params.get("forma")

        report_data = get_user_data_for_report(start_date_str, end_date_str, request.user)

        if format_type == "excel":
            generate_test_excel(report_data)

        return Response(report_data)
