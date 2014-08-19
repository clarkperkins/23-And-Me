from django.conf.urls import patterns, url
from ancestry import views

urlpatterns = patterns('ancestry.views',

    url(r'^$', 'home', name='home'),
    url(r'^login/$', 'api_login', name='api_login'),
    url(r'^logout/$', 'api_logout', name='api_logout'),
    url(r'^callback/$', 'api_callback', name='api_callback'),
    url(r'^haplogroups/$', views.HaplogroupsAPIView.as_view(), name='haplogroups'),
    url(r'^ancestry/$', views.AncestryAPIView.as_view(), name='ancestry'),
    url(r'^neanderthal/$', views.NeanderthalAPIView.as_view(), name='neanderthal'),
    url(r'^genotypes/$', views.GenotypesAPIView.as_view(), name='genotypes')
)
