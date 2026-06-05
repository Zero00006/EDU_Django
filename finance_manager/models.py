from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    TYPE_CHOICES = [('income', 'Доход'),
                    ('expense', 'Расход')]
    name = models.CharField('Название', max_length=50)
    type = models.CharField('Тип', max_length=10, choices=TYPE_CHOICES)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['name', 'user_id', 'type']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Transaction(models.Model):
    TYPE_CHOICES = [('income', 'Доход'),
                    ('expense', 'Расход')]
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='transactions')
    amount = models.DecimalField('Сумма транзакции', max_digits=10, decimal_places=2)
    description = models.CharField('Описание транзакции', max_length=250, blank=True)
    date = models.DateField('Дата транзакции', default = timezone.now)
    type = models.CharField('Тип', max_length=10, choices = TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date', '-created_at',)
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
