from calendar import month

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models import DecimalField, DateField
from django.utils import timezone
# Create your models here.


class Category(models.Model):
    name = models.CharField('Название категории',
                            max_length=50)
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'name')
        ordering = ['-name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    def clean(self):
        if Category.objects.filter(name=self.name, user=self.user).exists():
            raise ValidationError("Категория с таким названием существует")

    def __str__(self):
        return f"{self.name}"


class Transaction(models.Model):
    TYPE_CHOICES = [
                    ('income', 'Доход'),
                    ('expense', 'Расход')
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 related_name='transactions',
                                 verbose_name= 'Категория')
    amount = models.DecimalField('Сумма', max_digits=10,
                                 decimal_places=2, default=0)
    description = models.CharField('Комментарий', max_length=200,
                                   blank=True)
    date = models.DateField('Дата',
                            default=timezone.now)
    type = models.CharField('Тип', max_length=10,
                            choices=TYPE_CHOICES)

    class Meta:
        ordering = ('-id', '-amount')
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return (f"id:{self.id}, user_id:{self.user}, category:{self.category},"
                f" amount:{self.amount}, description:{self.description}, date:{self.date}")

class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    amount = DecimalField('Бюджет', max_digits=10,
                                 decimal_places=2, default=0)
    date = DateField('Год/Месяц', default=timezone.now)

    class Meta:
        unique_together = (('user', 'category'), ('date', 'category'))
        verbose_name = 'Бюджет'
        verbose_name_plural = 'Бюджеты'
    def __str__(self):
        return f"id:{self.id}, user_id:{self.user}, category:{self.category}, amount:{self.amount}"
    def clean(self):
        category = self.category
        user = self.user
        date = self.date
        if (Budget.objects.filter(category=category, user=user).exists()
                and Budget.objects.filter(category=category, date=date).exists()):
            raise ValidationError("Бюджет данной категории в этом месяце существует")