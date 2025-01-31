import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help = 'Backup PostgreSQL database and upload to Amazon S3'

    def handle(self, *args, **options):
        try:
            # Generate backup filename with timestamp
            backup_filename = f'backup_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.sql'
            backup_path = os.path.join(settings.BASE_DIR, backup_filename)

            # Set the PGPASSWORD environment variable for authentication
            os.environ['PGPASSWORD'] = os.getenv('DATABASE_PASSWORD')

            # Backup PostgreSQL database using pg_dump without specifying the user
            result = subprocess.run([
                'pg_dump', '-h', os.getenv('DATABASE_HOST', 'localhost'),
                '-d', os.getenv('DATABASE_NAME'),
                '-U', os.getenv('DATABASE_USER'),
                '-f', backup_path
            ], check=True)

            # Check if the backup was successful
            if result.returncode == 0:
                # Upload backup to S3 using default storage
                with open(backup_path, 'rb') as backup_file:
                    backup_key = f'backups/{backup_filename}'
                    default_storage.save(backup_key, backup_file)

                # Clean up local backup file
                os.remove(backup_path)

                self.stdout.write(self.style.SUCCESS('Backup and upload to S3 complete'))
            else:
                self.stdout.write(self.style.ERROR('Backup failed'))

        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Error during backup: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))
