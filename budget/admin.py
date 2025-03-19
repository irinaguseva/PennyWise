# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User
# admin.site.register(User, UserAdmin)

from django.contrib import admin
from .models import Category, Transaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')  # Поля, которые будут отображаться в списке
    list_filter = ('user',)  # Фильтр по пользователю
    search_fields = ('name',)  # Поиск по названию

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'category', 'type', 'date')
    list_filter = ('user', 'type', 'category')
    search_fields = ('description',)