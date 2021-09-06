from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import *
from .forms import *

# Create your views here.


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('/')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'tasks/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('/')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('list')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'tasks/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')



@login_required(login_url='login')
def index(request):
	tasks= Task.objects.filter(user=request.user)

	count=tasks.filter(complete=False).count()

	form = TaskForm()

	if request.method =='POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			fs = form.save(commit=False)
			fs.user = request.user
			fs.save()
		return redirect('/')


	context = {'tasks':tasks, 'form':form,'count':count}
	return render(request, 'tasks/list.html', context)

def updateTask(request,pk):
	task = Task.objects.get(id=pk)

	form = TaskForm(instance=task)

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			fs = form.save(commit=False)
			fs.user = request.user
			fs.save()
		return redirect('/')
		
	context = {'form':form}

	return render(request, 'tasks/update_task.html', context)

def deleteTask(request, pk):
	item = Task.objects.get(id=pk)

	if request.method == 'POST':
		item.delete()
		return redirect('/')

	context = {'item':item}
	return render(request, 'tasks/delete.html', context)



