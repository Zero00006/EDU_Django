from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CategoryForm, TransactionForm
from .models import Category


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
            return redirect('index')
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
    if request.method == 'POST':
        form_cat = CategoryForm(request.POST)
        form_tr = TransactionForm(request.POST)
        if form_cat.is_valid():
            form = form_cat.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('finances')
        if form_tr.is_valid():
            amount = int(request.POST.get('amount'))
            if amount < 0:
                request.POST._mutable = True
                request.POST.update({'type':'expense'})
                request.POST._mutable = False

            else:
                request.POST._mutable = True
                request.POST.update({'type': 'income'})
                request.POST._mutable = False
            cat = Category.objects.get(pk=request.POST.get('category'))
            cat.amount += amount
            cat.save()
            form = form_tr.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('finances')
    return render(request, 'finances.html', {'form_cat': form_cat, 'form_tr': form_tr})