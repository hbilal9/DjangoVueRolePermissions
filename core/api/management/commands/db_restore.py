import os
from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help = 'Restore PostgreSQL database from a backup stored in Amazon S3'
    '''
    python manage.py db_restore backups/backup_2023-10-01_12-00-00.sql
    '''

    def add_arguments(self, parser):
        parser.add_argument('backup_key', type=str, help='The S3 key of the backup file to restore')

    def handle(self, *args, **options):
        backup_key = options['backup_key']
        backup_filename = os.path.basename(backup_key)
        backup_path = os.path.join(settings.BASE_DIR, backup_filename)

        # Download backup from S3 using default storage
        with default_storage.open(backup_key, 'rb') as backup_file:
            with open(backup_path, 'wb') as local_backup_file:
                local_backup_file.write(backup_file.read())

        # Set the PGPASSWORD environment variable with the password
        os.environ['PGPASSWORD'] = os.getenv('DATABASE_PASSWORD')

        # Get the database host, port, user, and name from environment variables
        db_host = os.getenv('DATABASE_HOST')
        db_port = os.getenv('DATABASE_PORT')
        db_user = os.getenv('DATABASE_USER')
        db_name = os.getenv('DATABASE_NAME')

        # Restore PostgreSQL database
        subprocess.run([
            'psql',
            '-h', db_host,
            '-p', db_port,
            '-U', db_user,
            '-d', db_name,
            '-f', backup_path
        ])

        # Clean up local backup
        os.remove(backup_path)

        self.stdout.write(self.style.SUCCESS('Database restore complete'))