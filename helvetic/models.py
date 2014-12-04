from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
import pytz, random, string

def utcnow():
	return datetime.now(pytz.UTC)

class Scale(models.Model):
	hw_address = models.CharField(
		'Hardware address',
		max_length=12,
		help_text='Ethernet address of the Aria.'
	)

	ssid = models.CharField(
		'SSID',
		max_length=64,
		help_text='SSID of the WiFi network the Aria is connected to.'
	)

	fw_version = models.PositiveIntegerField(
		'Firmware version',
		null=True,
		blank=True,
	)

	battery_percent = models.PositiveIntegerField(
		'Battery percent remaining',
		null=True,
		blank=True
	)

	auth_code = models.CharField(
		'Authorisation code, in base16 encoding',
		max_length=32,
		null=True,
		blank=True
	)

	POUNDS = 0x00
	STONES = 0x01
	KILOGRAMS = 0x02
	UNIT_CHOICES = (
		(POUNDS, 'Pounds'),
		(STONES, 'Stones'),
		(KILOGRAMS, 'Kilograms')
	)

	unit = models.PositiveIntegerField(
		'Unit of measure',
		choices=UNIT_CHOICES,
		default=KILOGRAMS,
		help_text='Display units for the scale.'
	)

	owner = models.ForeignKey(
		User,
		help_text='Owner of these scales.',
		related_name='owned_scales'
	)
	
	users = models.ManyToManyField(
		'UserProfile',
		help_text='UserProfiles for the users of this scale.',
		related_name='used_scales',
		blank=True
	)

	def __unicode__(self):
		return self.hw_address

class UserProfile(models.Model):
	user = models.ForeignKey(
		User,
		unique=True
	)

	short_name = models.CharField(
		max_length=20,
		help_text='Short name for the user, displayed on the scales'
	)

	birth_date = models.DateField(
		help_text='Date when the user was born.'
	)

	height = models.PositiveIntegerField(
		help_text='Height of the user, in millimetres. Used to calculate body fat.'
	)

	MALE = 0x02
	FEMALE = 0x00
	UNKNOWN = 0x34
	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
		(UNKNOWN, 'Unknown')
	)

	gender = models.PositiveIntegerField(
		choices=GENDER_CHOICES,
		default=UNKNOWN,
		help_text='Biological gender of the user. Used to calculate body fat.'
	)

	def __unicode__(self):
		return unicode(self.user)

	def latest_measurement(self):
		"""
		Returns the last measurement for the user, or None if no measurement
		exists.
		"""

		try:
			return self.measurement.objects.all().order_by('-when')[0]
		except:
			return None

	def age(self, from_date=None):
		"""
		Returns the age of the user, in years.
		
		If no argument is specified, the age is calculated relative to today (in
		UTC).
		"""
		if from_date is None:
			from_date = utcnow().date()
		return relativedelta(from_date, self.birth_date).years

class Measurement(models.Model):
	user = models.ForeignKey(
		User,
		blank=True,
		null=True,
		related_name='measurement'
	)

	scale = models.ForeignKey(
		Scale
	)

	when = models.DateTimeField()

	weight = models.PositiveIntegerField(
		help_text='Weight measured, in grams.'
	)

	body_fat = models.DecimalField(
		max_digits=6, decimal_places=3,
		help_text='Body fat, measured as a percentage.',
		blank=True,
		null=True
	)

def _generate_auth_expiry():
	"""
	Generate an expiry time for an authorisation token (T + 1 hour)
	"""
	return utcnow() + timedelta(hours=1)

def _generate_auth_key():
	"""
	Generates a pseudorandom key for setting up the scales.
	"""
	return ''.join([random.choice(string.letters) for _ in range(10)])


class AuthorisationToken(models.Model):
	"""
	Used during the setup of scales.
	"""
	user = models.ForeignKey(
		User,
		unique=True
	)

	expires = models.DateTimeField(default=_generate_auth_expiry)
	key = models.CharField(
		max_length=10,
		default=_generate_auth_key
	)
	
	@classmethod
	def lookup_token(cls, key):
		"""
		Looks up the given key to see if there is a token that matches.
		
		Cleans up any expired tokens in the process.
		
		Returns None if no token is valid.
		"""
		now = utcnow()
		cls.objects.filter(expires__lte=now).delete()

		try:
			# Also sanity-check tokens here, in case delete fails or is not yet
			# consistent.
			return cls.objects.get(expires__gt=now, key=key)
		except cls.DoesNotExist:
			return


