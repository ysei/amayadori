# -*- coding: utf-8 -*-

import datetime
import logging
import StringIO
import struct
import binascii
import zlib

import nowcast
import png




#print get_current_observed_time()
#print get_current_predictive_time()
#print create_image_url(211, datetime.datetime.now(), 0)
#print create_image_url(211, datetime.datetime.now(), 1)

#print "Content-Type: image/png"
#print ""
#time = get_current_observed_time()
#print get_image(211, time, 0)
#time = get_current_predictive_time()
#print get_image(211, time, 1)

print "Content-Type: text/plain"
print ""

time  = nowcast.get_current_observed_time()
image = nowcast.get_image(211, time, 0)

png = png.Png8bitPalette.load(image)
print png

dx = png.bitmap.width
dy = png.bitmap.height
bitmap = png.bitmap.bitmap
print dx
print dy
print bitmap

cindex = None
for i in range(0, len(png.palette.colors)):
  if png.palette.colors[i] == (102,102,102):
    cindex = i
print cindex

xx = []
for x in range(0, dx):
  if bitmap[100][x] == cindex:
    xx.append(x)
  if bitmap[200][x] == cindex:
    xx.append(x)
  if bitmap[300][x] == cindex:
    xx.append(x)
print xx

#for line in png.bitmap.bitmap:
#  print ",".join(["%02X" % x for x in line])
