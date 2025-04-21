# from django.db import models
# from users.models import User
# from categories.models import Category
#
#
# # class Category(models.Model):
# #     name = models.CharField(max_length=100)
# #     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
# #
# #     def __str__(self):
# #         return self.name
#
# class Transaction(models.Model):
#     INCOME = 'income'
#     EXPENSE = 'expense'
#     TYPE_CHOICES = [
#         (INCOME, 'Income'),
#         (EXPENSE, 'Expense'),
#     ]
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
#     description = models.TextField(blank=True)
#     date = models.DateField()
#     type = models.CharField(max_length=10, choices=TYPE_CHOICES)
#
#     def __str__(self):
#         return f"{self.type} - {self.amount}"