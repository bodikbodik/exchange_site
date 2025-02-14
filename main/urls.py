from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('stocks/', views.stocks, name='stocks'),
    
    path("crypto/", views.crypto, name="crypto"),



    path('funds/', views.funds, name='funds'),
    path('currency/', views.currency, name='currency'),
]
