import datetime
import random
from django.core.management.base import BaseCommand
from budget.models import Category, User, Transaction


class Command(BaseCommand):
    help = "Generates transactions for testing"

    def add_arguments(self, parser):
        parser.add_argument('-u', '--user', type=str, help='User that makes a transaction')

    def handle(self, *args, **options):
        user_name = options['user']

        user = User.objects.get(username=user_name)  # example username, set yours
        categories = Category.objects.filter(user=user)
        types = ["income", "expense"]
        for i in range(len(categories)):
            Transaction.objects.create(
                user=user,
                amount=random.uniform(1, 2500),
                category=categories[i],
                description="This transaction was created for test purposes.",
                date=datetime.date(2025, 3, 20),
                type=types[i % 2],
            )
