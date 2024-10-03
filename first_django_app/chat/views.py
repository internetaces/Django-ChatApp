from django.shortcuts import render, get_object_or_404
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
			if user.first_name != "":
					return HttpResponseRedirect(request.POST.get('redirect'))
			else:
					return render(request, 'auth/complete.html', {'redirect': redirect})
		else:
			return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
	return render(request, 'auth/login.html', {'redirect': redirect})

def register_view(request):
	redirect = request.GET.get('next')
	if request.method == 'POST':
		User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))

	return render(request, 'auth/register.html', {'redirect': redirect})

def complete_view(request):
	if request.method == 'POST':
		user = get_object_or_404(User, username=request.user.username)
		user.first_name = request.POST.get('first_name')
		user.save()

		return render(request, 'chat/index.html')  # RICHTIGE WEITERLEITUNG zum CHAT FEHLT NOCH!!!!!
	else:
		return render(request, 'auth/complete.html')  

def front_view(request):
    return render(request, 'static/front.html')



