from django.conf.urls import patterns, include, url
from emacshaqiba import views
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'haqiba.views.home', name='home'),
    # url(r'^haqiba/', include('haqiba.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^emacshaqiba/', include('emacshaqiba.urls')),
                       url(r'^$', views.index),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root':settings.MEDIA_ROOT}),)

