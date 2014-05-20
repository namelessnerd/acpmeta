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

def get_domains(request):
	domains= [{'name':'Banking', 'icon':'/static/img/bankingIcon.jpeg'}, {'name':'Insurance','icon':'/static/img/insIcon.jpeg',},]
	return HttpResponse(simplejson.dumps(domains))


construct_query= lambda query_string: query_helper.prefix +' '+query_string

query_URL= 'http://localhost:3030/work/Accenture/ACP/PoC/ontologies/query'

def parse_SPARQL_response(SPARQL_response, params):
	bindings= SPARQL_response['results']['bindings']	
	result_array={param:[] for param in params}
	for binding in bindings:
		for param in params:
			try:
				result_element= [binding[param]['value'], binding[param]['value'].split('#')[-1]] if binding[param]['type']=='uri' else binding[param][value]
				result_array[param].append(result_element)
			except KeyError, e:
				pass
	return result_array			

def get_middleware(request):
	print construct_query('SELECT ?middleware ?relationship WHERE{?relationship rdfs:domain appModel:Application . ?relationship rdfs:range ?middleware . ?middleware rdfs:subClassOf appModel:Middleware }')
	payload= {'query':construct_query('SELECT ?middleware ?relationship WHERE{?relationship rdfs:domain appModel:Application . ?relationship rdfs:range ?middleware . ?middleware rdfs:subClassOf appModel:Middleware }')}
	query_response= requests.get(query_URL, params=payload)
	print query_response
	return HttpResponse(simplejson.dumps(parse_SPARQL_response(query_response.json(), ['middleware','relationship'])))

def get_policy(request):
	query='SELECT ?policy ?x ?equivalentClasses ?constraint WHERE ' \
			' {?x rdfs:range <'+ request.GET['artifact'] +'>  . ?x rdfs:domain ?policy . ?policy rdfs:subClassOf iPol:InfrastructurePolicyConstruct . ' \
			'?y rdfs:domain ?policy . ?y rdfs:range ?constraint . ?constraint rdfs:subClassOf iPol:InfrastructurePolicyConstraint . ' \
			'?constraint owl:equivalentClass ?equivalentClasses }'
	payload= {'query':construct_query(query)}
	query_response= requests.get(query_URL, params=payload)

	return HttpResponse(simplejson.dumps(parse_SPARQL_response(query_response.json(), ['equivalentClasses','x','policy'])))	

def get_subClasses(request):
	print 'inside subclass'
	query= 'SELECT ?subClasses WHERE {?subClasses rdfs:subClassOf <'+request.GET['parentClass']+'>}'
	print query
	payload= {'query':construct_query(query)}
	query_response= requests.get(query_URL, params=payload)
	return HttpResponse(simplejson.dumps(parse_SPARQL_response(query_response.json(), ['subClasses'])))	

def get_policy_components(request):
	query= 'SELECT ?policyModule WHERE{ '\
			'?policyModule rdfs:subClassOf* <'+ request.GET['policyModule'] + '> .'\
			'?rel rdfs:domain <' + request.GET['component'] + '> .'\
			'?rel rdfs:range ?policyModule .}'
	payload= {'query':construct_query(query)}		
	query_response= requests.get(query_URL, params=payload)
	print query_response.json()
	return HttpResponse(simplejson.dumps(parse_SPARQL_response(query_response.json(), ['policyModule'])))	


