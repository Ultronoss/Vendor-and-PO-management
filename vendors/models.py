from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=100, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    def update_performance_metrics(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        total_completed = completed_pos.count()

        if total_completed > 0:
            on_time = completed_pos.filter(delivered_date__lte=models.F('delivery_date')).count()
            self.on_time_delivery_rate = (on_time / total_completed) * 100

            average_quality = completed_pos.aggregate(avg_quality=Avg('quality_rating'))['avg_quality'] or 0.0
            self.quality_rating_avg = average_quality
        else:
            self.on_time_delivery_rate = 0.0
            self.quality_rating_avg = 0.0

        self.save()


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        null=True,
        blank=True
    )
    issue_date = models.DateTimeField(default=timezone.now)
    delivered_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.vendor.update_performance_metrics()