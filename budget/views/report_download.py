from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from budget.utils.excel_report_generator import generate_excel_report
from budget.utils.get_data_for_report import get_user_data_for_report


class ReportDownloadView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):

        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        report_data = get_user_data_for_report(start_date_str, end_date_str, request.user)

        file_path = generate_excel_report(report_data)

        response = FileResponse(
        open(file_path, 'rb'),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="IRA_TEST1.xlsx"'
        return response