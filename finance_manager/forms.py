from django import forms
from django.core.exceptions import ValidationError

from . import models


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ('name', 'amount')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    def clean(self):
        name = getattr(self, 'name', None)
        if models.Category.objects.filter(user=self.user, name=name).exists():
            self.add_error('name', ValidationError("Название данной категории уже используется"))
        return name

class TransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ('amount', 'category', 'date', 'description')