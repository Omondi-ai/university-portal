from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser if none exist'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            print("Creating superuser...")
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin1234'
            )
            print("Superuser created.")
        else:
            print("Superuser already exists.")
