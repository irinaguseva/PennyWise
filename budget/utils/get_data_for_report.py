import logging
from datetime import datetime

from transactions.models import Transaction

logger = logging.getLogger(__name__)


def get_user_data_for_report(start_date_str, end_date_str, current_user):
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
            user=current_user, date__gte=start_date, date__lte=end_date
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

        return report_data