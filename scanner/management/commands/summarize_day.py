from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from scanner.models import Transaction, DailySummary

class Command(BaseCommand):
    help = 'Summarizes the scanned items for the previous day and saves it to DailySummary'

    def handle(self, *args, **options):
        yesterday = timezone.now().date() - timedelta(days=1)

        total_mouses = 0
        total_keyboards = 0
        total_monitors = 0

        transactions = Transaction.objects.filter(timestamp__date=yesterday)

        for transaction in transactions:
            if 'mouse' in transaction.item_name.lower():
                total_mouses += transaction.quantity
            if 'keyboard' in transaction.item_name.lower():
                total_keyboards += transaction.quantity
            if 'monitor' in transaction.item_name.lower():
                total_monitors += transaction.quantity

        summary, created = DailySummary.objects.get_or_create(
            date=yesterday,
            defaults={
                'total_mouses': total_mouses,
                'total_keyboards': total_keyboards,
                'total_monitors': total_monitors,
            }
        )

        if not created:
            summary.total_mouses = total_mouses
            summary.total_keyboards = total_keyboards
            summary.total_monitors = total_monitors
            summary.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully summarized transactions for {yesterday}'))
