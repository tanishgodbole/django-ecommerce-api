from django.contrib.auth import get_user_model
from decimal import Decimal
from rest_framework.test import APITestCase
from apps.catalog.models import Category, Product
from .models import CartItem
class CartTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="buyer", email="b@example.com", password="Passphrase-12345!")
        self.product = Product.objects.create(category=Category.objects.create(name="Gear", slug="gear"), name="Bag", slug="bag", sku="BAG-1", price="30.00", stock=3)
        self.client.force_authenticate(self.user)
    def test_add_update_remove_and_cart_total(self):
        url = "/api/v1/cart/items/"
        r = self.client.post(url, {"product":self.product.pk,"quantity":2}, format="json")
        self.assertEqual(r.status_code, 201)
        item = CartItem.objects.get()
        self.assertEqual(self.client.get("/api/v1/cart/").data["total"], Decimal("60.00"))
        self.assertEqual(self.client.patch(f"{url}{item.pk}/", {"quantity":1}, format="json").status_code, 200)
        self.assertEqual(self.client.delete(f"{url}{item.pk}/").status_code, 204)
    def test_stock_limit_and_owner_isolation(self):
        self.assertEqual(self.client.post("/api/v1/cart/items/", {"product":self.product.pk,"quantity":4}, format="json").status_code, 400)
        other = get_user_model().objects.create_user(username="other", email="o@example.com", password="Passphrase-12345!")
        self.client.force_authenticate(other)
        self.assertEqual(self.client.get("/api/v1/cart/items/").data["count"], 0)
