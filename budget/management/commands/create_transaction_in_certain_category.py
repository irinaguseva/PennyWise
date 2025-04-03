import datetime
import random
from unicodedata import category

from django.core.management.base import BaseCommand

from budget.models import Category, Transaction, User


class Command(BaseCommand):
    help = "This is a tool for generating a transaction of specific category"

    def add_arguments(self, parser):
        parser.add_argument(
            "-c", "--category", type=str, help="Category of a transaction"
        )
        parser.add_argument("-u", "--user", type=str, help="User of a transaction")

    def handle(self, *args, **options):
        category = options["category"]
        user = options["user"]

        user = User.objects.get(username=user)
        category = Category.objects.get(name=category)
        types = ["income", "expense"]
        year, month, day = (
            datetime.datetime.now().year,
            datetime.datetime.now().month,
            datetime.datetime.now().day,
        )

        Transaction.objects.create(
            user=user,
            amount=random.uniform(1, 2500),
            category=category,
            description="This is a test transaction for a specific category",
            date=datetime.date(year, month, day),
            type=types[random.randint(0, 1)],
        )
