from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .permissions import StaffWriteOrReadOnly
from .serializers import CategorySerializer, ProductSerializer
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, StaffWriteOrReadOnly]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related("category")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, StaffWriteOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {"category": ["exact"], "price": ["lte", "gte"], "is_active": ["exact"]}
    search_fields = ["name", "description", "sku"]
    ordering_fields = ["price", "name", "created_at"]
    def perform_create(self, serializer): serializer.save(created_by=self.request.user)
