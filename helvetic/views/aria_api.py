from __future__ import absolute_import
from base64 import b16encode
from crc16 import crc16xmodem
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from string import hexdigits
import struct
from time import time

from ..models import AuthorisationToken, Measurement, Scale, utcnow


class ScaleRegisterView(View):
	def get(self, request):
		if 'serialNumber' not in request.GET:
			return HttpResponseBadRequest('serialNumber missing')
		if 'token' not in request.GET:
			return HttpResponseBadRequest('token missing')
		if 'ssid' not in request.GET:
			return HttpResponseBadRequest('ssid missing')

		serial = request.GET['serialNumber'].upper()
		token = request.GET['token']
		ssid = request.GET['ssid']
		
		if len(serial) != 12:
			return HttpResponseBadRequest('serialNumber must be 12 bytes')
		if any(((x not in hexdigits) for x in serial)):
			return HttpResponseBadRequest('serial must only contain hex')

		# Lookup the authorisation token
		auth_token = AuthorisationToken.lookup_token(token)

		if auth_token is None:
			return HttpResponseForbidden('Bad auth token')

		owner = auth_token.user

		# Delete the token.
		auth_token.delete()

		# Register the Aria
		scale = Scale.objects.create(
			hw_address=serial,
			ssid=ssid,
			owner=owner
		)

		# Only return 200 OK
		return HttpResponse('')


class ScaleUploadView(View):
	@method_decorator(csrf_exempt)
	@method_decorator(transaction.atomic)
	def dispatch(self, *args, **kwargs):
		return super(ScaleUploadView, self).dispatch(*args, **kwargs)

	def post(self, request):
		real_now = int(time())
		body = request.body

		# Version 3 protocol
		proto_ver, battery_pc, mac, auth_code = struct.unpack('<LL6s16s', body[:30])
		body = body[30:]

		if proto_ver != 3:
			return HttpResponseBadRequest('Unknown protocol version: %d' % proto_ver)

		if battery_pc > 100 or battery_pc < 0:
			return HttpResponseBadRequest('Battery percentage must be 0..100 (got %d)' % battery_pc)

		mac, auth_code = [b16encode(x) for x in (mac, auth_code)]
		scale = None

		try:
			scale = Scale.objects.get(hw_address=mac)
		except Scale.DoesNotExist:
			return HttpResponseBadRequest('Unknown scale: %s' % mac)

		# Check authcode
		if scale.auth_code is None or scale.auth_code == '':
			scale.auth_code = auth_code
		elif scale.auth_code != auth_code:
			return HttpResponseForbidden('Invalid auth code')

		scale.battery_percent = battery_pc

		fw_ver, unknown2, scale_now, measurement_count = struct.unpack('<LLLL', body[:16])
		body = body[16:]
		skew = scale_now - real_now
		print 'scale = %d, now = %d (%d skew)' % (scale_now, real_now, skew)

		scale.fw_version = fw_ver
		scale.save()
		for x in range(measurement_count):
			if len(body) < 32:
				return HttpResponseBadRequest('Measurement truncated.')

			id2, imp, weight, ts, uid, fat1, covar, fat2 = \
				struct.unpack('<LLLLLLLL', body[:32])

			# Record the measurement
			# Look up the owner of this measurement
			if uid == 0:
				measured_user = None
			else:
				try:
					measured_user = User.objects.get(id=uid)
				except User.NotFound:
					measured_user = None
			measurement = Measurement.objects.create(
				user=measured_user,
				scale=scale,
				when=utcnow() - timedelta(seconds=skew + (scale_now - ts)),
				weight=weight,
				body_fat=Decimal(fat1) / Decimal(1000),
			)
			
			body = body[32:]

		# Formulate a response
		scale_users = scale.users.all()
		response = struct.pack('<LBBBL',
			int(time()), # Fill with current time, to account for processing delay
			scale.unit,
			0x32, # status = configured
			0x01, # unknown
			len(scale_users)
		)
		
		# Insert user info
		for profile in scale_users:
			last_weight = last_body_fat = min_var = max_var = 0
			last_measurement = profile.latest_measurement()
			if last_measurement is not None:
				last_weight = last_measurement.weight
				last_body_fat = int(last_mearement.body_fat * 1000)
				min_var = last_weight - 4000
				if min_var < 0:
					min_var = 0
				max_var = last_weight + 4000

			response += struct.pack('<L16x20sLLLBLLLLLLLLL',
				profile.user.id,
				profile.short_name[:20].ljust(20),
				min_var,
				max_var,
				profile.age(),
				profile.gender,
				profile.height,
				last_weight,
				last_body_fat,
				0, # covariance
				0, # another weight, we don't care
				0, # timestamp, don't care.
				0, # always 0
				3, # always 3
				0  # always 0
			)

		return HttpResponse(response + struct.pack('HBB', 
			crc16xmodem(response), # checksum
			0x66, # always 0x66
			0x00, # always 0x00
		))

