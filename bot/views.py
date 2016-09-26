from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

def index(request):
	return render(request, 'bot/home.html')

'''
class: Bot

description:
    - Bot class, inherits from Django View

attributes:
    name : bot's name (string)
    id : bot's groupme id (string)    

initializer input:
    name, id

functions:
	get() - NOT USED
	post()
	perform()
'''
class Bot(View):
    def __init__(self, botname, botid):
        self.botname = botname
        self.botid = botid

    #def get(self, request):
    #	return HttpResponse("lolget")

	def post(self, request):
		self.perform()
    	return HttpResponse("lolpost")

    def perform(self):
    	print ("lol, i've performed")