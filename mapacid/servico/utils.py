# -*- coding: utf-8 -*-
import urllib2
import pprint
import json


def getGeoCode(address=""):

    add = urllib2.quote(address)
    geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false&region=uk" % add
    req = urllib2.urlopen(geocode_url)
    jsonResponse = json.loads(req.read())
    #pprint.pprint(jsonResponse)
    return jsonResponse