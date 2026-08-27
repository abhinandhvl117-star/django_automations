from django.core.management.base import BaseCommand

# proposed commmand = py manage.py helloworld

class Command(BaseCommand):
    help = "Prints Hello world"
    
    def handle(self, *args, **kwargs):
        self.stdout.write("Hello world")