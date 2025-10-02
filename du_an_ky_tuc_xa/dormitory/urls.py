# dormitory/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/create/', views.room_create, name='room_create'),
    path('rooms/<int:pk>/edit/', views.room_update, name='room_edit'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),

    path('buildings/', views.building_list, name='building_list'),
    path('buildings/create/', views.building_create, name='building_create'),
    path('buildings/<int:pk>/edit/', views.building_update, name='building_edit'),
    path('buildings/<int:pk>/delete/', views.building_delete, name='building_delete'),

    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_update, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    path('contracts/', views.contract_list, name='contract_list'),
    path('contracts/create/', views.contract_create, name='contract_create'),
    path('contracts/<int:pk>/edit/', views.contract_update, name='contract_edit'),
    path('contracts/<int:pk>/delete/', views.contract_delete, name='contract_delete'),

    path('reports/', views.reports, name='reports'),

   
    path('export/rooms/pdf/', views.export_rooms_pdf, name='export_rooms_pdf'),
    path('export/rooms/excel/', views.export_rooms_excel, name='export_rooms_excel'),
    path('export/students/excel/', views.export_students_excel, name='export_students_excel'),

    path('rooms/<int:room_id>/book/', views.room_booking, name='room_booking'), 

     path('accounts/login/', auth_views.LoginView.as_view(template_name='dormitory/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]