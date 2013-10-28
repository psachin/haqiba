from django.conf.urls import patterns, include, url
from emacshaqiba import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^emacs_config/$', views.emacs_config, name='emacs_config'),
    url(r'^about/$', views.about, name='about'),
    url(r'^register/$', views.register, name='register'), 
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
#    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^submit_code/$', views.submitcode, name='submitcode'),
    url(r'^code/(?P<code_name>\w+)/$', views.display_code, 
        name='display_code'),
)
