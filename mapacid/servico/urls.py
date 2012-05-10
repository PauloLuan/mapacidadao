from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    #url(r'^$', 'servico.views.home', name='home'),
    #url(r'^$', 'django.views.generic.simple.redirect_to', {'url':'editais/'}, name="sos-gestao"),
    url(r'^kml/', 'servico.views.kml', name="kml"),
    url(r'^ponto/$', 'servico.views.ponto_crud', name="ponto-crud"),
    

)
