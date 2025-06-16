import datetime
import random
from django.core.management.base import BaseCommand
from categories.models import Category
from transactions.models import Transaction
from users.models import User
from random_word import RandomWords


class Command(BaseCommand):
    help = "Generates category if not provided and makes a transaction"

    def add_arguments(self, parser):
        parser.add_argument('-c', '--category', type=str, help='Category of a transaction')
        parser.add_argument('-u', '--user', type=str, help='User of a transaction')
        parser.add_argument('-a', '--amount', type=str, help='Transaction amount')
        parser.add_argument('-t', '--type', type=str, help='Type of a transaction')


    def handle(self, *args, **options):
        category_name = options["category"]
        username = options["user"]
        amount = options["amount"]
        type = options["type"]

        if not category_name:
            category_name = (
            f"{RandomWords().get_random_word()}-{random.randint(100, 1000)}"
        )
        user = User.objects.get(username=username)
        if not amount:
            amount = random.uniform(1, 2500)
        category, created = Category.objects.get_or_create(name=category_name)
        year, month, day = datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day
        Transaction.objects.create(
            user=user,
            amount=amount,
            category=category,
            description=f"This is a test transaction with a custom or randomly generated category: {category_name}",
            date=datetime.date(year, month, day),
            type=type,
        )
