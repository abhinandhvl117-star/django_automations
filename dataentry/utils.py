from django.apps import apps
from django.core.management import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import os

def get_all_models():
    default_model = ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'Upload']
    custom_models = []
    
    for model in apps.get_models():
        if model.__name__ not in default_model:
            custom_models.append(model.__name__)
    
    return custom_models

def check_csv_error(file_path, model_name):
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

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            # getting csv header
            csv_header = reader.fieldnames
            
            # comparing model name and csv header
            if model_field != csv_header:
                raise DataError(f'The csv header doesnt match with the {model_name} files')
    except Exception as e:
        raise e

    return model

def send_email_notification(mail_subject, message, to_email, attachment=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        if attachment is not None:
            mail.attach_file(attachment)
        mail.send()
    except Exception as e:
        raise e
    
def generate_csv_file(model_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    export_dir = 'exported_files'
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    
    return file_path