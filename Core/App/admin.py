from django.contrib import admin
from .models import Vendor, VendorPerformance, PurchaseOrder
# Register your models here.

admin.site.register(Vendor)
admin.site.register(VendorPerformance)
admin.site.register(PurchaseOrder)