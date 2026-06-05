from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data= request.POST)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            return redirect('index.html')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})