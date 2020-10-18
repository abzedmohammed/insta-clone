from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http  import HttpResponse
import datetime as dt
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import *
from .forms import *
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.conf import settings 
from django.core.mail import send_mail 
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)


def index(request):
    posts = Post.objects.all().filter(date__lte=timezone.now()).order_by('-date')
    return render(request, 'index.html', {'posts':posts})

def add_image(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return False
    
    return render(request, 'add_image.html', {'form':ImageForm,})

def search_results(request):
    
    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})

# def welcome_email(request):
#     if request.method == 'POST':
#         username = request.POST('username')
#         password = request.POST('password')
#         email = request.POST('email')
#         user = User.objects.create_user(
#             username = username,
#             email = email,
#             password = password,
#         )
        
#         login(request, user)
        
#         subject = 'welcome to Insta Clone'
#         message = f'Hi {user.username}, thank you for registering in Insta Clone. Enjoy the app..'
#         email_from = settings.EMAIL_HOST_USER 
#         recipient_list = [user.email] 
#         send_mail( subject, message, email_from, recipient_list ) 

#         return redirect('/')
#     return render(request, 'django_registration/registration_form.html', {'form': form})

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(request,'/')
    
    return render(request, '/django_registration/login.html')
        
@login_required
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/')
    
    
