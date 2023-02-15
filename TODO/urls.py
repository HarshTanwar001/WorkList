from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('signin', views.signin, name='signin'),
    path('add', views.add, name='add'),
    path('create', views.create, name='create'),
    path('update', views.update, name='update'),
    path('save', views.save, name='save'),
]
