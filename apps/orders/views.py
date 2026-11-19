from django.db import transaction
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from apps.cart.models import Cart
from apps.catalog.models import Product
from .models import Order, OrderItem
from .serializers import OrderSerializer
class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.none()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False): return Order.objects.none()
        return Order.objects.filter(user=self.request.user).prefetch_related("items")
    @action(detail=False, methods=["post"])
    def checkout(self, request):
        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=request.user)
            items = list(cart.items.select_related("product").select_for_update())
            if not items: raise ValidationError({"cart": "Cannot checkout an empty cart."})
            products = {p.pk: p for p in Product.objects.select_for_update().filter(pk__in=[i.product_id for i in items])}
            for item in items:
                product = products[item.product_id]
                if not product.is_active or product.stock < item.quantity: raise ValidationError({"stock": f"Insufficient stock for {product.name}."})
            order = Order.objects.create(user=request.user)
            total = 0
            for item in items:
                product = products[item.product_id]
                OrderItem.objects.create(order=order, product=product, product_name=product.name, unit_price=product.price, quantity=item.quantity)
                product.stock -= item.quantity
                product.save(update_fields=["stock"])
                total += product.price * item.quantity
            order.total = total
            order.save(update_fields=["total"])
            cart.items.all().delete()
        return Response(self.get_serializer(order).data, status=status.HTTP_201_CREATED)
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        with transaction.atomic():
            order = Order.objects.select_for_update().filter(user=request.user, pk=pk).first()
            if order is None: return Response({"detail": "Not found."}, status=404)
            if order.status != Order.Status.PENDING: raise ValidationError({"status": "Only pending orders can be cancelled."})
            for item in order.items.all():
                product = Product.objects.select_for_update().get(pk=item.product_id)
                product.stock += item.quantity
                product.save(update_fields=["stock"])
            order.status = Order.Status.CANCELLED
            order.cancelled_at = timezone.now()
            order.save(update_fields=["status", "cancelled_at"])
        return Response(self.get_serializer(order).data)
