# payment/management/commands/check_overdue_payments.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from payment.models import Payment

class Command(BaseCommand):
    help = 'Kiểm tra và đánh dấu hóa đơn quá hạn'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        overdue_payments = Payment.objects.filter(
            status='pending',
            due_date__lt=today
        )
        
        count = overdue_payments.count()
        
        self.stdout.write(
            self.style.WARNING(f'⚠️ Có {count} hóa đơn quá hạn')
        )
        
        for payment in overdue_payments:
            self.stdout.write(
                f'   - HĐ #{payment.id}: {payment.contract.student.student_id} - {payment.amount} VNĐ'
            )