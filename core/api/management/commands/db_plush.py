import os
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Drop all tables'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Dropping all tables...'))
        self.drop_all_tables()
        self.stdout.write(self.style.SUCCESS('All tables dropped.'))

    def drop_all_tables(self):
        with connection.cursor() as cursor:
            cursor.execute('DROP SCHEMA public CASCADE;')
            cursor.execute('CREATE SCHEMA public;')
            cursor.execute('GRANT ALL ON SCHEMA public TO postgres;')
            cursor.execute('GRANT ALL ON SCHEMA public TO public;')