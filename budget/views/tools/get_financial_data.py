from django.db.models import Sum

from transactions.models import Transaction


def get_total_by_type(user, transaction_type, category=None):
    filters = {
        "user": user,
        "type": transaction_type,
    }
    if category is not None:
        filters["category"] = category

    return (
        Transaction.objects.filter(**filters)
        .aggregate(total=Sum("amount"))
        .get("total")
        or 0
    )
