from django.shortcuts import render, redirect
from django.http import HttpResponse
from dataentry.tasks import celery_test_task
from .forms import Registration
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, 'home.html')

def celery_test(request):
    celery_test_task.delay()
    return HttpResponse("task done successfully")
    
def register(request):
    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registered Successfullty')
            return redirect('register')
        else:
            context = {
            'form': form
            }
            return render(request, 'register.html', context)
            
    else:
        form = Registration()
        context = {
            'form': form
        }
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            return redirect('home')


    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')