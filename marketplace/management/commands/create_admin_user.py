from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create the FarmConnect admin user'

    def handle(self, *args, **options):
        User = get_user_model()

        admin_email = 'admin@farmconnect.sn'
        admin_username = 'farmconnect_admin'
        admin_password = 'FarmConnect@2024'

        # Check if admin already exists
        if User.objects.filter(username=admin_username).exists():
            self.stdout.write(self.style.WARNING(f'Admin user "{admin_username}" already exists.'))
            return

        # Create superuser
        admin = User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password,
            first_name='Admin',
            last_name='FarmConnect',
            role='admin'
        )

        self.stdout.write(self.style.SUCCESS('FarmConnect Admin Created Successfully!'))
        self.stdout.write(f'Email:     {admin_email}')
        self.stdout.write(f'Username:  {admin_username}')
        self.stdout.write(f'Password:  {admin_password}')
        self.stdout.write('Admin Dashboard: http://127.0.0.1:8000/admin/')
        self.stdout.write(self.style.WARNING('IMPORTANT: Change the password after first login!'))
