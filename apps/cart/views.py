from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import ValidationError
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self): return Cart.objects.get_or_create(user=self.request.user)[0]
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.none()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False): return CartItem.objects.none()
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart).select_related("product")
    def perform_create(self, serializer):
        product = serializer.validated_data["product"]
        existing = self.get_queryset().filter(product=product).first()
        if serializer.validated_data["quantity"] + (existing.quantity if existing else 0) > product.stock: raise ValidationError({"quantity": "Requested quantity exceeds available stock."})
        serializer.save()
    def perform_update(self, serializer):
        product = serializer.validated_data.get("product", serializer.instance.product)
        if serializer.validated_data.get("quantity", serializer.instance.quantity) > product.stock: raise ValidationError({"quantity": "Requested quantity exceeds available stock."})
        serializer.save()
