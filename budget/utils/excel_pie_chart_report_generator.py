import os

from openpyxl import Workbook
from openpyxl.chart import PieChart3D, Reference

from .CONF import generate_report_filename


def generate_excel_with_pie_chart(report_data):
    """
    Формат report_data должен быть следующим
        data = [
        ("Type of Expense", "Amount Spent"),
        ("Grocery", 300),
        ("Electricity", 150),
    ]
    """
    wb_pie_chart = Workbook()
    ws_pie_chart = wb_pie_chart.active

    for row in report_data:
        ws_pie_chart.append(row)
    pie = PieChart3D()
    labels = Reference(ws_pie_chart, min_col=1, min_row=2, max_row=7)
    data = Reference(ws_pie_chart, min_col=2, min_row=1, max_row=7)
    pie.add_data(data, titles_from_data=True)
    pie.set_categories(labels)
    pie.title = "Expenditures Pie Chart"

    ws_pie_chart.add_chart(pie, "C10")

    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, generate_report_filename("pie_chart_report"))
    wb_pie_chart.save(filepath)
    print(f"Файл успешно сохранен: {os.path.abspath(filepath)}")
