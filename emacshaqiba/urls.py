from django.conf.urls import patterns, include, url
from emacshaqiba import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^emacs/$', views.emacs, name='emacs'),
    url(r'^about/$', views.about, name='about'),
    url(r'^register/$', views.register, name='register'), 
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/', views.profile, name='profile'),

    url(r'^code/submit/$', views.submitcode, name='submitcode'),
    url(r'^code/(?P<id>\d+)/$', views.display_code,  name='display_code'),
    url(r'^code/edit/$', views.editcode, name='editcode'),
    url(r'^code/edit/(?P<id>\d+)/$', views.editcode_p, name='editcode_p'),
    url(r'^code/delete/(?P<id>\d+)/$', views.delete_code, name='delete_code'),
    
    url(r'^package/submit/$', views.submit_package, name='submit_package'),
    url(r'^package/(?P<id>\d+)/$', views.display_package,  name='display_package'),
    url(r'^package/edit/$', views.editpackage, name='editpackage'),
    url(r'^package/edit/(?P<id>\d+)/$', views.editpackage_p, name='editpackage_p'),
    url(r'^package/delete/(?P<id>\d+)/$', views.delete_package, name='delete_package'),
    
    url(r'^bundle/submit/$', views.submit_bundle, name='submit_bundle'),
    url(r'^bundle/(?P<id>\d+)/$', views.display_bundle, name='display_bundle'),
    url(r'^bundle/edit/$', views.editbundle, name='editbundle'),
    url(r'^bundle/edit/(?P<id>\d+)/$', views.editbundle_p, name='editbundle_p'),
    url(r'^bundle/delete/(?P<id>\d+)/$', views.delete_bundle, name='delete_bundle'),

    url(r'^suggest_code/$', views.suggest_code, name='suggest_code'),
    
)
