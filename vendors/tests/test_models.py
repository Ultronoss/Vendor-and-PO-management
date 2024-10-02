from django.test import TestCase
from django.utils import timezone
from vendors.models import Vendor, PurchaseOrder

class VendorModelTest(TestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="123 Test Street",
            address="456 Vendor Avenue",
            vendor_code="VEND123"
        )

    def test_vendor_creation(self):
        self.assertEqual(self.vendor.name, "Test Vendor")
        self.assertEqual(self.vendor.vendor_code, "VEND123")
        self.assertEqual(self.vendor.on_time_delivery_rate, 0.0)
        self.assertEqual(self.vendor.quality_rating_avg, 0.0)

    def test_update_performance_metrics_no_pos(self):
        self.vendor.update_performance_metrics()
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.on_time_delivery_rate, 0.0)
        self.assertEqual(self.vendor.quality_rating_avg, 0.0)

    def test_update_performance_metrics_with_pos(self):
        PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items={"item": "Test Item"},
            quantity=10,
            status="completed",
            quality_rating=4.5,
            issue_date=timezone.now(),
            delivered_date=timezone.now()
        )
        PurchaseOrder.objects.create(
            po_number="PO002",
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items={"item": "Test Item 2"},
            quantity=5,
            status="completed",
            quality_rating=3.5,
            issue_date=timezone.now(),
            delivered_date=timezone.now() + timezone.timedelta(days=1)  # Late delivery
        )
        self.vendor.update_performance_metrics()
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.on_time_delivery_rate, 50.0)  # 1 on-time out of 2
        self.assertEqual(self.vendor.quality_rating_avg, 4.0)  # Average of 4.5 and 3.5

class PurchaseOrderModelTest(TestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="123 Test Street",
            address="456 Vendor Avenue",
            vendor_code="VEND123"
        )

    def test_purchase_order_creation(self):
        po = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items={"item": "Test Item"},
            quantity=10,
            status="pending",
            issue_date=timezone.now()
        )
        self.assertEqual(po.po_number, "PO001")
        self.assertEqual(po.status, "pending")
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.on_time_delivery_rate, 0.0)
        self.assertEqual(self.vendor.quality_rating_avg, 0.0)

    def test_purchase_order_save_updates_vendor_metrics(self):
        po = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items={"item": "Test Item"},
            quantity=10,
            status="completed",
            quality_rating=5.0,
            issue_date=timezone.now(),
            delivered_date=timezone.now()
        )
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.on_time_delivery_rate, 100.0)
        self.assertEqual(self.vendor.quality_rating_avg, 5.0)