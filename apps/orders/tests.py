from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from apps.catalog.models import Category, Product
class OrderTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="buyer", email="b@example.com", password="Passphrase-12345!")
        self.product = Product.objects.create(category=Category.objects.create(name="Gear", slug="gear"), name="Bag", slug="bag", sku="BAG-1", price="30.00", stock=3)
        self.client.force_authenticate(self.user)
    def add_item(self, quantity=2): return self.client.post("/api/v1/cart/items/", {"product":self.product.pk,"quantity":quantity}, format="json")
    def test_checkout_captures_price_decrements_stock_and_clears_cart(self):
        self.add_item()
        r = self.client.post("/api/v1/orders/checkout/")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data["total"], "60.00")
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1)
        self.assertEqual(self.client.get("/api/v1/cart/").data["items"], [])
    def test_empty_checkout_rejected(self):
        self.assertEqual(self.client.post("/api/v1/orders/checkout/").status_code, 400)
    def test_cancel_restores_stock_and_repeat_cancel_rejected(self):
        self.add_item()
        order = self.client.post("/api/v1/orders/checkout/").data
        self.assertEqual(self.client.post(f"/api/v1/orders/{order['id']}/cancel/").status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)
        self.assertEqual(self.client.post(f"/api/v1/orders/{order['id']}/cancel/").status_code, 400)
