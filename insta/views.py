from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http  import HttpResponse
import datetime as dt
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import *
from .forms import *
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout

def index(request):
    return render(request, 'index.html')

def search_results(request):
    
    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})

@login_required
def welcome_email(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            name = self.cleaned_data['username']
            email = self.cleaned_data['email']
            recipient = SignupForm(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)
            HttpResponseRedirect('index')
    else:
        form = SignupForm()
        
    return render(request, 'django_registration/registration_form.html', {"form":form})

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
    
    
