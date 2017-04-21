# -*- mode: python; indent-tabs-mode: nil; tab-width: 2 -*-
"""
registration.py - implements device registration
"""
from __future__ import absolute_import

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from ..models import AuthorisationToken

class RegistrationView(LoginRequiredMixin, TemplateView):
  template_name = 'helvetic/registration/register.html'
  http_method_names = ['get', 'head']

class CurlRegistrationView(LoginRequiredMixin, TemplateView):
  template_name = 'helvetic/registration/register_curl.html'
  http_method_names = ['post']

	def post(self, request):
	  # Delete existing tokens for the user.
	  AuthorisationToken.objects.filter(user=request.user).delete()
	
	  # Create a new token
	  auth_token, _ = AuthorisationToken.objects.get_or_create(user=request.user)
	  
	  return self.render_to_response(dict(auth_token=auth_token))
	
