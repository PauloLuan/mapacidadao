from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^starter/$', 'starter', name='sample_starter'),
    url(r'^fluid/$', 'fluid', name='sample_fluid'),
    url(r'^hero/$', 'hero', name='sample_hero'),
)
