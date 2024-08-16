from django.core.management.base import BaseCommand
from faker import Faker
from products.models import Products

class Command(BaseCommand):
    help = 'Seeds the database with fake data using Faker'

    def handle(self, *args, **kwargs):
        
        fake = Faker()

        for _ in range(20):
            Products.objects.create(
                product_name=fake.word(),
                product_description=fake.text(),
                product_price=fake.random_number(digits=5) / 100.0,  
                product_stock=fake.random_int(min=0, max=100) 
            )

        self.stdout.write(self.style.SUCCESS('Database seeded with fake data successfully'))