from django.core.management.base import BaseCommand


# proposed command = py manage.py greetin name
class Command(BaseCommand):
    help = "greets the user"
    
    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help="gets user name")
    
    def handle(self, *args, **kwargs):
        name = kwargs['name']
        greeting = f'Hello {name}, Good Morning'
        # normal
        # self.stdout.write(greeting)
        self.stdout.write(self.style.HTTP_REDIRECT(greeting))