# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import bcrypt

# Create your views here.
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

import bcrypt

def index(request):
    return render(request, 'user_dashboard/index.html')

def signin(request):
    return render(request, 'user_dashboard/signin.html')

def process_signin(request):
    errors = User.objects.validate_login(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/signin')
    else:
        user_check = User.objects.filter(email = request.POST['email'])
        if len(user_check) > 0:
            user_check = user_check[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user_check.password.encode()):
                request.session['id'] = user_check.id
                if user_check.admin == True:
                    return redirect('/dashboard/admin')
                else:
                    return redirect('/dashboard/')

def register(request):
    return render(request, 'user_dashboard/register.html')

def process_registration(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
            return redirect('/register')      
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], password = hashed_pw)
        request.session['id'] = new_user.id
        return redirect('/dashboard')

def dashboard(request):
    context = {
        "current_user": User.objects.filter(id=request.session['id']),
        "all_users": User.objects.all()
    }
    return render(request, 'user_dashboard/dashboard.html', context)

def admin(request):
    context = {
        "admin_user": User.objects.filter(admin=True),
        "all_users": User.objects.all()
    }
    return render(request, 'user_dashboard/admin.html', context)

def show(request, id):
    context = {
        "current_user": User.objects.filter(id=request.session['id']),
        "show_user": User.objects.filter(id = id),
        "messages": Message.objects.filter(receiver = id)
    }
    return render(request, 'user_dashboard/show.html', context)

def process_message(request):
    sender_id = User.objects.all().get(id = request.session['id'])
    receiver_id = User.objects.all().get(id = request.POST['receiver_id'])
    receiver = request.POST['receiver_id']
    message = Message.objects.create(content=request.POST['message_content'], sender=sender_id, receiver=receiver_id)
    return redirect('/users/show/' + receiver)

def logout(request):
    del request.session['id']
    return redirect('/')
