from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('finances/', views.finances, name='finances'),
    path('transactions/', views.transactions, name='transactions'),
    path('finances/delete/<int:pk>/', views.delete_budget,
         name='delete_budget'),
    path('transactions/delete/<int:pk>/', views.delete_transaction,
         name='delete_transaction'),
]
