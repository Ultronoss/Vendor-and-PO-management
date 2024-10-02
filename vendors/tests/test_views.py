from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from vendors.models import Vendor, PurchaseOrder
from django.utils import timezone

class VendorAPITest(APITestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="123 Test Street",
            address="456 Vendor Avenue",
            vendor_code="VEND123"
        )
        self.vendor_url = reverse('vendor-list')
        self.vendor_detail_url = reverse('vendor-detail', args=[self.vendor.id])
        self.performance_url = reverse('vendor-performance', args=[self.vendor.id])

    def test_create_vendor(self):
        data = {
            "name": "New Vendor",
            "contact_details": "789 New Street",
            "address": "101 New Avenue",
            "vendor_code": "VEND456"
        }
        response = self.client.post(self.vendor_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)
        self.assertEqual(Vendor.objects.get(id=response.data['id']).name, "New Vendor")

    def test_list_vendors(self):
        response = self.client.get(self.vendor_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_vendor(self):
        response = self.client.get(self.vendor_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Vendor")

    def test_update_vendor(self):
        data = {"name": "Updated Vendor"}
        response = self.client.patch(self.vendor_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, "Updated Vendor")

    def test_delete_vendor(self):
        response = self.client.delete(self.vendor_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

    def test_vendor_performance(self):
        # Create completed POs
        PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items={"item": "Item 1"},
            quantity=10,
            status="completed",
            quality_rating=4.0,
            issue_date=timezone.now(),
            delivered_date=timezone.now()
        )
        PurchaseOrder.objects.create(
            po_number="PO002",
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timezone.timedelta(days=1),
            items={"item": "Item 2"},
            quantity=5,
            status="completed",
            quality_rating=3.0,
            issue_date=timezone.now(),
            delivered_date=timezone.now() + timezone.timedelta(days=2)  # Late
        )
        response = self.client.get(self.performance_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['on_time_delivery_rate'], 50.0)
        self.assertEqual(response.data['quality_rating_avg'], 3.5)

class PurchaseOrderAPITest(APITestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="123 Test Street",
            address="456 Vendor Avenue",
            vendor_code="VEND123"
        )
        self.po = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timezone.timedelta(days=5),
            items={"item": "Test Item"},
            quantity=10,
            status="pending",
            issue_date=timezone.now()
        )
        self.po_url = reverse('purchaseorder-list')
        self.po_detail_url = reverse('purchaseorder-detail', args=[self.po.id])

    def test_create_purchase_order(self):
        data = {
            "po_number": "PO002",
            "vendor": self.vendor.id,
            "order_date": timezone.now(),
            "delivery_date": timezone.now() + timezone.timedelta(days=3),
            "items": {"item": "Another Item"},
            "quantity": 20,
            "status": "pending",
            "quality_rating": 4.5,
            "issue_date": timezone.now(),
            "delivered_date": None
        }
        response = self.client.post(self.po_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)
        self.assertEqual(PurchaseOrder.objects.get(po_number="PO002").quantity, 20)

    def test_list_purchase_orders(self):
        response = self.client.get(self.po_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_purchase_orders_by_vendor(self):
        response = self.client.get(self.po_url, {'vendor': self.vendor.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_purchase_order(self):
        response = self.client.get(self.po_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], "PO001")

    def test_update_purchase_order(self):
        data = {
            "status": "completed",
            "quality_rating": 4.0,
            "delivered_date": timezone.now().isoformat()  # Ensure proper datetime format
        }
        response = self.client.patch(self.po_detail_url, data, format='json')  # Use PATCH for partial updates
        if response.status_code != status.HTTP_200_OK:
            print("Response Errors:", response.data)  # Print validation errors
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.po.refresh_from_db()
        self.assertEqual(self.po.status, "completed")
        self.assertEqual(self.po.quality_rating, 4.0)
        self.assertIsNotNone(self.po.delivered_date)

    def test_delete_purchase_order(self):
        response = self.client.delete(self.po_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)