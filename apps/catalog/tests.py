from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from .models import Category, Product
class CatalogTests(APITestCase):
    def setUp(self):
        self.staff = get_user_model().objects.create_superuser("staff", "staff@example.com", "Passphrase-12345!")
        self.category = Category.objects.create(name="Books", slug="books")
        self.product = Product.objects.create(category=self.category, name="API Design", slug="api-design", sku="BOOK-1", price="25.00", stock=8)
    def test_product_list_paginates_and_filters(self):
        r = self.client.get("/api/v1/products/?search=API&price__gte=20")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["count"], 1)
    def test_catalog_write_requires_staff(self):
        self.assertEqual(self.client.post("/api/v1/products/", {}).status_code, 401)
        self.client.force_authenticate(self.staff)
        response = self.client.post("/api/v1/products/", {"category":self.category.pk,"name":"Lamp","slug":"lamp","sku":"LAMP-1","price":"9.99","stock":2}, format="json")
        self.assertEqual(response.status_code, 201)
    def test_schema_and_category_routes(self):
        self.assertEqual(self.client.get("/api/schema/").status_code, 200)
        self.assertEqual(self.client.get("/api/v1/categories/").status_code, 200)
