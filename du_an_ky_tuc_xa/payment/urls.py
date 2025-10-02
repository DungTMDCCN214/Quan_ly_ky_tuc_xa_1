# payment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('create/', views.payment_create, name='payment_create'),
    path('<int:pk>/', views.payment_detail, name='payment_detail'),
    path('<int:pk>/update/', views.payment_update, name='payment_update'),
    path('<int:pk>/send-reminder/', views.send_reminder, name='send_reminder'),
]