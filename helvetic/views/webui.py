# -*- mode: python; indent-tabs-mode: nil; tab-width: 2 -*-
"""
webui.py - misc web functionality
"""
from __future__ import absolute_import

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from ..models import Scale, UserProfile

class IndexView(LoginRequiredMixin, TemplateView):
  template_name = 'helvetic/index.html'
  http_method_names = ['get', 'head']

class ScaleListView(LoginRequiredMixin, ListView):
  def get_queryset(self):
    return Scale.objects.filter(
      Q(owner=self.request.user) | Q(users__user=self.request.user))

