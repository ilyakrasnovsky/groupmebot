from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404

def index(request):
	return render(request, 'bot/home.html')

def boobot(request):
	context = {"data" : "meh"}
	if (request.method == "POST"):
		context = request.POST.dict()
	return JsonResponse(context)