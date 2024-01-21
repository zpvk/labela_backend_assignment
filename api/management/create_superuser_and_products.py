from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from models import Product

class Command(BaseCommand):
    help = 'Create superuser and add products to the database'

    def handle(self, *args, **kwargs):
        # Apply migrations
        self.call_command("migrate")

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            self.call_command(
                "createsuperuser",
                "--username", "admin",
                "--email", "admin@example.com",
                "--password", "admin",  # Set your desired password here
                "--noinput"
            )

        # Create products
        if not Product.objects.exists():
            Product.objects.create(name='Product 1', description='Description 1', price=19.99)
            Product.objects.create(name='Product 2', description='Description 2', price=29.99)

    def call_command(self, *args, **options):
        from django.core.management import call_command
        call_command(*args, **options)
