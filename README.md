### Intelligent Infrastructure Management for Cloud Deployments
***
#### System Overview
The Intelligent Infrastructure Management system is developed in Python (backend), RDF (metadata modeling), and JS (front end). The backend APIs are served using Django and RDF is SPARQL enabled using Apache Fuseki. We use Django 1.4.* and this can be downloaded [from here](https://www.djangoproject.com/download/1.4.13/tarball/). Django installation can be done using pip. It is recommended to create a [virtuanenv](http://virtualenv.readthedocs.org/en/latest/) and install Django inside of it. Once installed, change to iim_poc directory and run ```python manage.py runserver``` to start django

[Apache Fuseki](http://jena.apache.org/documentation/serving_data/) is a SPARQL end point and is used for serving RDF data over HTTP. The Fuseki jars needed to run on *ix is already checked in. To start Fuseki, run the start script inside Fuseki directory.

#### FS Structure
The file system is organized in the following manner. The top level folders are backend and ontologies. Inside the backend folder, we have the web app content in iim_poc, static, and template folders. Static has the css and javascript files. Templates have the html templates. The fuseki folder has the fuseki jars and the start script.

To access the ontologies, check out the ontologies branch. 
***
#### Uploading the Ontologies to Fuseki
Once started, go the Fuseki url (port 3030 is default), go to the control panel, and select the workspace (/Users/namelessnerd/TBCMEWorkspace/intelligentInfrastructure/). Scroll down to the bottom to the upload area and upload the ontology files. There are some example SPARQL scripts in the file named sparql under Fuseki directory for testing.
***
#### Django Structure
Urls.py has the url to function mappings. The two view files (controllers in other MVC frameworks is known as view in Django) are views and ontologyAPIs. There are under backend/iim_poc/iim_poc. Please make sure to follow [PEP-8](http://legacy.python.org/dev/peps/pep-0008/) standards while editing code. 

###### Please make sure to change the TEMPLATE_DIRS and STATIC_DIRS folders in settings.py (under iim_poc/iim_poc) to point to the directories in your local FS. It is ```path to backend+/iim_poc/{static | templates}```

For each API method, there is a test dictionary that captures a 2 node subgraph that we use to test the API and Front end controls. These dictionaries make sure that when the right data is sent back, the frontend behaves the way we want. 


