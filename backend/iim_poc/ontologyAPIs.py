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
# IIMPoC Dependencies
#---------------------------------------------------------------------------------------

policy= [{'uri':'http://ontology.techlabs.acn.com/appModel#WebServer',
						'name':'Web Server',
						'policies': [
							{'uri':'http://ontology.techlabs.acn.com/policyModel#SecurityPolicy', 
							'name':'Web Server Security Policy'},
							{'uri':'http://ontology.techlabs.acn.com/policyModel#AuthenticationPolicy', 
							'name':'Web Server Authentication Policy'},
							],
						},
						{'uri':'http://ontology.techlabs.acn.com/appModel#Database',
						'name':'Database Server',
						'policies': [
							{'uri':'http://ontology.techlabs.acn.com/policyModel#DBSecurityPolicy', 
							'name':'Database Server Encryption Policy'},
							{'uri':'http://ontology.techlabs.acn.com/policyModel#StoragePolicy', 
							'name':'Database Server Storage Policy'},
							],
						},
						{'uri':'http://ontology.techlabs.acn.com/appModel#ApplicationServer',
						'name':'Application Server',
						'policies': [
							{'uri':'http://ontology.techlabs.acn.com/policyModel#EncryptionPolicy', 
							'name':'Application Server Encryption Policy'},
							],
						},
					]

application_policy=[{
											'app_uri':'http://ontology.techlabs.acn.com/appModel#nginx',
												'policies':{
													'policy_uri':'http://ontology.techlabs.acn.com/policyModel#SecurityPolicy',
													'name':'Nginx Security Module',
												},
										},
									]

import query_helper

def get_domains(request):
	domains= [{'name':'Banking', 
						  'uri':'http://ontology.techlabs.acn.com/appModel#banking'}, 
						{'name':'Insurance', 
						 'uri':'http://ontology.techlabs.acn.com/appModel#insurance'},]
	return HttpResponse(simplejson.dumps(domains))

def get_application_type(request):
	appTypes= [
						{'name':'Consumer Banking API', 
						 'uri':'http://ontology.techlabs.acn.com/appModel#consumerBankAPI',}, 
						{'name':'Consumer Credit Card Application API',
						 'uri':'http://ontology.techlabs.acn.com/appModel#consumerCCAPI',},
						{'name':'Small Business Banking API',
						 'uri':'http://ontology.techlabs.acn.com/appModel#smallBusinessBankAPI',},	
						]
	# return HttpResponse(request.GET['domain'])
	return HttpResponse(simplejson.dumps(appTypes))#[request.GET['domain']]))


construct_query= lambda query_string: query_helper.prefix +' '+query_string

query_URL= 'http://localhost:3030/work/Accenture/ACP/PoC/ontologies/query'

def parse_SPARQL_response(SPARQL_response, params):
	bindings= SPARQL_response['results']['bindings']	
	result_array={param:[] for param in params}
	for binding in bindings:
		for param in params:
			try:
				result_element= ([binding[param]['value'], binding[param]['value'].split('#')[-1]] 
			  							if binding[param]['type']=='uri' else binding[param][value])
				result_array[param].append(result_element)
			except KeyError, e:
				pass
	return result_array			

def get_middleware(request):
	query_stub= """SELECT ?middleware ?relationship WHERE 
								{?relationship rdfs:domain appModel:Application . 
								?relationship rdfs:range ?middleware . 
								?middleware rdfs:subClassOf appModel:Middleware}"""
	print construct_query(query_stub)
	payload= {'query':construct_query(query_stub)}
	query_response= requests.get(query_URL, params=payload)
	print query_response
	return HttpResponse(simplejson.dumps(
						parse_SPARQL_response(query_response.json(),
																 ['middleware','relationship'])
																	)
											)

def get_policy(request):
	# query='SELECT ?policy ?x ?equivalentClasses ?constraint WHERE ' \
	# 		' {?x rdfs:range <'+ request.GET['artifact'] +'>  . ?x rdfs:domain ?policy . ?policy rdfs:subClassOf iPol:InfrastructurePolicyConstruct . ' \
	# 		'?y rdfs:domain ?policy . ?y rdfs:range ?constraint . ?constraint rdfs:subClassOf iPol:InfrastructurePolicyConstraint . ' \
	# 		'?constraint owl:equivalentClass ?equivalentClasses }'
	# payload= {'query':construct_query(query)}
	# query_response= requests.get(query_URL, params=payload)
	print 'foo'
	try:
		policyToReturn= {'Status':'Error. No policy associated with middleware'}
		for p in policy:
			print p['uri']
			print p['policies']
			print p
			print request.GET['middleware']
			if p['uri']== request.GET['middleware']:
				policyToReturn= p['policies'] 
				break
		return HttpResponse(simplejson.dumps(policyToReturn))
	except KeyError, k:
		print k
		return HttpResponse(simplejson.dumps(policy))

	# return HttpResponse(simplejson.dumps(parse_SPARQL_response(query_response.json(), ['equivalentClasses','x','policy'])))	
	
	

def get_subClasses(request):
	print 'inside subclass'
	query= 'SELECT ?subClasses WHERE {?subClasses rdfs:subClassOf* <' + \
					request.GET['parentClass'] + '> . ' + \
								'NOT EXISTS { ?child rdfs:subClassOf ?subClasses}' + \
						'}'
	print construct_query(query)
	payload= {'query':construct_query(query)}
	query_response= requests.get(query_URL, params=payload)
	return HttpResponse(simplejson.dumps(parse_SPARQL_response(query_response.json(), ['subClasses'])))	

def get_policy_module(request):
	try:
		policyToReturn= {'Status':'Error. No policy associated with middleware'}
		for pol in application_policy:
			if pol['app_uri']==request.GET['appURI']:
				for p in pol['policies']:
					if p['policy_uri']==request.GET['policyURI']:
						policyToReturn= p
						break
				break
		return HttpResponse(simplejson.dumps(policyToReturn))
	except KeyError, e:
		return HttpResponse(simplejson.dumps(policyToReturn))

def get_policy_components(request):
	query= 'SELECT ?policyModule WHERE{ '\
			'?policyModule rdfs:subClassOf* <'+ request.GET['policyModule'] + '> .'\
			'?rel rdfs:domain <' + request.GET['component'] + '> .'\
			'?rel rdfs:range ?policyModule .}'
	payload= {'query':construct_query(query)}		
	query_response= requests.get(query_URL, params=payload)
	print query_response.json()
	return HttpResponse(simplejson.dumps(parse_SPARQL_response(query_response.json(), ['policyModule'])))	


