from rest_framework import serializers
from .models import Vendor, PurchaseOrder

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ['on_time_delivery_rate', 'quality_rating_avg']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = []

    def validate_quality_rating(self, value):
        if value is not None and (value < 1.0 or value > 5.0):
            raise serializers.ValidationError("Quality rating must be between 1 and 5.")
        return value

class PerformanceMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['on_time_delivery_rate', 'quality_rating_avg']