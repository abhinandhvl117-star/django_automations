from auto_main.celery import app
import time
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import send_email_notification

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