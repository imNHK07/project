from django.contrib import admin
from django.http import HttpResponse
from .models import Master, Transaction, DailySummary
from .pdf_utils import generate_barcode_pdf, get_barcode_svg
from django.utils.safestring import mark_safe

class MasterAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'item_name', 'quantity')
    search_fields = ('barcode', 'item_name')
    list_filter = ('item_name',)
    actions = ['download_pdf']

    def download_pdf(self, request, queryset):
        buffer = generate_barcode_pdf(queryset)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="barcodes.pdf"'
        return response
    download_pdf.short_description = "Download PDF of selected barcodes"

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return (
                (None, {
                    'fields': ('item_name', 'quantity')
                }),
            )
        return super().get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('barcode',)
        return ()

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('get_barcode', 'get_item_name', 'quantity', 'timestamp')
    ordering = ('-timestamp',)

    def get_barcode(self, obj):
        return obj.barcode.barcode
    get_barcode.short_description = 'Barcode'
    get_barcode.admin_order_field = 'barcode__barcode'

    def get_item_name(self, obj):
        return obj.barcode.item_name
    get_item_name.short_description = 'Item Name'
    get_item_name.admin_order_field = 'barcode__item_name'

class DailySummaryAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_mouses', 'total_keyboards', 'total_monitors')
    ordering = ('-date',)

admin.site.register(Master, MasterAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(DailySummary, DailySummaryAdmin)