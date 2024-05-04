from django.db import models
from django.contrib.auth.models import User
from shortuuidfield import ShortUUIDField

from django.db.models.signals import post_save, post_delete 
from django.dispatch import receiver
from django.db.models import Avg, Count, F, Sum 

# Create your models here.
class Vendor(models.Model):
    name= models.CharField(max_length=50)
    contact_details= models.TextField(max_length=200,null=True)
    address= models.TextField(default="")
    vendor_code= ShortUUIDField(primary_key=True)
    on_time_delivery_rate= models.FloatField(default=0) 
    quality_rating_avg= models.FloatField(default=0)
    average_response_time= models.FloatField(default=0)
    fulfillment_rate= models.FloatField(default=0)

    def __str__(self):
        return f'{self.vendor_code} - {self.name}'

class PurchaseOrder(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number= ShortUUIDField(primary_key=True)
    vendor= models.ForeignKey(Vendor, on_delete=models.CASCADE)
    items= models.JSONField()
    quantity= models.IntegerField(default=0)
    status= models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    quality_rating= models.FloatField(null=True,default=0)
    order_date= models.DateTimeField(auto_now_add=True)
    issue_date= models.DateTimeField(auto_now_add=True,null=True)
    acknowledgement_date= models.DateTimeField(null=True)
    expected_delivery_date= models.DateTimeField(null=True)
    delivery_date= models.DateTimeField(null=True)

    def __str__(self):
        return self.po_number
    
class VendorPerformance(models.Model):
    vendor= models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date= models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate= models.FloatField(default=0) 
    quality_rating_avg= models.FloatField(default=0)
    average_response_time= models.FloatField(default=0)
    fulfillment_rate= models.FloatField(default=0)
    
# Signal on PurchaseOrder model to calculate performance matrix
@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def calc_performance_matrix(sender, instance, **kwargs):
    vendor = instance.vendor
    print("Signals is working on Purchase Model")

    # Calculate on-time delivery rate
    po_on_or_before = PurchaseOrder.objects.filter(vendor = instance.vendor,status='completed',delivery_date__lte=instance.expected_delivery_date).count()
    total_orders = PurchaseOrder.objects.filter(vendor = instance.vendor , delivery_date__isnull=False,status='completed').count()
    if total_orders >0:
        vendor.on_time_delivery_rate = (po_on_or_before*100)/total_orders
    else:
        vendor.on_time_delivery_rate = 0

    # Calculate quality rating average
    ratings_provided = PurchaseOrder.objects.filter(vendor = instance.vendor,status= "completed",quality_rating__gt=0).aggregate( ratings=Sum('quality_rating'))
    total_ratings = PurchaseOrder.objects.filter(vendor = instance.vendor,status= "completed").count()
    if ratings_provided['ratings'] is not None:
        vendor.quality_rating_avg = (ratings_provided["ratings"]/total_ratings) if total_ratings >0 else 0
    else:
        vendor.quality_rating_avg = 0

    # Calculate average response time
    sum_time = PurchaseOrder.objects.filter(vendor = instance.vendor,acknowledgement_date__isnull = False).aggregate(sum_time =Avg(F('acknowledgement_date') - F('issue_date')))
    if sum_time['sum_time'] is not None:
        vendor.average_response_time=sum_time['sum_time'].total_seconds()
    else:
        vendor.average_response_time=0


    # Calculate fulfillment rate
    po_completed = PurchaseOrder.objects.filter(vendor = instance.vendor,status="completed").count()
    po_total = PurchaseOrder.objects.filter(vendor = instance.vendor).count()
    vendor.fulfillment_rate = (po_completed*100)/po_total if po_total> 0 else 0
    
    vendor.save()

# Signal to make entry into VendorPerformance Model whenever any instance of Vendor model is deleted.
@receiver(post_delete, sender=Vendor)
def store_historical_performance(sender, instance, **kwargs):
    VendorPerformance.objects.create(vendor=instance, on_time_delivery_rate= instance.on_time_delivery_rate, quality_rating_avg= instance.quality_rating_avg, average_response_time= instance.average_response_time, fulfillment_rate = instance.fulfillment_rate)

    instance.save()

