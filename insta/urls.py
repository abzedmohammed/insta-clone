from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('', views.index, name='MainPage'),
    path('/subscribe', views.welcome_email, name='WelcomePage'),
    path('search/', views.search_results, name='search_results'),
    path('logout/', views.logout, name='logout'),
    path('accounts/login', views.login, name='login'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)