from django.conf.urls import patterns, include, url

urlpatterns = patterns('ancestry.views',
    # Examples:
    # url(r'^$', 'geneology.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'home', name='home'),
    url(r'^login/$', 'api_login', name='api_login'),
    url(r'^logout/$', 'api_logout', name='api_logout'),
    url(r'^callback/$', 'api_callback', name='api_callback'),
    url(r'^call/$', 'call', name='call'),
)
