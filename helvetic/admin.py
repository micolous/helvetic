from __future__ import absolute_import
from django.contrib import admin
from .models import Scale, UserProfile, Measurement, AuthorisationToken

class ScaleAdmin(admin.ModelAdmin):
	list_display = ('hw_address', 'ssid', 'owner')


class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'short_name', 'birth_date', 'height', 'gender')


class MeasurementAdmin(admin.ModelAdmin):
	list_display = ('user', 'scale', 'when', 'weight', 'body_fat')
	list_filter = ('user', 'scale')


class AuthorisationTokenAdmin(admin.ModelAdmin):
	list_display = ('user', 'expires')


for x in (
	(Scale, ScaleAdmin),
	(UserProfile, UserProfileAdmin),
	(Measurement, MeasurementAdmin),
	(AuthorisationToken, AuthorisationTokenAdmin),
):
	admin.site.register(*x)

