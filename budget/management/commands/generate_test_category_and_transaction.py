import datetime
import random
from django.core.management.base import BaseCommand
from budget.models import Category, User, Transaction
from random_word import RandomWords


class Command(BaseCommand):
    help = "Generates category and transaction"

    def handle(self, *args, **options):
        random_category_name = (
            f"{RandomWords().get_random_word()}-{random.randint(100, 1000)}"
        )
        user = User.objects.get(username="ira")
        new_category = Category.objects.create(name=random_category_name, user=user)
        types = ["income", "expense"]
        Transaction.objects.create(
            user=user,
            amount=random.uniform(1, 2500),
            category=new_category,
            description="This is a test transaction with a randomly generated category",
            date=datetime.date(2025, 3, 22),
            type=types[random.randint(0, 1)],
        )
