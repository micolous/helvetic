from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import datetime, pytz, random, string


class Scale(models.Model):
	hw_address = models.CharField(
		max_length=12,
		help_text='Ethernet address of the Aria'
	)

	ssid = models.CharField(
		max_length=64,
	)

	fw_version = models.PositiveIntegerField(null=True, blank=True)
	battery_percent = models.PositiveIntegerField(null=True, blank=True)
	auth_code = models.BinaryField(max_length=16, null=True, blank=True)

	POUNDS = 0x00
	STONES = 0x01
	KILOGRAMS = 0x02
	UNIT_CHOICES = (
		(POUNDS, 'Pounds'),
		(STONES, 'Stones'),
		(KILOGRAMS, 'Kilograms')
	)

	unit = models.PositiveIntegerField(
		choices=UNIT_CHOICES,
		default=KILOGRAMS,
		help_text='Display units for the scale.'
	)

	owner = models.ForeignKey(
		User,
		help_text='Owner of these scales.'
	)


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


class Measurement(models.Model):
	user = models.ForeignKey(
		User,
		blank=True,
		null=True
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
	return datetime.datetime.now(pytz.UTC) + datetime.timedelta(hours=1)

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

