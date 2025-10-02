
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('student/register/', views.student_register, name='student_register'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/complete-profile/', views.student_complete_profile, name='student_complete_profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]