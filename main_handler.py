# -*- coding: utf-8 -*-

import os
import logging
import re
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import areamanager
import amayadori
import png
import latlngutil


class TopPage(webapp.RequestHandler):
  def get(self):
    values = {
      "redirect_url": "http://amayadori-opt.appspot.com/docomo/iarea",
    }

    path = os.path.join(os.path.dirname(__file__), "views/top.html")
    html = template.render(path, values)
    self.response.out.write(html)


class ViewPage(webapp.RequestHandler):
  def get(self, lat, lng):
    lnglat = (float(lng), float(lat))
    area = areamanager.get_nearest_area(lnglat)
    if area == None:
      self.error_message("範囲外です。")
      return

    xy = area.lnglat_to_xy(lnglat)

    current_time = amayadori.get_current_time()
    radar_time   = amayadori.get_radar_time(current_time)
    nowcast_time = amayadori.get_nowcast_time(current_time)
    time_table   = amayadori.get_time_table(radar_time, nowcast_time)

    records = []
    for (image_time, image_ordinal), present_time in time_table:
      image    = amayadori.get_image(area.code, image_time, image_ordinal)
      rainfall = amayadori.get_rainfall(image, xy)

      if rainfall[0] == rainfall[1]:
        rainfall_str = str(rainfall[0])
      else:
        rainfall_str = str(rainfall[0]) + "～" + str(rainfall[1])

      records.append({
        "type": ("現在" if image_ordinal == 0 else "予想"),
        "time": present_time.strftime("%H時%M分"),
        "rainfall": rainfall_str,
        "image_time": image_time.strftime("%Y%m%d%H%M"),
        "image_ordinal": ("%02i" % image_ordinal),
      })


    # http://amayadori-opt.appspot.com/ のためのGoogle Maps API Key
    mapkey = "ABQIAAAA-ys93Qu6HH7Py3ElrvrGIxQGMNRpk4DlDb3SBK780CawkJsqbhR6Q77-5by3FYPdmP6wscv2utyMUQ"

    values = {
      "area": str(area.code),
      "lat": str(lnglat[1]),
      "lng": str(lnglat[0]),
      "x": str(xy[0]),
      "y": str(xy[1]),
      "mapkey": mapkey,
      "radar_time": radar_time.strftime("%Y%m%d%H%M"),
      "nowcast_time": nowcast_time.strftime("%Y%m%d%H%M"),
      "records": records,
    }

    path = os.path.join(os.path.dirname(__file__), "views/view.html")
    html = template.render(path, values)
    self.response.out.write(html)

  def error_message(self, message):
    path = os.path.join(os.path.dirname(__file__), "error.html")
    html = template.render(path, {"message": message})
    self.response.out.write(html)


class DocomoIAreaRedirector(webapp.RequestHandler):
  def post(self):
    lat  = self.request.get("LAT")
    lng  = self.request.get("LON")
    xacc = self.request.get("XACC")
    logging.info("docomo-iarea: lat=" + str(lat) + " lng=" + str(lng) + " xacc=" + str(xacc))

    lat_deg = "%.4f" % latlngutil.dms_to_deg(lat)
    lng_deg = "%.4f" % latlngutil.dms_to_deg(lng)
    self.redirect("/view/" + lat_deg + "/" + lng_deg)

  def get(self):
    self.response.out.write("")


class DocomoGpsRedirector(webapp.RequestHandler):
  def get(self):
    lat  = self.request.get("lat")
    lng  = self.request.get("lon")
    xacc = self.request.get("x-acc")
    logging.info("docomo-gps: lat=" + str(lat) + " lng=" + str(lng) + " xacc=" + str(xacc))

    lat_deg = "%.4f" % latlngutil.dms_to_deg(lat)
    lng_deg = "%.4f" % latlngutil.dms_to_deg(lng)
    self.redirect("/view/" + lat_deg + "/" + lng_deg)


class TestPage(webapp.RequestHandler):
  def get(self):
    pass


if __name__ == "__main__":
  application = webapp.WSGIApplication(
    [
      (r"/", TopPage),
      (r"/view/(\-?\d+(?:\.\d+)?)/(\-?\d+(?:\.\d+)?)", ViewPage),
      (r"/docomo/iarea", DocomoIAreaRedirector),
      (r"/docomo/gps",   DocomoGpsRedirector),
      (r"/test",         TestPage),
    ],
    debug = True)
  run_wsgi_app(application)
