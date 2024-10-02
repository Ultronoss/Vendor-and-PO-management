from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer, PerformanceMetricsSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=['get'], url_path='performance')
    def performance(self, request, pk=None):
        vendor = self.get_object()
        serializer = PerformanceMetricsSerializer(vendor)
        return Response(serializer.data)

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get('vendor', None)
        if vendor_id is not None:
            queryset = queryset.filter(vendor__id=vendor_id)
        return queryset