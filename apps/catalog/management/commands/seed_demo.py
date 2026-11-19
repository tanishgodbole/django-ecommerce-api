import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.catalog.models import Category, Product

class Command(BaseCommand):
    help = "Create deterministic demo catalog data (10 categories, 500 products)."
    def add_arguments(self, parser): parser.add_argument("--seed", type=int, default=2026)
    def handle(self, *args, **options):
        rng = random.Random(options["seed"])
        names = ["Electronics", "Home", "Books", "Clothing", "Outdoor", "Kitchen", "Beauty", "Toys", "Office", "Sports"]
        categories = [Category.objects.update_or_create(slug=slugify(n), defaults={"name": n, "description": f"Curated {n.lower()} essentials."})[0] for n in names]
        adjectives = ["Premium", "Everyday", "Compact", "Classic", "Modern", "Travel", "Pro", "Eco", "Wireless", "Lightweight"]
        nouns = ["Headphones", "Bottle", "Notebook", "Backpack", "Lamp", "Mug", "Jacket", "Speaker", "Keyboard", "Watch"]
        for n in range(500):
            label = f"{adjectives[n % len(adjectives)]} {nouns[(n // 10) % len(nouns)]} {n + 1:03d}"
            Product.objects.update_or_create(sku=f"DEMO-{n+1:04d}", defaults={"category":categories[n % len(categories)], "name":label, "slug":f"demo-product-{n+1:04d}", "description":f"{label}: dependable quality, practical design, and a one-year limited warranty.", "price":Decimal(rng.randrange(499, 49999)) / 100, "stock":rng.randint(0, 250), "is_active":True})
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(categories)} categories and 500 products (seed {options['seed']})."))
