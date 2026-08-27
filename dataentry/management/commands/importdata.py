from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv

# proposed command = py manage.py importdata file_path model_name

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to the csv file")
        parser.add_argument('model_name', type=str, help="Name of the model")
        
    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()
        
        # search for the model in the apps
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue
        
        if not model:
            raise CommandError(f"Model {model_name} does not found in any apps")
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)
                
        self.stdout.write(self.style.SUCCESS("Data imported from csv file successfully"))