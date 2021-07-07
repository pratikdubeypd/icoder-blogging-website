from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path('', views.blogHome, name='BlogHome'),
    path('<str:slug>', views.blogPost, name='BlogPost'),
    path('postcomment/post', views.postComment, name='postComment'),
]
