from django.db import models
import pytz
import random
from barcode import get_barcode_class

class Master(models.Model):
    barcode = models.CharField(max_length=100, unique=True, blank=True)
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:
            EAN13 = get_barcode_class('ean13')
            while True:
                random_12_digits = ''.join(random.choices('0123456789', k=12))
                ean = EAN13(random_12_digits)
                barcode = ean.get_fullcode()
                if not Master.objects.filter(barcode=barcode).exists():
                    self.barcode = barcode
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.item_name

class Transaction(models.Model):
    barcode = models.ForeignKey(Master, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        dhaka_tz = pytz.timezone("Asia/Dhaka")
        local_time = self.timestamp.astimezone(dhaka_tz)
        return f"Transaction for {self.item_name}, Quantity: {self.quantity} at {local_time.strftime('%Y-%m-%d %H:%M:%S')}"

class DailySummary(models.Model):
    date = models.DateField(unique=True)
    total_mouses = models.IntegerField(default=0)
    total_keyboards = models.IntegerField(default=0)
    total_monitors = models.IntegerField(default=0)

    def __str__(self):
        return f"Summary for {self.date}"