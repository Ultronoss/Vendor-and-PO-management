from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from vendors.views import VendorViewSet, PurchaseOrderViewSet
from vendors.models import Vendor, PurchaseOrder
from django.utils import timezone

class URLRoutingTest(APITestCase):

    def test_vendor_list_url(self):
        url = reverse('vendor-list')
        self.assertEqual(resolve(url).func.cls, VendorViewSet)

    def test_vendor_detail_url(self):
        vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="123 Test Street",
            address="456 Vendor Avenue",
            vendor_code="VEND123"
        )
        url = reverse('vendor-detail', args=[vendor.id])
        self.assertEqual(resolve(url).func.cls, VendorViewSet)

    def test_vendor_performance_url(self):
        vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="123 Test Street",
            address="456 Vendor Avenue",
            vendor_code="VEND123"
        )
        url = reverse('vendor-performance', args=[vendor.id])
        self.assertEqual(resolve(url).func.cls, VendorViewSet)

    def test_purchase_order_list_url(self):
        url = reverse('purchaseorder-list')
        self.assertEqual(resolve(url).func.cls, PurchaseOrderViewSet)

    def test_purchase_order_detail_url(self):
        vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="123 Test Street",
            address="456 Vendor Avenue",
            vendor_code="VEND123"
        )
        po = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timezone.timedelta(days=5),
            items={"item": "Test Item"},
            quantity=10,
            status="pending",
            issue_date=timezone.now()
        )
        url = reverse('purchaseorder-detail', args=[po.id])
        self.assertEqual(resolve(url).func.cls, PurchaseOrderViewSet)