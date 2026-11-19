from django.conf import settings
from django.db import models
from apps.catalog.models import Product
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    updated_at = models.DateTimeField(auto_now=True)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="cart_items")
    quantity = models.PositiveIntegerField()
    class Meta:
        ordering = ["id"]
        constraints = [models.UniqueConstraint(fields=["cart", "product"], name="unique_product_per_cart"), models.CheckConstraint(condition=models.Q(quantity__gt=0), name="cart_item_quantity_positive")]
