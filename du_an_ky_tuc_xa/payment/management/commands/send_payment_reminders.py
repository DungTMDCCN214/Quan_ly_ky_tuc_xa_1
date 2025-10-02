# payment/management/commands/send_payment_reminders.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from payment.models import Payment
from payment.services import send_payment_reminder

class Command(BaseCommand):
    help = 'Gửi email nhắc nhở thanh toán cho hóa đơn sắp hết hạn'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        
        # Hóa đơn sắp hết hạn (3 ngày tới)
        upcoming_payments = Payment.objects.filter(
            status='pending',
            due_date__lte=today + timedelta(days=3),
            due_date__gte=today
        )
        
        # Hóa đơn quá hạn
        overdue_payments = Payment.objects.filter(
            status='pending',
            due_date__lt=today
        )
        
        emails_sent = 0
        
        # Gửi cho hóa đơn sắp hết hạn
        for payment in upcoming_payments:
            if send_payment_reminder(payment):
                self.stdout.write(f'✅ Đã gửi nhắc nhở HĐ #{payment.id} cho {payment.contract.student.student_id}')
                emails_sent += 1
        
        # Gửi cho hóa đơn quá hạn
        for payment in overdue_payments:
            if send_payment_reminder(payment):
                self.stdout.write(f'⚠️ Đã gửi cảnh báo quá hạn HĐ #{payment.id} cho {payment.contract.student.student_id}')
                emails_sent += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Đã gửi {emails_sent} email nhắc nhở')
        )