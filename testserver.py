#!/usr/bin/env python
from bottle import request, response, get, post, run, template
from time import time
from crc16 import crc16xmodem
import struct


@get('/scale/register')
def register():
	print 'register query = %r' % dict(request.query)
	return ''

@get('/scale/validate')
def validate():
	# Context: https://github.com/micolous/helvetic/issues/1
	print 'validate query = %r' % dict(request.query)
	return 'T'


@post('/scale/upload')
def upload():
	print 'headers = %r' % dict(request.headers)
	response.set_header('Content-Type', 'application/octet-stream;charset=UTF-8')

	body = request.body.read()
	# version 3 protocol
	proto_ver, battery_pc, mac, authcode = struct.unpack('<LL6s16s', body[:30])
	body = body[30:]
	print 'upload: %d / %d%% / %r / %r' % (proto_ver, battery_pc, mac, authcode)

	fw_ver, unknown2, ts, measurement_count = struct.unpack('<LLLL', body[:16])
	body = body[16:]
	print 'fw = %d / u33 = %d / ts = %d / count = %d' % (fw_ver, unknown2, ts, measurement_count)

	for x in range(measurement_count):
		if len(body) < 32:
			print 'oops, not enough bytes to decode measurement!'
			break

		id2, imp, weight, ts, uid, fat1, covar, fat2 = \
			struct.unpack('<LLLLLLLL', body[:32])
		print 'id2 = %d / imp = %d / weight = %.3f / ts = %d' % (id2, imp, weight/1000., ts)
		print 'uid = %d / fat1 = %d / covar = %d / fat2 = %d' % (uid, fat1, covar, fat2)
		body = body[32:]

	print "checksum = %r" % body

	d = struct.pack('<LBBBLL16x20sLLLBLLLLLLLLL',
		int(time()), # timestamp

		0x02, # units, 0x02 = KG
		0x32, # status (configured)
		0x01, # unknown
		1, # user count
		
		1, # userid = 1
		#'ABC' + (' '*17), # Initials of user
		'MICHAEL' + (' '*(20-7)),
		
		89000, # min tolerance (weight, g)
		97000, # max tolerance (weight, g)
		
		25,   # age, years
		0x34, # gender, male=0x02, female=0x00, unknown=0x34
		1900, # height, mm
		
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

run(host='0.0.0.0', port=80)

