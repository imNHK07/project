from django.http import JsonResponse
from .models import Master, Transaction, DailySummary
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.utils import timezone
from django.db.models import F
import json

def index(request):
    return render(request, 'scanner/index.html')


@csrf_exempt
def scan_barcode(request, barcode):
    if request.method == 'POST':
        try:
            master = Master.objects.get(barcode=barcode)
            if Transaction.objects.filter(barcode=master).exists():
                return JsonResponse({'error': 'Error: This barcode has already been scanned.'}, status=400)
            transaction = Transaction.objects.create(
                barcode=master,
                item_name=master.item_name,
                quantity=master.quantity
            )

            # Update DailySummary
            today = timezone.now().date()
            item_name_lower = master.item_name.lower()

            DailySummary.objects.get_or_create(date=today) # Ensure the summary for today exists

            update_kwargs = {}
            if 'mouse' in item_name_lower:
                update_kwargs['total_mouses'] = F('total_mouses') + transaction.quantity
            elif 'keyboard' in item_name_lower:
                update_kwargs['total_keyboards'] = F('total_keyboards') + transaction.quantity
            elif 'monitor' in item_name_lower:
                update_kwargs['total_monitors'] = F('total_monitors') + transaction.quantity

            if update_kwargs:
                DailySummary.objects.filter(date=today).update(**update_kwargs)

            return JsonResponse({'success': f'Transaction created for {master.item_name}'})
        except Master.DoesNotExist:
            return JsonResponse({'error': 'Barcode not found'}, status=404)

@csrf_exempt
def auto_scan_barcode(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            barcode = data.get('barcode')

            if not barcode:
                return JsonResponse({'error': 'Barcode not provided'}, status=400)

            master = Master.objects.get(barcode=barcode)
            if Transaction.objects.filter(barcode=master).exists():
                return JsonResponse({'error': 'Error: This barcode has already been scanned.'}, status=400)
            transaction = Transaction.objects.create(
                barcode=master,
                item_name=master.item_name,
                quantity=master.quantity
            )

            # Update DailySummary
            today = timezone.now().date()
            item_name_lower = master.item_name.lower()

            summary, created = DailySummary.objects.get_or_create(date=today)

            update_kwargs = {}
            if 'mouse' in item_name_lower:
                update_kwargs['total_mouses'] = F('total_mouses') + transaction.quantity
            elif 'keyboard' in item_name_lower:
                update_kwargs['total_keyboards'] = F('total_keyboards') + transaction.quantity
            elif 'monitor' in item_name_lower:
                update_kwargs['total_monitors'] = F('total_monitors') + transaction.quantity

            if update_kwargs:
                DailySummary.objects.filter(date=today).update(**update_kwargs)

            return JsonResponse({'success': f'Transaction created for {master.item_name}'})
        except Master.DoesNotExist:
            return JsonResponse({'error': 'Barcode not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)