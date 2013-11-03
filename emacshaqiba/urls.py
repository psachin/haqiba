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
    url(r'^profile/', views.profile, name='profile'),
    url(r'^submit_code/$', views.submitcode, name='submitcode'),
    url(r'^edit_code/$', views.editcode, name='editcode'),
    url(r'^edit_code_p/(?P<id>\d+)/$', views.editcode_p, name='editcode_p'),
    url(r'^delete_code/(?P<id>\d+)/$', views.delete_code, name='delete_code'),
    url(r'^code/(?P<id>\d+)/$', views.display_code, 
        name='display_code'),
    url(r'^display_bundle/$', views.display_bundle, name='display_bundle'),
)
