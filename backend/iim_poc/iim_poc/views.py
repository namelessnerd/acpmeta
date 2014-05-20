#---------------------------------------------------------------------------------------
# Python Dependencies
#---------------------------------------------------------------------------------------
import simplejson
import string
import time
import requests

#---------------------------------------------------------------------------------------
# Django Dependencies
#---------------------------------------------------------------------------------------
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

#---------------------------------------------------------------------------------------
# PoC Dependencies
#---------------------------------------------------------------------------------------
import query_helper

#return home 

def get_home(request):
	return render_to_response('page_template.html', {'page_title': 'Intelligent Infrastructure Management','page_content':'index.html',})


def get_onboarding(request):
	return render_to_response('page_template.html',{'page_title': 'Service Onboarding', 'page_content':'onboarding.html',})

