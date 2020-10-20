from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
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
from django.urls import reverse
from django.db import transaction

@login_required
def index(request):
    posts = Post.objects.all().filter(date__lte=timezone.now()).order_by('-date')
    
    return render(request, 'index.html', {'posts':posts})

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    avatar = Profile.objects.all()
    posts = Post.objects.filter(user=user).order_by("-date")
    
    post_count = Post.objects.filter(user=user).count()
    follower_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
    
    return render(request,'profile/profile.html', {'user':user, 'profile':profile, 'posts':posts, 'avatar':avatar, 'post_count':post_count, 
                                                   'follower_count':follower_count, 'following_count':following_count,'follow_status':follow_status})

@login_required
def timeline(request):
    user = request.user
    stream = Stream.objects.filter(user=user)
    posts = Post.objects.all().filter(date__lte=timezone.now()).order_by('-date')
    
    group_ids = []
    
    for items in stream:
        group_ids.append(items.post_id)
        
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-date')
    
    return render(request, 'timeline.html', {'posts':posts, 'stream':stream,'post_items':post_items})

@login_required
def follow(request, username, option):
    user = request.user
    folllowing = get_object_or_404(User, username=username)
    
    try:
        f, created = Follow.objects.get_or_create(follower=user, following=folllowing)
        
        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=folllowing, user=user).all().delete()
            
        else:
            posts = Post.objects.all().filter(user=folllowing)[:10]
            
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=user, date=post.date, following=folllowing)
                    stream.save()
                    
        return HttpResponseRedirect(reverse('profile', args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))      

@login_required
def single_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    comments = Comment.objects.filter(id=post_id).order_by('-date')
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            return redirect('/')
        else:
            form = CommentForm()
    
    return render(request, 'single_post.html', {'post':post, 'form':CommentForm, 'comments':comments})    

@login_required
def add_image(request):
    userX = request.user
    user = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.profile = user
            data.user = userX
            data.save()
            return redirect('/')
        else:
            return False
    
    return render(request, 'add_image.html', {'form':ImageForm,})

@login_required
def profile_form(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            return redirect('/')
        else:
            form = ProfileForm()
    legend = 'Create Profile'
    
    return render(request, 'profile/update.html', {'form':ProfileForm, 'legend':legend})

@login_required
def profile_edit(request,username):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            return redirect('profile')
        else:
            form = ProfileForm()
    legend = 'Edit Profile'
    return render(request, 'profile/update.html', {'legend':legend, 'form':ProfileForm})

@login_required
def like(request,post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.like
    
    liked = Likes.objects.filter(user=user, post=post).count()
    
    if not liked:
        like = Likes.objects.create(user=user,post=post)
        
        current_likes = current_likes + 1
        
    else:
        Likes.objects.filter(user=user,post=post).delete()
        current_likes = current_likes - 1
        
    post.like = current_likes
    post.save() 
    
    return HttpResponseRedirect(reverse('MainPage'))       
     

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
    
    
