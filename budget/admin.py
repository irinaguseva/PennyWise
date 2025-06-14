from django.contrib import admin
from categories.models import Category
from transactions.models import Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    list_filter = ("user",)
    search_fields = ("name",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "category", "type", "date", "description")
    list_filter = ("user", "type", "category")
    search_fields = ("description",)
