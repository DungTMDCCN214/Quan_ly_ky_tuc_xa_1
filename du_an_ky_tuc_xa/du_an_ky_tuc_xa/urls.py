
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

# Temporary views for testing
def home_view(request):
    return render(request, 'home.html')

def student_dashboard_view(request):
    return render(request, 'student_dashboard.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dormitory.urls')),
    path('accounts/', include('accounts.urls')),
    path('payments/', include('payment.urls')),
    path('student/dashboard/', student_dashboard_view, name='student_dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)