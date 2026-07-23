import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create or update a default admin user (superuser).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            default=os.getenv('DEFAULT_ADMIN_USERNAME', 'admin'),
            help='Admin username. Default from DEFAULT_ADMIN_USERNAME or "admin".',
        )
        parser.add_argument(
            '--password',
            default=os.getenv('DEFAULT_ADMIN_PASSWORD', 'admin12345'),
            help='Admin password. Default from DEFAULT_ADMIN_PASSWORD or "admin12345".',
        )
        parser.add_argument(
            '--email',
            default=os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@sakukoperasi.local'),
            help='Admin email. Default from DEFAULT_ADMIN_EMAIL or "admin@sakukoperasi.local".',
        )
        parser.add_argument(
            '--if-not-exists',
            action='store_true',
            help='Only create user when missing. If user exists, skip update.',
        )

    def handle(self, *args, **options):
        username = options['username'].strip()
        password = options['password']
        email = options['email'].strip()

        if not username:
            raise CommandError('username cannot be empty.')

        if not password:
            raise CommandError('password cannot be empty.')

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
            },
        )

        if options['if_not_exists'] and not created:
            self.stdout.write(self.style.WARNING(f'Admin user already exists, skipped: {username}'))
            return

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Admin user created: {username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Admin user updated: {username}'))
