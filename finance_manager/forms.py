from django import forms

from finance_manager.models import Category, Transaction, Budget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'user_id')
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('amount', 'type', 'category', 'date', 'description')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super.__init__(*args, **kwargs)
            if user:
                self.fields['category'].queryset = Category.objects.filter(user=user)

            self.fields['category'].required = False

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ('user_id', 'category','amount', 'month')
        widgets = {
            'month': forms.Select(attrs={'class': 'datepicker'}),
        }