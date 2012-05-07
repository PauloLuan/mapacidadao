# -*- coding: utf-8 -*-
import urllib2
import pprint
import json

def getGeoCode(address=""):

    add = urllib2.quote(address)
    geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false&region=br" % add
    req = urllib2.urlopen(geocode_url)
    jsonResponse = json.loads(req.read())
    #pprint.pprint(jsonResponse)


    return jsonResponse

class GoogleGeoCode(object):

    def __init__(address=None, point=None,  csv=None, sensor='false', region='br'):

        self.json_response = None
        self.google_maps_api_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=%s&region=%s"


        add_urled = urllib2.quote(address)
        region_urled = urllib2.quote(region)

        geocode_url = self.google_maps_api_url % (address or point, sensor, region_urled)
        req = urllib2.urlopen(geocode_url)

        self.json_response = json.loads(req.read())
        if data["status"] != "OK":
            raise ValueError(data["status"])
        else:
            _set_params_(data)

    def _set_params_(self, data):

        pass

