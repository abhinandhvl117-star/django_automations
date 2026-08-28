from django.core.management.base import BaseCommand
from django.apps import apps
import csv
import datetime

# proposed command - py manage.py exportdata model_name

class Command(BaseCommand):
    help = 'export data from the model to the csv file'
    
    # accept argument
    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='model_name')
    
    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name']
        
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)        
                break
            except LookupError:
                continue
            
        if not model:
            self.stdout.write(self.style.ERROR(f"model {model_name} not found"))
            return
        
        data = model.objects.all()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        file_name = f'exported_{model_name}_data_{timestamp}.csv'
        
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            
            writer.writerow([field.name for field in model._meta.fields])
            
            for dt in data:
                writer.writerow([getattr(dt,field.name) for field in model._meta.fields])
                
        self.stdout.write(self.style.SUCCESS(f"Successfully exported the file, filename-{file_name}"))
        