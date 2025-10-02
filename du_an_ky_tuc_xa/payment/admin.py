# payment/admin.py
from django.contrib import admin
from .models import Payment
from .services import send_payment_reminder

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'contract', 'amount', 'payment_method', 'status', 'due_date', 'paid_date']
    list_filter = ['status', 'payment_method', 'due_date']
    search_fields = ['contract__student__student_id', 'contract__student__full_name']
    actions = ['send_reminder_email']
    
    def send_reminder_email(self, request, queryset):
        """Action để gửi email nhắc nhở"""
        success_count = 0
        for payment in queryset:
            if send_payment_reminder(payment, request):
                success_count += 1
        
        if success_count > 0:
            self.message_user(request, f'✅ Đã gửi {success_count} email nhắc nhở thành công!')
        else:
            self.message_user(request, '❌ Gửi email thất bại!')
    
    send_reminder_email.short_description = '📧 Gửi email nhắc nhở'