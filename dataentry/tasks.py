from auto_main.celery import app
import time
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import send_email_notification
from dataentry.utils import generate_csv_file

@app.task
def celery_test_task():
    time.sleep(5)
    
    return 'Email send successfully'

@app.task
def import_data_task(absolute_path, model_name):
    try:
        call_command('importdata', absolute_path, model_name)
    except Exception as e:
        raise e  
    
    email_subject = 'Import Data Completed'
    message = 'Your data imported successfully'
    to_mail = settings.DEFAULT_TO_EMAIL
    send_email_notification(email_subject, message, to_mail)
     
    return 'Imported successfully'

@app.task
def export_data_task(model_name):
    try:
        call_command('exportdata', model_name)
    except Exception as e:
        raise e
        
    file_path = generate_csv_file(model_name)
        
    email_subject = 'export data from the database'
    message = 'Exporting data from the database has be successfull'
    to_email = settings.DEFAULT_TO_EMAIL
    
    send_email_notification(email_subject, message, to_email, attachment=file_path)