from .models import UserData
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render

import re


def index(request):
    return render(request, 'index.html', {'msg': None})


# view to register the user then log the user in and save user credentials in the db
def register(request):
    id = request.POST['id'].strip()
    pwd = request.POST['pwd'].strip()

    # checking if user is trying to use a non-supported special character in their user id
    x = re.findall("[^\s0-9a-zA-Z_@.+-]", id)

    if x:
        return render(request, 'index.html', {'msg': 'User IDs may contain whitespaces, alphanumeric, _, @, +, . and - characters only'})

    # checking if user id has already been taken
    data = UserData.objects.filter(id=id)

    if data:
        return render(request, 'index.html', {'msg': 'User ID already taken'})

    user = User.objects.create_user(username=id, password=pwd)
    user.save()
    auth_login(request, user)

    data = UserData(id=id)
    data.save()

    return render(request, 'tasks.html', {'tasks': None})


def login(request):
    return render(request, 'login.html', {'msg': None})


# view to signin the user if the user has already registered
def signin(request):
    id = request.POST['id'].strip()
    pwd = request.POST['pwd'].strip()

    user = authenticate(username=id, password=pwd)
    
    if user:
        auth_login(request, user)

        data = UserData.objects.filter(id=request.user)
        tasks = None
        
        if data[0].tasks:
            tasks = data[0].tasks

        return render(request, 'tasks.html', {'tasks': tasks})

    return render(request, 'login.html', {'msg': 'Wrong ID and/or Password'})


def add(request):
    return render(request, 'add.html')


# view to create tasks and save them in the db
def create(request):
    data = UserData.objects.filter(id=request.user)
    tasks = data[0].tasks

    # checking if tasklist for the user exists or not
    if not tasks:
        tasks = {}

    for new_task in request.POST.getlist('id'):
        tasks[new_task.strip()] = 0

    UserData.objects.filter(id=request.user).update(tasks=tasks)

    return render(request, 'tasks.html', {'tasks': tasks})


# view to update a task/ mark task as complete or incomplete/ delete the task and save changes in the db
def update(request):
    data = UserData.objects.filter(id=request.user)
    tasks = data[0].tasks

    for key in request.POST:
        # marking the task as complete/ incomplete based on button description
        if key.startswith('mark'):
            if tasks[key.split(':')[-1]]:
                tasks[key.split(':')[-1]] = 0
            else:
                tasks[key.split(':')[-1]] = 1

        # rendering 'edit.html' to edit a task based on button description
        elif key.startswith('edit'):
            txt = key.split(':')[-1]

            return render(request, 'edit.html', {'txt': txt})
        
        # deleting the task based on button description
        elif key.startswith('delete'):
            tasks.pop(key.split(':')[-1])

    UserData.objects.filter(id=request.user).update(tasks=tasks)

    return render(request, 'tasks.html', {'tasks': tasks})


# view to update the description of a task and save changes in the db
def save(request):
    data = UserData.objects.filter(id=request.user)
    tasks = data[0].tasks

    for key in request.POST:
        if key.startswith('id'):
            new_task, old_task = request.POST[key].strip(), key.split(':')[-1]

            # checking if the user updated the description of the task or not
            if new_task != old_task:
                tasks[new_task] = tasks[old_task]
                tasks.pop(old_task)

                UserData.objects.filter(id=request.user).update(tasks=tasks)

    return render(request, 'tasks.html', {'tasks': tasks})
