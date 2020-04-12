# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import sys
import json
import math
import logging
import calendar
from django.db import connection
from django.core.mail import mail_admins, send_mail
import datetime
import traceback
import bson
import time

import requests



import socket
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.conf import settings
from locations.models import Location, HistoricalKWInfo, Client, UserProfile, Dealer, Device
# from locations.models import Location, HistoricalKWInfo, Client, UserProfile, Dealer, Devices

from locations.report_helpers import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from pymongo import MongoClient
from bson import json_util
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
# from django.views.generic.simple import direct_to_template
import django.contrib.auth.views as auth_views
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.conf import settings
from random import random
from django.views.generic import TemplateView


pymongoclient = MongoClient(settings.MONGO_HOST,settings.MONGO_PORT)
adminDb = pymongoclient['admin']
adminDb.authenticate("root","beetroot");

dailydb=pymongoclient['daily']

lasttime = get_last_knack_mongo_record()

newrecords = get_new_records()

for record in newrecords:
    upload_record(record)


def get_last_knack_mongo_record:
    print('here')

def get_new_records:
    print('here')

def upload_record:
    print('here')


PROXY_URL = "http://proxy.kiteandlightning.com:8001/"
NEW_PROXY_URL = "http://proxy.unityesg.net:8001/"


class Command(BaseCommand):
  args = '<none>'
  help = 'Queries the proxy server and marks locations on or offline'

  def handle(self, *args, **options):
    try:
      rawkeys = urlopen(PROXY_URL + "list").read()
      rawkeys1 = urlopen(NEW_PROXY_URL + "list").read()


      keys = json.loads(rawkeys)
      keys1 = json.loads(rawkeys1)

      locs = Location.objects.filter(client_version__gte=4)
      for loc in locs:
        if (loc.new_proxy):

            if not (loc.key in keys1):

              if loc.is_online:
                print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "(GMT) -", loc.name, "went offline of", '"',NEW_PROXY_URL,'"!\n')
                loc.is_online = False
                loc.save()
            else:

              if not loc.is_online:

                print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "(GMT) -", loc.name, "is back online of", '"',NEW_PROXY_URL,'"!\n')


                loc.is_online = True
                loc.save()
        else:

            if not (loc.key in keys):

              if loc.is_online:
                print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "(GMT) -", loc.name, "went offline of", '"',PROXY_URL,'"!\n')

                loc.is_online = False
                loc.save()
            else:
              if not loc.is_online:
                print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "(GMT) -", loc.name, "is back online of", '"',PROXY_URL,'"!\n')


                loc.is_online = True
                loc.save()

    except Exception as e:
      raise CommandError(e)
