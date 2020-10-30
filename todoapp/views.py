from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import Todoform
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, "todoapp/home.html")

def deletet(request, idid):
    todo=get_object_or_404(Todo, pk=idid, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currento')

def completed(request):
    todos=Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todoapp/completed.html', {'todos':todos})



def complete(request, idid):
    todo=get_object_or_404(Todo, pk=idid, user=request.user)
    if request.method == 'POST':
        todo.datecompleted=timezone.now()
        todo.save()
        return redirect('currento')
def viewtodo(request, idid):
    todo=get_object_or_404(Todo, pk=idid, user=request.user)
    if request.method == "GET":
        form=Todoform(instance=todo)
        return render(request, 'todoapp/ttodo.html', {'todo':todo, 'form': form})  
    else:
        try:
            form=Todoform(request.POST, instance=todo)
            form.save()
            return redirect('currento')
        except ValueError:
            return render(request, 'todoapp/ttodo.html', {'todo':todo, 'form': form, "error":'bad info'})  

def creattodo(request):
    if request.method == "GET":
        return render(request, "todoapp/create.html", {'form': Todoform()})
    else:
       
        try:
            form=Todoform(request.POST)
            latest=form.save(commit=False)
            latest.user=request.user
            latest.save()
            return redirect('currento')
        except ValueError:
            return render(request, "todoapp/create.html", {'form': Todoform(), 'error': 'bad data passed in'})

def signupuser(request):
    if request.method == "GET":
        return render(request, "todoapp/sign.html", {'form': UserCreationForm()})
    else:
    #create a new user
        if request.POST['password1']== request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currento')
            except IntegrityError:
                return render(request, "todoapp/sign.html", {'form': UserCreationForm(), 'error': 'username already taken, try another one'})

        else:
            return render(request, "todoapp/sign.html", {'form': UserCreationForm(), 'error': 'passwords didn\'t match'})
@login_required        
def currento(request):
    todos=Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todoapp/current.html', {'todos':todos})
def loginuser(request):
    if request.method == "GET":
        return render(request, "todoapp/login.html", {'form': AuthenticationForm(), })
    else:
        user1 = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        #if there is an issue with the user e.g....if the user doesn't exist, none will be returned
        if user1 is None:
            return render(request, "todoapp/login.html", {'form': AuthenticationForm(), 'error': 'username or password doesn\'t match'})
        else:
            login(request, user1)
            return redirect('currento')

def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')