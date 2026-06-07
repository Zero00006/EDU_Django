from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CategoryForm, TransactionForm, BudgetForm, DateWidgetEvent
from .models import Budget


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
    form_tr = TransactionForm()
    form_bg = BudgetForm()
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
            form_tr = TransactionForm(request.POST)
            form_tr.instance.user = request.user
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
                bg = Budget.objects.filter(category=request.POST.get('category'), date=date)
                if bg.exists():
                    bg = bg.first()
                    bg.amount += amount
                    bg.save()
                    request.POST._mutable = True
                    request.POST.update({'budget': bg})
                    request.POST._mutable = False
                    form_tr = TransactionForm(request.POST)
                    form = form_tr.save(commit=False)
                    form.user = request.user
                    form.save()
                return redirect('finances')
        if button == 'btn_bg':
            form_bg = BudgetForm(request.POST)
            form_bg.instance.user = request.user
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
                objects = Budget.objects.filter(date=sort_date)
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