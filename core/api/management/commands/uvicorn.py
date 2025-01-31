from django.core.management.base import BaseCommand
import uvicorn

class Command(BaseCommand):
    help = "Runs the Uvicorn server."
    # uvicorn core.asgi:application --host 127.0.0.1 --port 8000

    def add_arguments(self, parser):
        # Optional arguments, with default values
        parser.add_argument(
            '--host', 
            type=str, 
            default='127.0.0.1', 
            help='Specify the host for Uvicorn to bind to (default: 127.0.0.1)'
        )
        parser.add_argument(
            '--port', 
            type=int, 
            default=8000, 
            help='Specify the port for Uvicorn to bind to (default: 8000)'
        )
        parser.add_argument(
            '--reload', 
            action='store_true', 
            help='Enable auto-reload on code changes'
        )

    def handle(self, *args, **options):
        host = options['host'] or '127.0.0.1'
        port = options['port'] or 8000
        reload = options['reload']
        self.stdout.write(f"Starting Uvicorn server at {host}:{port} with reload={'enabled' if reload else 'disabled'}")
        
        # Run Uvicorn with specified (or default) host and port
        uvicorn.run("core.asgi:application", host=host, port=port, reload=reload)
