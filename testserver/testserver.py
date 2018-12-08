#!/usr/bin/env python
from __future__ import print_function 
from bottle import request, response, get, post, run, template
from time import time
from datetime import datetime
import struct
from os import environ
from sys import argv

#from crc16 import crc16xmodem
from crcmod.predefined import mkCrcFun
crc16xmodem = mkCrcFun('xmodem')

# user details
GENDERS = {'f': 0, 'm': 2}

name = environ.get('HEL_USER', 'EXAMPLE')
min_tolerance = int(environ.get('HEL_MIN_TOLERANCE', 89000)) # grams
max_tolerance = int(environ.get('HEL_MAX_TOLERANCE', 97000)) # grams
age = datetime.now().year - int(environ.get('HEL_BIRTHYEAR', 1970)) # birthyear
gender = GENDERS.get(environ.get('HEL_GENDER', '')[:1].lower(), 0x34)
height = int(environ.get('HEL_HEIGHT', 1900)) # millimetres

name = name[:20].upper().ljust(20)
age = 1 if age < 1 else age

log_buffer = []
def log(f, *args):
	global log_buffer
	now = datetime.now().isoformat()
	o = f % args
	d = '%s: %s' % (now, o)
	print(d)
	log_buffer.append(d)
	log_buffer = log_buffer[-10:]

def get_config():
	return 'name: %s\ntolerance: %d - %d grams\nage: %d years\ngender: 0x%02x\nheight: %d millimetres' % (
		name, min_tolerance, max_tolerance, age, gender, height)


@get('/scale/register')
def register():
	log('register query = %r', dict(request.query))
	return ''

@get('/scale/validate')
def validate():
	# Context: https://github.com/micolous/helvetic/issues/1
	log('validate query = %r', dict(request.query))
	return 'T'


@post('/scale/upload')
def upload():
	log('headers = %r', dict(request.headers))
	response.set_header('Content-Type', 'application/octet-stream;charset=UTF-8')

	body = request.body.read()
	# version 3 protocol
	proto_ver, battery_pc, mac, authcode = struct.unpack('<LL6s16s', body[:30])
	body = body[30:]
	log('upload: %d / %d%% / %r / %r', proto_ver, battery_pc, mac, authcode)

	fw_ver, unknown2, ts, measurement_count = struct.unpack('<LLLL', body[:16])
	body = body[16:]
	log('fw = %d / u33 = %d / ts = %d / count = %d', fw_ver, unknown2, ts, measurement_count)

	for x in range(measurement_count):
		if len(body) < 32:
			log('oops, not enough bytes to decode measurement!')
			break

		id2, imp, weight, ts, uid, fat1, covar, fat2 = \
			struct.unpack('<LLLLLLLL', body[:32])
		log('id2 = %d / imp = %d / weight = %.3f / ts = %d', id2, imp, weight/1000., ts)
		log('uid = %d / fat1 = %d / covar = %d / fat2 = %d', uid, fat1, covar, fat2)
		body = body[32:]

	log('checksum = %r', body)

	d = struct.pack('<LBBBLL16x20sLLLBLLLLLLLLL',
		int(time()), # timestamp

		0x02, # units, 0x02 = KG
		0x32, # status (configured)
		0x01, # unknown
		1, # user count
		
		1, # userid = 1
		#'ABC' + (' '*17), # Initials of user
		name,
		
		min_tolerance, # min tolerance (weight, g)
		max_tolerance, # max tolerance (weight, g)
		
		age,   # age, years
		gender, # gender, male=0x02, female=0x00, unknown=0x34
		height, # height, mm
		
		0,    # some weight
		0,    # body fat
		0,    # covariance
		0,    # some other weight
		0,    # timestamp
		
		0,    # unknown
		3,    # unknown (always 3)
		0,    # unknown
	)

	return struct.pack('<100sHH',
		d,
		crc16xmodem(d), # checksum
		(0x19 + (1 * 0x4d)), # size of message
	)

@get('/')
def index():
	global log_buffer
	response.set_header('Content-Type', 'text/plain')
	return 'helvetic testserver.py server status\n\nConfig:\n%s\n\nLog:\n%s' % (
		get_config(), '\n'.join(log_buffer))


print('helvetic testserver.py')
print(get_config())
run(host=argv[1], port=int(argv[2]))

