from rest_framework import serializers
from decimal import Decimal
from .models import Cart, CartItem
class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    unit_price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = CartItem
        fields = ("id", "product", "product_name", "quantity", "unit_price")
        read_only_fields = ("id",)
    def validate(self, attrs):
        product = attrs.get("product", getattr(self.instance, "product", None))
        quantity = attrs.get("quantity", getattr(self.instance, "quantity", 1))
        if product and (not product.is_active or quantity > product.stock): raise serializers.ValidationError("Product is unavailable or requested quantity exceeds stock.")
        return attrs
    def create(self, data):
        cart, _ = Cart.objects.get_or_create(user=self.context["request"].user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=data["product"], defaults={"quantity": data["quantity"]})
        if not created:
            item.quantity += data["quantity"]
            item.save(update_fields=["quantity"])
        return item
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ("id", "items", "total", "updated_at")
    def get_total(self, cart) -> Decimal: return sum((i.product.price * i.quantity for i in cart.items.select_related("product")), start=Decimal("0.00"))
