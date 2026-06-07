from tabnanny import verbose

from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import SelectDateWidget, HiddenInput
import datetime

from . import models

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
        fields = ('amount', 'category', 'date', 'description', 'type', 'budget')
        widgets = {
            'type': HiddenInput(),
            'budget': HiddenInput(),
            'date': SelectDateWidget,
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = models.Budget
        fields = ('category', 'amount', 'date')
        widgets = {
            'date': MonthYearWidget(),
        }

class DateWidgetEvent(forms.Form):
    date = forms.DateField(widget=MonthYearWidget(),
                           initial=datetime.date.today(),
                           label="Сортировка по дате")