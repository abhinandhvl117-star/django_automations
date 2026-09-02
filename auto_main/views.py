from django.shortcuts import render
from django.http import HttpResponse
from dataentry.tasks import celery_test_task
import time

def home(request):
    return render(request, 'home.html')

def celery_test(request):
    celery_test_task.delay()
    return HttpResponse("task done successfully")
    