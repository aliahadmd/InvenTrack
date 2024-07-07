import random
from django.core.management.base import BaseCommand
from django.db import transaction
from inventory.models import Category, Supplier, Product, StockMovement
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Generates fake data for e-commerce products'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of products to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        self.stdout.write('Creating fake e-commerce product data...')

        # Create categories
        categories = [
            'Electronics', 'Clothing', 'Home & Garden', 'Sports & Outdoors',
            'Books', 'Toys & Games', 'Beauty & Personal Care', 'Automotive',
            'Jewelry', 'Food & Grocery'
        ]
        for category_name in categories:
            Category.objects.get_or_create(name=category_name, description=fake.text(max_nb_chars=200))

        # Create suppliers
        suppliers = []
        for _ in range(20):
            supplier = Supplier.objects.create(
                name=fake.company(),
                contact_person=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                address=fake.address()
            )
            suppliers.append(supplier)

        # Create products
        products = []
        with transaction.atomic():
            for _ in range(total):
                category = Category.objects.order_by('?').first()
                supplier = random.choice(suppliers)
                
                product = Product.objects.create(
                    name=fake.catch_phrase(),
                    description=fake.paragraph(nb_sentences=3),
                    sku=fake.unique.ean(length=13),
                    category=category,
                    supplier=supplier,
                    price=round(random.uniform(1.0, 999.99), 2),
                    stock_quantity=random.randint(0, 1000),
                    reorder_level=random.randint(10, 100)
                )
                products.append(product)
                self.stdout.write(f'Created product: {product.name}')

        # Create stock movements
        with transaction.atomic():
            for product in products:
                for _ in range(random.randint(5, 20)):  # Random number of stock movements per product
                    StockMovement.objects.create(
                        product=product,
                        quantity=random.randint(1, 100),
                        movement_type=random.choice(['IN', 'OUT']),
                        notes=fake.text()
                    )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} fake products and their stock movements'))
