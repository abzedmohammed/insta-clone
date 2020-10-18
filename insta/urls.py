from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('', views.index, name='MainPage'),
    #path('/accounts/register', views.welcome_email, name='WelcomePage'),
    path('search/', views.search_results, name='search_results'),
    path('logout/', views.logout, name='logout'),
    path('accounts/login', views.login, name='login'),
    path('add_image/', views.add_image, name='addImage'),
    path('my_timeline/', views.timeline, name='timeline'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)