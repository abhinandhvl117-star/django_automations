from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv
from django.db import DataError

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
        
        # getting model field name
        model_field = [field.name for field in model._meta.fields if field.name != 'id']
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            # getting csv header
            csv_header = reader.fieldnames
            
            # comparing model name and csv header
            if model_field != csv_header:
                raise DataError(f'The csv header doesnt match with the {model_name} files')
            
            for row in reader:
                model.objects.create(**row)
                
        self.stdout.write(self.style.SUCCESS("Data imported from csv file successfully"))