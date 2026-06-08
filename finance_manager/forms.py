from tabnanny import verbose

from django import forms
from django.forms.widgets import SelectDateWidget, HiddenInput
import datetime

from . import models
from .models import Budget, Transaction


class MonthYearWidget(forms.SelectDateWidget):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['subwidgets'][0]['attrs']['style'] = 'display: none;'
        context['widget']['subwidgets'][0]['attrs']['type'] = 'hidden'
        context['widget']['subwidgets'][0]['attrs']['value'] = '01'
        return context

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ('name',)

class TransactionForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = models.Category.objects.filter(user=user)
    class Meta:
        model = models.Transaction
        fields = ('amount', 'category', 'date', 'description', 'type', 'budget')
        widgets = {
            'type': HiddenInput(),
            'budget': HiddenInput(),
            'date': SelectDateWidget,
        }

class BudgetForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = models.Category.objects.filter(user=user)
    class Meta:
        model = models.Budget
        fields = ('category', 'amount', 'date', 'current')
        widgets = {
            'current': HiddenInput(),
            'date': MonthYearWidget(),
        }

class DateWidgetEvent(forms.Form):
    date = forms.DateField(widget=MonthYearWidget(),
                           initial=datetime.date.today(),
                           label="Сортировка по дате")
class BudgetWidgetEvent(forms.Form):
    budget = forms.ModelChoiceField(queryset=None, label='Сортирвка по бюджету')
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['budget'].queryset = models.Budget.objects.filter(user=user)