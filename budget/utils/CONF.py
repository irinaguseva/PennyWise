from datetime import datetime


def generate_report_filename(report_name):
    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    time_str = now.strftime("%H-%M-%S")
    filename = f"{report_name}_{date_str}_{time_str}.xlsx"
    return filename