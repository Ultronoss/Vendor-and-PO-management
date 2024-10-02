from django.test import TestCase
from rest_framework.exceptions import ValidationError
from vendors.models import Vendor, PurchaseOrder
from vendors.serializers import VendorSerializer, PurchaseOrderSerializer, PerformanceMetricsSerializer
from django.utils import timezone

class VendorSerializerTest(TestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="123 Test Street",
            address="456 Vendor Avenue",
            vendor_code="VEND123"
        )

    def test_vendor_serializer_fields(self):
        serializer = VendorSerializer(instance=self.vendor)
        data = serializer.data
        self.assertEqual(set(data.keys()), {
            'id', 'name', 'contact_details', 'address',
            'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg'
        })

class PurchaseOrderSerializerTest(TestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="123 Test Street",
            address="456 Vendor Avenue",
            vendor_code="VEND123"
        )
        self.valid_data = {
            "po_number": "PO001",
            "vendor": self.vendor.id,
            "order_date": timezone.now(),
            "delivery_date": timezone.now() + timezone.timedelta(days=5),
            "items": {"item": "Test Item"},
            "quantity": 10,
            "status": "pending",
            "quality_rating": 4.0,
            "issue_date": timezone.now(),
            "delivered_date": None
        }

    def test_purchase_order_serializer_valid(self):
        serializer = PurchaseOrderSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        po = serializer.save()
        self.assertEqual(po.po_number, "PO001")

    def test_purchase_order_serializer_invalid_quality_rating(self):
        data = self.valid_data.copy()
        data['quality_rating'] = 6.0  # Invalid rating
        serializer = PurchaseOrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quality_rating', serializer.errors)

class PerformanceMetricsSerializerTest(TestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="123 Test Street",
            address="456 Vendor Avenue",
            vendor_code="VEND123",
            on_time_delivery_rate=95.0,
            quality_rating_avg=4.5
        )

    def test_performance_metrics_serializer_fields(self):
        serializer = PerformanceMetricsSerializer(instance=self.vendor)
        data = serializer.data
        self.assertEqual(set(data.keys()), {
            'on_time_delivery_rate', 'quality_rating_avg'
        })
        self.assertEqual(data['on_time_delivery_rate'], 95.0)
        self.assertEqual(data['quality_rating_avg'], 4.5)