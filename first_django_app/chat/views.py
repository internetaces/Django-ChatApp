from django.shortcuts import render
from .models import Message, Chat
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers

@login_required(login_url='/login/')
def index(request):
	if request.method == 'POST':
		print("Received data " + request.POST['textmessage'])
		myChat = Chat.objects.get(id=1)
		new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
		serialized_obj = serializers.serialize('json', [ new_message, ])
		return JsonResponse(serialized_obj[1:-1], safe=False) #vom 1. bis zum vorletzten [1:-1]
	chatMessages = Message.objects.filter(chat__id=1)
	return render(request, 'chat/index.html', {'messages' : chatMessages})

def login_view(request):
	redirect = request.GET.get('next', '/chat/')
	if request.method == 'POST':
		user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
		if user:
			login(request, user)
			return HttpResponseRedirect(request.POST.get('redirect'))
		else:
			return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
	return render(request, 'auth/login.html', {'redirect': redirect})

def register_view(request):
	redirect = request.GET.get('next')
	if request.method == 'POST':
		User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))

	return render(request, 'auth/register.html', {'redirect': redirect})



