# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User
# admin.site.register(User, UserAdmin)

from django.contrib import admin
from .models import Category, Transaction


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
