from io import BytesIO
from reportlab.lib import colors, pdfencrypt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_category_report_pdf(report_data):
    # 1. Создаем буфер и настраиваем метаданные PDF
    buffer = BytesIO()

    # --- Добавляем эту часть ---
    enc = pdfencrypt.StandardEncryption("", canPrint=1, canModify=1)
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        title="Financial Report",
        author="PennyWise",
        encrypt=enc  # Опционально (можно удалить, если защита не нужна)
    )
    # --------------------------

    # 2. Создаем элементы PDF (заголовки, таблицы)
    styles = getSampleStyleSheet()
    elements = []

    # Заголовок
    elements.append(Paragraph("Financial Report", styles['Title']))

    # Таблица с данными
    data = [["Category", "Income", "Expense", "Balance"]]
    for category, values in report_data['categories'].items():
        data.append([
            category,
            f"${values['income']:.2f}",
            f"${values['expense']:.2f}",
            f"${values['income'] - values['expense']:.2f}"
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))

    elements.append(table)

    # 3. Генерируем PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer