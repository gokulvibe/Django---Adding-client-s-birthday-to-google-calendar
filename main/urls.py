from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('success',views.success,name='success'),
    path('dob',views.dob,name='dob'),
    path('send',views.send,name='send')
]
