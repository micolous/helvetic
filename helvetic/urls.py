from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'helvetic.views.home', name='home'),
)
