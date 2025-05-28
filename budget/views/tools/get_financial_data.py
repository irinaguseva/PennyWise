from django.db.models import Sum
from transactions.models import Transaction


def get_total_by_type(user, tx_type):
    return (
            Transaction.objects.filter(user=user, type=tx_type)
            .aggregate(total=Sum("amount"))
            .get("total") or 0
    )