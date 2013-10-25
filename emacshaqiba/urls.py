from django.conf.urls import patterns, include, url
from emacshaqiba import views

urlpatterns = patterns(
    '',
    url(r'^$', views.submitcode, name='submitcode'),
)
