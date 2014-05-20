from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'iim_poc.views.get_home', name='home'),
    url(r'^onboarding$', 'iim_poc.views.get_onboarding', name='home'),
    url(r'^get/domains$', 'iim_poc.ontologyAPIs.get_domains', name='home'),
    url(r'^get/apptype$', 'iim_poc.ontologyAPIs.get_application_type', name='home'),
    url(r'^get/subClass$', 'iim_poc.ontologyAPIs.get_subClasses', name='get middleware'),
	url(r'^get/middleware$', 'iim_poc.ontologyAPIs.get_middleware', name='get middleware'),
	url(r'^get/policy$', 'iim_poc.ontologyAPIs.get_policy', name='get middleware'),
    url(r'^get/policy/module$', 'iim_poc.ontologyAPIs.get_policy_module', name='get policy compoents'),
	url(r'^get/policy/components$', 'iim_poc.ontologyAPIs.get_policy_components', name='get middleware'),
    (r'^notes-bg-ico\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/notes-bg-ico.ico'}),
    # url(r'^iim_poc/', include('iim_poc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
