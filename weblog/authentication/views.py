from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import logout
from django.utils.encoding import *
# from decouple import config
import ssl, smtplib
from time import sleep

# Create your views here.

def register(request):
    
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST["username"]
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                print('Username Taken')
                messages.error(request, 'Oops😥. Username Already Taken!')
                return render(request, 'authentication/register.html')#, {'error': 'Username is already taken!'})
 
            elif User.objects.filter(email=email).exists():
                print('email Taken')
                messages.error(request, 'Too bad😶. Email Already Exist!')
                return render(request, 'authentication/register.html')#, {'error':'Email is already taken!'})
                              
            else:
                user = User.objects.create_user(username=username, password=confirm_password, email=email, first_name=first_name, last_name=last_name)
                #user.is_active = False
                user.save();
                print('User created')
                return redirect('home')
        
        else:
            print('Password does not match')
            messages.error(request, 'Password Does Not Match!')
            return render(request, 'authentication/register.html')
        
    return render(request, 'authentication/register.html')



def login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            print('logged in')
            return redirect('home')
        
        else:
            print('not logged in')
            messages.error(request, 'Incorrect Credentials! ❌')
            return render(request, 'authentication/login.html')
    
    return render(request, 'authentication/login.html')

def logout(request):
    auth.logout(request)
    return redirect("/")
