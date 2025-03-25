import random
import datetime
from budget.models import User, Transaction, Category
from django.core.management.base import BaseCommand
from random_word import RandomWords


class Command(BaseCommand):
    help = "This is a script for generating a user, a category and a transaction."

    def handle(self, *args, **options):
        new_user = User.objects.create(
            username=f"test-user-{RandomWords().get_random_word()}"
        )
        new_category = Category.objects.create(
            name=f"test-category-{RandomWords().get_random_word()}", user=new_user
        )
        types = ["income", "expense"]
        Transaction.objects.create(
            user=new_user,
            amount=random.uniform(1, 2500),
            category=new_category,
            description="This is a test transaction for checking user creation",
            date=datetime.date(2025, 3, 22),
            type=types[random.randint(0, 1)],
        )
