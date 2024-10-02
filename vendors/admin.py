from django.contrib import admin
from .models import Vendor, PurchaseOrder

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg')
    search_fields = ('name', 'vendor_code')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'po_number', 'vendor', 'status', 'order_date', 'delivery_date')
    search_fields = ('po_number', 'vendor__name')
    list_filter = ('status',)