from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .forms import (CategoryForm, TransactionForm, BudgetForm,
                    DateWidgetEvent, BudgetWidgetEvent)
from .models import Budget, Transaction


def index(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('index')
    else:
        return redirect('index')


@login_required(login_url='login')
def finances(request):
    form_cat = CategoryForm()
    form_tr = TransactionForm(user=request.user)
    form_bg = BudgetForm(user=request.user)
    form_sort = DateWidgetEvent()
    if request.method == 'POST':
        button = request.POST.get('submit')
        if button == 'btn_cat':
            form_cat = CategoryForm(request.POST)
            form_cat.instance.user = request.user
            if form_cat.is_valid():
                form = form_cat.save(commit=False)
                form.save()
                return redirect('finances')
        if button == 'btn_tr':
            form_tr = TransactionForm(request.POST, user=request.user)
            print(form_tr.is_valid())
            if form_tr.is_valid():
                amount = int(form_tr.instance.amount)
                if amount < 0:
                    request.POST._mutable = True
                    request.POST.update({'type': 'Расход'})
                    request.POST._mutable = False

                else:
                    request.POST._mutable = True
                    request.POST.update({'type': 'Доход'})
                    request.POST._mutable = False
                date = form_tr.instance.date
                date = str(date)[:-2] + '01'
                bg = Budget.objects.filter(category=request.POST.
                                           get('category'), date=date)
                if bg.exists():
                    bg = bg.first()
                    request.POST._mutable = True
                    request.POST.update({'budget': bg})
                    request.POST._mutable = False
                    form_tr = TransactionForm(request.POST, user=request.user)
                    if form_tr.is_valid():
                        form_tr.instance.user = request.user
                        form_tr.save()
                        bg.current = bg.amount
                        trs = Transaction.objects.filter(budget=request.
                                                         POST['budget'])
                        for transaction in trs:
                            bg.current += transaction.amount
                        (Budget.objects.filter(pk=bg.id).
                         update(current=bg.current))
                    return redirect('finances')
        if button == 'btn_bg':
            form_bg = BudgetForm(request.POST)
            form_bg.instance.user = request.user
            form_bg.instance.current = form_bg.instance.amount
            if form_bg.is_valid():
                form = form_bg.save(commit=False)
                form.save()
                return redirect('finances')
        if button == 'btn_sort':
            form_sort = DateWidgetEvent(request.POST)
            if form_sort.is_valid():
                sort_date = form_sort.cleaned_data['date']
                sort_date.strftime('%Y-%m-%d')
                sort_date = str(sort_date)[:-2] + '01'
                objects = Budget.objects.filter(date=sort_date,
                                                user=request.user)
                return render(request, 'finances.html',
                              {'form_cat': form_cat,
                               'form_tr': form_tr,
                               'form_bg': form_bg,
                               'objects': objects,
                               'form_sort': form_sort})
    return render(request, 'finances.html',
                  {'form_cat': form_cat,
                   'form_tr': form_tr,
                   'form_bg': form_bg,
                   'form_sort': form_sort,
                   })


@login_required(login_url='login')
def transactions(request):
    form_sort_tr = BudgetWidgetEvent(user=request.user)
    if request.method == 'POST':
        button = request.POST.get('submit')
        if button == 'btn_sort_tr':
            form_sort_tr = BudgetWidgetEvent(request.POST, user=request.user)
            if form_sort_tr.is_valid():
                print(form_sort_tr.cleaned_data)
                sort_date = form_sort_tr.data['budget']
                transac = Transaction.objects.filter(budget=sort_date)
                return render(request, 'transactions.html',
                              {"form_sort_tr": form_sort_tr,
                               "transac": transac})
    return render(request, 'transactions.html', {'form_sort_tr': form_sort_tr})


@require_http_methods(['POST'])
@login_required(login_url='login')
def delete_budget(request, pk):
    item = get_object_or_404(Budget, pk=pk)
    item.delete()
    return redirect('finances')


@require_http_methods(['POST'])
@login_required(login_url='login')
def delete_transaction(request, pk):
    item = get_object_or_404(Transaction, pk=pk)
    item.delete()
    return redirect('transactions')
