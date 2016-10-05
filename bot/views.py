from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
#from django.views import View
#from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
import dbmgr
import json
import requests
from django.conf import settings

def index(request):
    return render(request, 'bot/home.html')

@csrf_exempt
def boobot(request):
    dbmgr1 = dbmgr.Dbmgr()
    if (request.method == "POST"):
        #get the name and message
        jsondata = json.loads(request.body)
        #if message is not corrupted
        if ('name' in jsondata and 'text' in jsondata):
            #save this in firebase
            dbmgr1.addMessage(jsondata['name'], jsondata['text'])
            #have the bot respond to anyone but itself
            if (jsondata['name'] != "Fister Roboto"):
                #botid = "6bae961d754f11ccd688753363" #wah bot
                botid = "000ccdb6b4bd1320e186cdc10f" #fister roboto
                postbody = {
                        "bot_id"  : botid,
                        "text"    : jsondata['text']
                        }
                for i in range(0,2):
                    requests.post(settings.GROUPME_URL, data=postbody)
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
'''
class Bot(View):
    def __init__(self, botname, botid):
        self.botname = botname
        self.botid = botid

    #def get(self, request):
    #   return HttpResponse("lolget")

    def post(self, request):
        self.perform()
        return HttpResponse("lolpost")

    def perform(self):
        print ("lol, i've performed")
'''