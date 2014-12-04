from __future__ import absolute_import
from django.conf.urls import patterns, include, url
from .views import aria_api

urlpatterns = patterns('',
	url(
		r'^scale/register$',
		aria_api.ScaleRegisterView.as_view(),
		name='scale_register'
	),

	url(
		r'^scale/upload$',
		aria_api.ScaleUploadView.as_view(),
		name='scale_upload'
	),

	#url(r'^$', 'helvetic.views.home', name='home'),
)
