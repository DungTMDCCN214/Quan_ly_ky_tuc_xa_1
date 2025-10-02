# payment/management/commands/generate_monthly_bills.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from payment.models import Payment
from dormitory.models import Contract

class Command(BaseCommand):
    help = 'Tạo hóa đơn thuê phòng hàng tháng'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        next_month = today + timedelta(days=30)
        
        # Lấy các hợp đồng đang active
        active_contracts = Contract.objects.filter(
            status='active',
            end_date__gte=today  # Chưa hết hạn
        )
        
        bills_created = 0
        
        for contract in active_contracts:
            # Kiểm tra xem đã có hóa đơn tháng này chưa
            existing_bill = Payment.objects.filter(
                contract=contract,
                due_date__year=today.year,
                due_date__month=today.month
            ).exists()
            
            if not existing_bill:
                # Tạo hóa đơn mới
                Payment.objects.create(
                    contract=contract,
                    amount=contract.room.room_type.price_per_month,
                    payment_method='bank_transfer',
                    status='pending',
                    due_date=next_month,
                    notes=f"Hóa đơn thuê phòng tháng {today.month}/{today.year}"
                )
                bills_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Đã tạo {bills_created} hóa đơn tháng {today.month}/{today.year}')
        )