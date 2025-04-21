from django.db.models import Sum

from categories.models import Category
from transactions.models import Transaction


def get_user_financial_data(user, start_date, end_date):

    income = (
        Transaction.objects.filter(
            user=user,
            type=Transaction.INCOME,
            date__gte=start_date,
            date__lte=end_date,
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    expenses = (
        Transaction.objects.filter(
            user=user,
            type=Transaction.EXPENSE,
            date__gte=start_date,
            date__lte=end_date,
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    balance = income - expenses

    categories = Category.objects.filter(user=user)
    category_expenses = []

    for category in categories:
        amount = (
            Transaction.objects.filter(
                user=user,
                category=category,
                type=Transaction.EXPENSE,
                date__gte=start_date,
                date__lte=end_date,
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        if amount > 0:
            category_expenses.append(
                {
                    "category": category.name,
                    "amount": float(amount),
                    "percentage": (
                        float(amount) / float(expenses) * 100 if expenses else 0
                    ),
                }
            )

    return {
        "balance": float(balance),
        "income": float(income),
        "expenses": float(expenses),
        "category_expenses": sorted(
            category_expenses, key=lambda x: x["amount"], reverse=True
        ),
        "period": {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        },
    }
