from django.contrib import admin

from finance_manager.models import Category, Transaction, Budget


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id', 'created_at')
    list_filter = ['created_at']
    search_fields = ('name', 'user_id')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'type', 'amount', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('id', 'user_id')


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'amount', 'month')
    sortable_by = ('amount', 'month')
    search_fields = ['user_id']
