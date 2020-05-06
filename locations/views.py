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
import pytz
import calendar

import requests
from .forms import EmailForm

from django.core.mail import send_mail

from django.utils import timezone


import socket
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.conf import settings
from locations.models import Product,Category,SubCategory,Order,ProductOrder,Customer
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
from django.http import FileResponse
from django.core import serializers

pymongoclient = MongoClient(settings.MONGO_HOST,settings.MONGO_PORT)
adminDb = pymongoclient['admin']
adminDb.authenticate("root","beetroot");

dailydb=pymongoclient['daily']


logger = logging.getLogger('django')







def index(request):
  return render_to_response("index.html")


def get_products(request):
    try:

        # from easy_timezones.signals import detected_timezone
        # print(detected_timezone)
        result = {'result': {'categories':[],'products':[],'occupied':[]}}


        products = Product.objects.all()
        categories = Category.objects.all()
        for category in categories:
            c = {'name':category.name,'subcategories':[]}
            # print(c)

            subcategories = SubCategory.objects.filter(category=category)
            for sub in subcategories:

                c['subcategories'].append(sub.name)
            result['result']['categories'].append(c)


        retproducts = []
        for prod in products:

            myimg = None
            if prod.image:

                myimg = '/static/' + str(prod.image).split('/')[1]
            jsonprod = {
               'name' : prod.name,
               'description' : prod.description,
               'price': prod.price,
               'image': myimg,
               



            }
            if prod.category:

                jsonprod['category'] = prod.category.name

            if prod.subcategory:

                jsonprod['subcategory'] = prod.subcategory.name

            retproducts.append(jsonprod)
        result['result']['products'] = retproducts

        occupied = []
        activeorders = Order.objects.filter(active=True)
        for i in activeorders:
            if i.delivery_slot:
                occupied.append(i.delivery_slot.timestamp())
        result['result']['occupied'] = occupied





        return JsonResponse(result)
    except:
         e = sys.exc_info()
         edict = {
             'error':str(e)
         }
         print('api_report -  error : ', e)
         return HttpResponse(status=500)

def post_order(request):

    try:
        stuff = json.loads(request.body.decode('utf-8'))
        cust = Customer.objects.filter(phone=stuff['custinfo']['phone']) | Customer.objects.filter(email=stuff['custinfo']['email'])
        cust = cust[0]
        if not cust:
            cust = Customer.objects.create(name=stuff['custinfo']['name'],
                            email =stuff['custinfo']['email'],
                            phone =stuff['custinfo']['phone'],
                            address =stuff['custinfo']['address1'],
                            optional =stuff['custinfo']['address2'],
                            province =stuff['custinfo']['province'],
                            postal =stuff['custinfo']['postal'],
                            city =stuff['custinfo']['city'],
                            country =stuff['custinfo']['country'])

        order = Order.objects.create(estimated_total=stuff['total'],
                        additional=stuff['additional'],
                        customer = cust,
                        active = True,
                        delivery_slot = datetime.datetime.utcfromtimestamp(stuff['ts']/1000).replace(tzinfo=pytz.utc))

        for i in stuff['cart']:
            prod = Product.objects.get(name=i['name'])
            prodord = ProductOrder.objects.create(product=prod,
                            measurement =i['measurement'],
                            quantity =i['quantity'],
                            order = order)
            if prodord.measurement == 'Tied Bunch':
                prodord.unit_price = prod.price_per_tied_bunch
            if prodord.measurement == 'Kg':
                prodord.unit_price = prod.price_per_kg
            if prodord.measurement == 'Unit':
                prodord.unit_price = prod.price_per_unit
            prodord.save()


        jsonreturn = {"result": "success"}


        return JsonResponse(jsonreturn)


    except:
        var = traceback.format_exc()

        print('api_report -  error : ', var)
        return HttpResponse(status=500)



# def robots(request):
#   return HttpResponse("User-agent: *\nAllow: /")
#
# def login(request, *args, **kwargs):
#
#   if request.method == 'POST':
#     if not request.POST.get('remember_me', None):
#       request.session.set_expiry(0)
#   return auth_views.login(request, *args, **kwargs)
#
#
# def get_email(request):
#
#     if request.method == 'POST':
#         form = EmailForm(request.POST)
#         if form.is_valid():
#             up = request.user.profile
#             up.first_name = form['fname'].value()
#             up.last_name = form['lname'].value()
#             up.email = form['email'].value()
#             up.phone = form['phone'].value()
#             up.new_email_update = datetime.datetime.now(tz=timezone.utc)
#             up.save()
#             send_mail(
#                 'Django user updated info',
#                 'Django user ' + up.first_name + ' ' + up.last_name + ', with Username: ' + up.user.username + ', just updated their info with Email: ' + up.email + ' and Phone: ' + up.phone,
#                 'notifications@unityesg.com',
#                 ['customerservice@unityesg.com'],
#                 fail_silently=False,
#             )
#
#             return HttpResponseRedirect("/")
#
#     else:
#
#         form = EmailForm()
#         # return render(request, 'blog/post_edit.html', )
#     return render(request, 'get_email.html',{'form': form})
#         # print(request)
#         # return render(request, 'get_email.html')
#
#
#
# def logout_view(request):
#   logout(request)
#   return HttpResponseRedirect("/")
#   # return HttpResponseRedirect("http://www.kiteandlightning.com/")
#
#
# def get_remote_username_for_profile(profile):
#   if (profile.remote_username is not None) and (len(profile.remote_username) > 0):
#
#     return profile.remote_username
#   else:
#
#     return profile.user.username
#
# def get_locations_for_profile(profile):
#
#   # admins see all locations
#   if profile.is_admin:
#     # print('1')
#
#     return Location.objects.all()
#   # else if specific locations are specified, that's all you see
#   elif profile.locations.count() > 0:
#     # print('2')
#
#     return profile.locations.all()
#   # else if you're a dealer, you see all locations below that dealer
#   elif profile.dealer:
#     # print('3')
#
#     clients = Client.objects.filter(dealer=profile.dealer)
#     return Location.objects.filter(client__in=clients)
#   # else if you're a client, you get all locations for that client
#   elif profile.client:
#     # print('4')
#     return Location.objects.filter(client=profile.client)
#   else:
#     return None
#
# def get_clients_for_profile(profile):
#   if profile.is_admin:
#     return Client.objects.all()
#   # else if specific locations are specified, that's all you see
#   elif profile.locations.count() > 0:
#     locations = profile.locations.all()
#     clients = Client.objects.filter(location__in=locations).distinct()
#     return clients
#   # else if you're a dealer, you see all locations below that dealer
#   elif profile.dealer:
#     return Client.objects.filter(dealer=profile.dealer)
#   # else if you're a client, you get all locations for that client
#   elif profile.client:
#     return Client.objects.filter(id=profile.client.id);
#   else:
#     return None
#
# def get_locations_for_client(profile, client):
#   if profile.is_admin:
#     return Location.objects.filter(client=client)
#   elif profile.locations.count() > 0:
#     return profile.locations.filter(client=client)
#   elif profile.dealer and profile.dealer == client.dealer:
#     return Location.objects.filter(client=client)
#   elif profile.client and profile.client == client:
#     return Location.objects.filter(client=client)
#   else:
#     return None
#
#
# ########################
# # SITE SETUP
#
# # called by remote units to create a new location record
# def site_setup(request):
#   try:
#     name = request.GET['name']
#     client = Client.objects.get(name="NEW INSTALLS")
#     loc = Location(name=name, client=client)
#     loc.save()
#
#     # resave, using the id as the tunnel offset
#     loc.tunnel_offset = loc.id
#     loc.save()
#
#     # send an email about this
#     #mail_admins("NEW INSTALL! %s" % loc.name, "%s\n%s\n%s\nssh -L 9000:127.0.0.1:9000 otto@bounce.kiteandlightning.com -p %s" % (loc.name, loc.key, loc.tunnel_offset, (20000 + loc.tunnel_offset)))
#
#     return JsonResponse({
#       'key':loc.key,
#       'secret_key':loc.secret_key,
#       'id':loc.tunnel_offset
#     })
#   except: return JsonResponse({'error': "No new site name specified"})
#
#
# #########################
# # FLASH CLIENT ENDPOINT
#
# @login_required
# def client(request):
#   key = request.GET.get('key', None)
#   user = request.GET.get('user', None)
#   force = request.GET.get('force', None)
#   locname = 'Remote Control'
#
#   try:
#     loc = Location.objects.get(key=key)
#     locname = loc.name
#     secret_key = loc.secret_key
#     p = request.user.profile
#   except:
#     return dashboard(request)
#
#   access = False
#
#   if p.is_admin:
#     access = True
#   elif p.locations.filter(pk=loc.pk).exists():
#     access = True
#   elif p.client is not None:
#     if loc.client.pk == p.client.pk:
#       access = True
#
#   if access:
#     return render(request, 'client.html', {
#       'key':key,
#       'secret_key':secret_key,
#       'user':user,
#       'force':force,
#       'locname':locname,
#       'version':loc.client_version,
#       'rnd':random()*1000,
#       'new_proxy':loc.new_proxy
#     })
#   else:
#     return dashboard(request)
#
#
# #######################
# # INTERNAL KL-ONLY REPORTS
#
# @login_required
# def internal_reports(request):
#   try:
#
#     p = request.user.profile
#     assert p.is_admin == True
#
#     if request.method == 'POST':
#       key = request.POST.get('key')
#       from_date = request.POST.get('from_date', None)
#       to_date = request.POST.get('to_date', None)
#       start_ts = datetime.datetime.strptime(from_date, "%m/%d/%Y")
#       end_ts = datetime.datetime.strptime(to_date, "%m/%d/%Y")
#     else:
#       # default to current month
#       d = datetime.datetime.now()
#       rng = calendar.monthrange(d.year, d.month)
#       start_ts = datetime.datetime(d.year, d.month, 1)
#       end_ts = datetime.datetime(d.year, d.month, rng[1])
#       from_date = start_ts.strftime("%m/%d/%Y")
#       to_date = end_ts.strftime("%m/%d/%Y")
#       key = request.GET.get('key', None)
#
#     loc = dailydb.locations.find_one({'key':key})
#     locname = loc['name']
#   except:
#     return dashboard(request)
#
#   totals_json = json.dumps(get_daily_kw_totals(key, start_ts, end_ts))
#   ctx = {
#     'key':key, 'locname':locname, 'from_date':from_date, 'to_date':to_date,
#     'daily_kw_totals':totals_json
#   }
#   return render(request, 'internal_reports.html', ctx)
#
#
#
#
#
# @login_required
# def dashboard(request):
#     try:
#
#         if (request.user.profile):
#             p = request.user.profile
#             p.last_portal_login = datetime.datetime.now(tz=timezone.utc)
#             p.save()
#             if p.email is None or p.phone is None or p.first_name is None or p.last_name is None:
#
#
#                 return HttpResponseRedirect("/get_email/")
#
#                 # return get_email(request)
#
#             ruser = get_remote_username_for_profile(p)
#
#             locs = get_locations_for_profile(p)
#             if locs is None:
#               return HttpResponse('user profile has no locations assigned', status=401)
#
#             # MIGHT NOT NEED THIS. THIS WAS FROM AN ERROR WHERE A CLIENT DIDNT HAVE A SAVED LOGO ON THE SERVER
#             if len(locs) > 1:
#               locs = locs.order_by('client__name', 'name')
#             ctx = {'is_admin':p.is_admin,
#                                            'client':p.client,
#                                            'locs':locs,
#                                            'ruser':ruser,
#                                            'user':request.user,
#                                            'staff':request.user.is_staff}
#
#             return render(request, 'dashboard.html', ctx)
#         else :
#             return HttpResponse('user does not have profile attached', status=401)
#     except:
#         var = traceback.format_exc()
#
#         print('api_report -  error : ', var)
#
#         return HttpResponse('user does not have profile attached', status=401)
#
#
#
#
#
# def test_multi_kw(request):
#   out = []
#   keys = [
#     "793b5fd45c3478b86404e0da413f3592e8e0dec5",
#     "e35fdd89d8f169dd933d760b21543b476d1582a8",
#     "b8a38c7ac3378f199b905fb0e75bbe2481bffc67",
#     "eae49b23105edb3d47beb1bb7e76f647e7c60c29",
#     "78989faf6a05073e35f51a17a9fd3e6a6ef8f6c0",
#     "25e3cc5627f01866d5ecfcc9d35e30f45ef4f0cb",
#     "871c10e06ca5ea3dcd27860be6a208f806fee04b",
#     "5971aa61c6108b15e0ed643bf150c9a357ffa77c",
#     "cd7dc0980498b10fee9351490f4e0fb2203fc5d4"
#   ]
#
#   start_ts = datetime.datetime.strptime("01/01/2010", "%m/%d/%Y")
#   end_ts = datetime.datetime.strptime("01/01/2014", "%m/%d/%Y")
#
#   for k in keys:
#     rep = get_kw_report(k, 'demand analyzer', start_ts, end_ts)
#     out.append({'key':k, 'report':rep})
#
#   return HttpResponse(json.dumps(out), content_type='application/json')
#
#
# @login_required
# def dashboard2(request):
#     try:
#
#         if (request.user.profile):
#             p = request.user.profile
#
#             clients = get_clients_for_profile(p)
#
#             ctx = {'is_admin':p.is_admin,
#                                            'client':clients,
#                                            'locs':locs,
#                                            'ruser':ruser,
#                                            'user':request.user}
#
#             return render(request, 'client_list.html', ctx)
#         else :
#             return HttpResponse('user does not have profile attached', status=401)
#     except:
#         return HttpResponse('user does not have profile attached', status=401)
#
#
# @login_required
# def client_dashboard(request, client_slug):
#     try:
#
#         if (request.user.profile):
#              p = request.user.profile
#              client = Client.objects.get(slug=client_slug)
#              locs = get_locations_for_client(p, client)
#              ruser = get_remote_username_for_profile(p)
#
#              ctx = {'is_admin':p.is_admin,
#              			   'client':client,
#              			   'locs':locs,
#              			   'ruser':ruser}
#              return render(request,'dashboard.html', ctx)
#         else :
#             return HttpResponse('user does not have profile attached', status=401)
#     except:
#         return HttpResponse('user does not have profile attached', status=401)
#
#
#
#
#
# ######################
# # REPORT ENDPOINT
#
# ## LOGIN - REQUIRED, although you shouldn't even be able to hit this unless logged in so.
# ## Also, how many of these functions are also just endpoints that are exposed to urls?
# @login_required
# def report(request):
#   ## don't know why it would be either a post or a get?
#   if request.method == 'POST':
#     key = request.POST.get('key')
#   else:
#     key = request.GET.get('key')
#
#   # get record from django and check report type
#   loc = Location.objects.get(key=key)
#
#   if loc.report_type == 'standard':
#     return standard_report(request)
#   else:
#     ## NO NO NO NO NO!
#     return index(request)
#
#
# def standard_report(request):
#   try:
#
#     if request.method == 'POST':
#       key = request.POST.get('key')
#       from_date = request.POST.get('from_date', None)
#       to_date = request.POST.get('to_date', None)
#       start_ts = datetime.datetime.strptime(from_date, "%m/%d/%Y")
#       end_ts = datetime.datetime.strptime(to_date, "%m/%d/%Y")
#     else:
#       # default to current month
#
#       d = datetime.datetime.now()
#       rng = calendar.monthrange(d.year, d.month)
#       start_ts = datetime.datetime(d.year, d.month, 1)
#       end_ts = datetime.datetime(d.year, d.month, rng[1])
#       from_date = start_ts.strftime("%m/%d/%Y")
#       to_date = end_ts.strftime("%m/%d/%Y")
#       key = request.GET.get('key', None)
#
#     loc = dailydb.locations.find_one({'key':key})
#     locname = loc['name']
#   except:
#     return index(request)
#
#   adminDb = pymongoclient['admin']
#   adminDb.authenticate("root","beetroot");
#
#   hvacs = []
#   lights = []
#   kwmeters = []
#   kwrep = None
#   historical_kw = get_historical_usage_map(key)
#   print(start_ts)
#   alarms = list(dailydb.alarms.find({'key':key, 'ts':{'$gte':start_ts, '$lte':end_ts}}))
#   hvac_alarms = []
#
#   ids = dailydb.daily_logs.find({'key':key}).distinct('controller_id')
#   for i in ids:
#     c = dailydb.daily_logs.find({'key':key, 'controller_id':i}).sort('ts', -1).limit(1)[0]
#     if c['type'] == 'hvac':
#
#       id = c['controller_id']
#       rep = get_hvac_report(key, id, start_ts, end_ts)
#       if rep:
#         rep['controller_id'] = id
#         rep['name'] = c['name']
#         rep['alarms'] = []
#         for a in alarms:
#           if a['source_id'] == id:
#             rep['alarms'].append(a)
#             hvac_alarms.append(a)
#         hvacs.append(rep)
#     elif c['type'] == 'light':
#       id = c['controller_id']
#       rep = get_light_report(key, id, start_ts, end_ts)
#       if rep:
#         rep['controller_id'] = id
#         rep['name'] = c['name']
#         lights.append(rep)
#     elif c['type'] == 'kw_meter':
#       id = c['controller_id']
#       rep = get_kw_report(key, id, start_ts, end_ts)
#       if rep:
#         rep['controller_id'] = id
#         rep['name'] = c['name']
#         kwmeters.append(rep)
#     elif c['type'] == 'demand analyzer':
#       id = c['controller_id']
#       rep = get_kw_report(key, id, start_ts, end_ts)
#       if rep:
#         rep['controller_id'] = id
#         rep['name'] = 'Energy Usage'
#         kwrep = rep
#
#   # sort the controller lists
#   sortkey = lambda s: s['name'].lower()
#
#   free_alarms = [x for x in alarms if not x in hvac_alarms]
#
#   hvacs = sorted(hvacs, key=sortkey)
#   lights = sorted(lights, key=sortkey)
#   kwmeters = sorted(kwmeters, key=sortkey)
#
#   # don't show individual kwmeters unless there's more than 1
#   if len(kwmeters) <= 1: kwmeters = []
#   ctx = {
#     'key':key, 'locname':locname, 'historical_kw':historical_kw,
#     'hvacs':hvacs, 'lights':lights, 'kwmeters':kwmeters, 'kw':kwrep,
#     'from_date':from_date, 'to_date':to_date, 'alarms':free_alarms
#   }
#
#   return render(request, 'report.html', ctx)
#
#
#
# def ng_google(request):
#
#     try:
#         stuff = json.loads(request.body.decode('utf-8'))
#         loc = Location.objects.get(secret_key=stuff['loc']['secret_key'])
#         newstring = loc.name.replace(' ', '%20')
#         url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=' + newstring + '&inputtype=textquery&fields=place_id,photos,formatted_address,name,rating,opening_hours,geometry&key=AIzaSyALymVceM72Yb1CTpG7rSlXVer2aodnwHg'
#         serialized_data = json.loads(requests.get(url).text)
#         secondurl = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + serialized_data['candidates'][0]['place_id'] + '&fields=name,rating,formatted_phone_number&key=AIzaSyALymVceM72Yb1CTpG7rSlXVer2aodnwHg'
#         hello = json.loads(requests.get(secondurl).text)
#
#         jsonreturn = {'result': hello['result']['formatted_phone_number'] }
#
#         return JsonResponse(jsonreturn)
#
#
#     except:
#         var = traceback.format_exc()
#
#         print('api_report -  error : ', var)
#
#         return HttpResponse(status=500)
#
#
# def ng_addthing(request):
#
#     try:
#         stuff = json.loads(request.body.decode('utf-8'))
#         loc = Location.objects.get(secret_key=stuff['location'])
#         locdb = pymongoclient[loc.key]
#         locdb.things.insert(stuff['model'])
#         # print(stuff)
#         # db = client['']
#
#         # model = request.POST.get('key')
#         # from_date = request.POST.get('from_date', None)
#         # to_date = request.POST.get('to_date',
#         #
#         jsonreturn = {
#
#             "settings": {},
#             'controllers': {},
#             "devices": {},
#             "time": {},
#             "schedules": {}
#
#
#         }
#
#
#         return JsonResponse(jsonreturn)
#
#
#     except:
#         var = traceback.format_exc()
#
#         print('api_report -  error : ', var)
#
#         return HttpResponse(status=500)
#
#
# def ng_location_data(request):
#
#     try:
#
#         secret = request.GET.get('secret')
#
#         loc = Location.objects.get(secret_key=secret)
#
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         socket.timeout(5.0)
#
#         port = 8000
#         s.connect(('proxy.kiteandlightning.com', port))
#
#
#         proxy_ident = {
#
#                     'method':'proxy.ident',
#                     'params': ['client']
#         }
#         s.sendall((json.dumps(proxy_ident)+"\r\n").encode('utf-8'))
#
#
#
#         proxy_setdefaultserver = {
#                   'method':'proxy.setdefaultserver',
#                   'params': [loc.key, loc.secret_key]
#         }
#         s.sendall((json.dumps(proxy_setdefaultserver)+"\r\n").encode('utf-8'))
#
#
#         kl_get_settings = {
#                   'method':'kl.get_settings',
#                   'params': [["energy.demand","energy.kw_sp","energy.kw_total","energy.demand_mode"]],
#                   'id':124
#         }
#         kl_get_controllers = {
#
#                     'method':'kl.get_controllers',
#                     'params': [["sockets","name","type","subtype","enabled","status","map_entries"],[["type",1],["subtype",1],["name",1]]],
#                     'id':125
#         }
#         kl_get_devices = {
#
#                     'method':'kl.get_devices',
#                     'id':126
#         }
#         kl_get_server_time = {
#
#                     'method':'kl.get_server_time',
#                     'id':127
#         }
#         kl_get_schedules = {
#
#                     'method':'kl.get_schedules',
#                     'id':128
#         }
#
#
#         s.sendall((
#             json.dumps(kl_get_settings) + "\r\n" +
#             json.dumps(kl_get_controllers) + "\r\n" +
#             json.dumps(kl_get_devices) + "\r\n" +
#             json.dumps(kl_get_server_time) + "\r\n" +
#             json.dumps(kl_get_schedules) + "\r\n" ).encode('utf-8'))
#
#
#         mycount = 5
#         data = ''
#         msgs = 0
#         while True:
#           newdata = s.recv(2048).decode('utf-8')
#           if not newdata:
#               break
#           msgs = msgs + newdata.count("\n")
#           if msgs == mycount:
#               data = data + newdata
#               break
#           else:
#               data = data + newdata
#
#         if len(data) == 0:
#             loc.is_online = False
#             jsonoffline = {
#
#                 "offline": 'offline'
#             }
#             return JsonResponse(jsonoffline)
#
#         sepdata = data.split("\r\n")[:-1]
#
#         jsondata = []
#         jsonreturn = {
#
#             # "settings": {
#             #     "demand": 'null',
#             #     'kw_total': 'null',
#             #     'kw_sp': 'null',
#             #     'demand_mode': 'null'
#             # },
#             "settings": {},
#             'controllers': {},
#             "devices": {},
#             "time": {},
#             "schedules": {},
#             "daily_logs_stuff": {}
#
#         }
#         devices = []
#         controllers = []
#         for thing in sepdata:
#
#
#             blah = json.loads(thing)
#
#             if blah['id'] == 124:
#                 if blah['result'] == None:
#                     jsonreturn['settings']['error'] = blah['error']
#                 else:
#
#                     jsonreturn['settings']['result'] = blah['result']
#                 # jsonreturn['settings']['kw_total'] = blah['result']["energy.kw_total"]
#                 # jsonreturn['settings']['kw_sp'] = blah['result']["energy.kw_sp"]
#                 # jsonreturn['settings']['demand_mode'] = blah['result']["energy.demand_mode"]
#
#
#             elif blah['id'] == 125:
#                 # if (loc.secret_key == 'd42e9bc62780f1373334'):
#                 #     print(blah[result])
#                 if blah['result'] == None:
#
#                     jsonreturn['controllers']['error'] = blah['error']
#                 else:
#
#                     jsonreturn['controllers']['result'] = blah['result']
#
#                     for thing in blah['result']:
#                         controllers.append(thing)
#
#             elif blah['id'] == 126:
#                 if blah['result'] == None:
#
#                     jsonreturn['devices']['error'] = blah['error']
#                 else:
#
#                     jsonreturn['devices']['result'] = blah['result']
#
#                     for thing in blah['result']:
#                         # deviceid = thing['device_id']
#                         devices.append(thing)
#
#             elif blah['id'] == 127:
#                 if blah['result'] == None:
#
#                     jsonreturn['time']['error'] = blah['error']
#                 else:
#
#                     jsonreturn['time']['result'] = blah['result']
#
#             elif blah['id'] == 128:
#                 # print(blah)
#                 if blah['result'] == None:
#
#                     jsonreturn['schedules']['error'] = blah['error']
#                 else:
#
#                     jsonreturn['schedules']['result'] = blah['result']
#
#
#                     # for thing in blah['result']:
#                     #     deviceid = thing['device_id']
#                     #     devices.append(deviceid)
#
#         # print(devices)
#         # print(loc)
#
#         for c in controllers:
#             c["hardware_devices"] = []
#
#         for d in devices:
#
#             items = []
#             kl_get_settings = {
#                       'method':'kl.get_items_by_device_id',
#                       'params': [d["device_id"]],
#                       'id':129
#             }
#
#             s.sendall((
#                 json.dumps(kl_get_settings) + "\r\n").encode('utf-8'))
#
#
#             mycount = 1
#             data = ''
#             msgs = 0
#             while True:
#               newdata = s.recv(2048).decode('utf-8')
#               if not newdata:
#                   break
#               msgs = msgs + newdata.count("\n")
#               if msgs == mycount:
#                   data = data + newdata
#                   break
#               else:
#                   data = data + newdata
#
#             if len(data) == 0:
#                 loc.is_online = False
#                 jsonoffline = {
#
#                     "offline": 'offline'
#                 }
#                 return JsonResponse(jsonoffline)
#
#             sepdata = data.split("\r\n")[:-1]
#
#             for thing in sepdata:
#
#
#                 blah = json.loads(thing)
#
#                 if blah['id'] == 129:
#                     if blah['result'] == None:
#                         d["items"] = blah['error']
#                     else:
#                         for item in blah['result']:
#                             if "usage" in item:
#                                 for usage in item["usage"]:
#                                     cid = usage["controller_id"]
#                                     for c in controllers:
#                                         if c["_id"]["$oid"] == cid:
#                                             # if c["name"] == "grow room 1":
#
#                                                 # print(c)
#                                             if "hardware_devices" in c:
#
#                                                 if c["hardware_devices"] != None:
#                                                     found = False
#                                                     for h in c["hardware_devices"]:
#                                                         if h == d["device_id"]:
#                                                             found = True
#                                                     if not found:
#
#
#                                                         c["hardware_devices"].append(d["device_id"])
#                                                 else:
#
#                                                     c["hardware_devices"] = [d["device_id"]]
#
#                                             else:
#
#                                                 c["hardware_devices"] = [d["device_id"]]
#
#
#                         # d["items"] = blah['result']
#         jsonreturn['devices']['result'] = devices
#         jsonreturn['controllers']['result'] = controllers
#
#         # import csv
#         #
#         #
#         # controllerdata = open('/data/hardware.csv', 'a')
#         #
#         # # create the csv writer object
#         #
#         # csvwriter = csv.writer(controllerdata)
#         #
#         #
#         #
#         #
#         # for d in devices:
#         #     newd = {}
#         #     if "name" in d:
#         #         newd["name"] = d['name']
#         #     else:
#         #         newd["name"] = 'N/A'
#         #     if "connection" in d:
#         #         newd["connection"] = d['connection']
#         #     else:
#         #         newd["connection"] = 'N/A'
#         #     if "device_id" in d:
#         #         newd["device_id"] = d['device_id']
#         #     else:
#         #         newd["device_id"] = 'N/A'
#         #     if "device_model" in d:
#         #         newd["device_model"] = d['device_model']
#         #     else:
#         #         newd["device_model"] = 'N/A'
#         #     newd["loc_key"] = loc.key
#         #
#         #
#         #
#         #
#         #     csvwriter.writerow(newd.values())
#         #
#         # controllerdata.close()
#
#
#
#         #
#         # controllerdata = open('/data/controllers.csv', 'a')
#         #
#         # # create the csv writer object
#         #
#         # csvwriter = csv.writer(controllerdata)
#         #
#         #
#         # for c in controllers:
#         #
#         #
#         #     for d in c["hardware_devices"]:
#         #         newc = {}
#         #         newc["name"] = c['name']
#         #         newc["type"] = c['type']
#         #         newc["subtype"] = c['subtype']
#         #         newc["id"] = c['_id']['$oid']
#         #         newc["device_id"] = d
#         #         newc["loc_key"] = loc.key
#         #
#         #
#         #
#         #
#         #         csvwriter.writerow(newc.values())
#         #
#         # controllerdata.close()
#
#
#
#         d = datetime.datetime.now()
#         rng = calendar.monthrange(d.year, d.month)
#         start_ts = datetime.datetime(d.year, d.month, 1)
#         end_ts = datetime.datetime(d.year, d.month, rng[1])
#         from_date = start_ts.strftime("%m/%d/%Y")
#         to_date = end_ts.strftime("%m/%d/%Y")
#         key = loc.key
#
#         dailyloc = dailydb.locations.find_one({'key':key})
#         if (dailyloc):
#
#             locname = dailyloc['name']
#
#             hvacs = []
#             lights = []
#             kwmeters = []
#             kwrep = None
#             historical_kw = get_historical_usage_map(key)
#
#             alarms = list(dailydb.alarms.find({'key':key, 'ts':{'$gte':start_ts, '$lte':end_ts}}))
#             hvac_alarms = []
#
#             ids = dailydb.daily_logs.find({'key':key}).distinct('controller_id')
#             for i in ids:
#               c = dailydb.daily_logs.find({'key':key, 'controller_id':i}).sort('ts', -1).limit(1)[0]
#               if c['type'] == 'hvac':
#
#                 id = c['controller_id']
#                 rep = get_hvac_report(key, id, start_ts, end_ts)
#                 if rep:
#                   rep['controller_id'] = id
#                   rep['name'] = c['name']
#                   rep['alarms'] = []
#                   for a in alarms:
#                     if a['source_id'] == id:
#                       rep['alarms'].append(a)
#                       hvac_alarms.append(a)
#                   hvacs.append(rep)
#               elif c['type'] == 'light':
#                 id = c['controller_id']
#                 rep = get_light_report(key, id, start_ts, end_ts)
#                 if rep:
#                   rep['controller_id'] = id
#                   rep['name'] = c['name']
#                   lights.append(rep)
#               elif c['type'] == 'kw_meter':
#                 id = c['controller_id']
#                 rep = get_kw_report(key, id, start_ts, end_ts)
#                 if rep:
#                   rep['controller_id'] = id
#                   rep['name'] = c['name']
#                   kwmeters.append(rep)
#               elif c['type'] == 'demand analyzer':
#                 id = c['controller_id']
#                 rep = get_kw_report(key, id, start_ts, end_ts)
#                 if rep:
#                   rep['controller_id'] = id
#                   rep['name'] = 'Energy Usage'
#                   kwrep = rep
#
#             # sort the controller lists
#             sortkey = lambda s: s['name'].lower()
#
#             free_alarms = [x for x in alarms if not x in hvac_alarms]
#
#             hvacs = sorted(hvacs, key=sortkey)
#             lights = sorted(lights, key=sortkey)
#             kwmeters = sorted(kwmeters, key=sortkey)
#
#             # don't show individual kwmeters unless there's more than 1
#             if len(kwmeters) <= 1: kwmeters = []
#             ctx = {
#               'key':key, 'locname':locname, 'historical_kw':historical_kw,
#               'hvacs':hvacs, 'lights':lights, 'kwmeters':kwmeters, 'kw':kwrep,
#               'from_date':from_date, 'to_date':to_date, 'alarms':free_alarms
#             }
#
#             newctx = json_util.dumps(ctx)
#             newctx = json.loads(newctx)
#             # ctx['alarms'] = json.dumps(ctx['alarms'])
#             # ctx['historical_kw'] = json.loads(ctx['historical_kw'])
#             # ctx['lights'] = json.loads(ctx['lights'])
#             # ctx['kwmeters'] = json.loads(ctx['kwmeters'])
#             # ctx['kw'] = json.loads(ctx['kw'])
#             # ctx['from_date'] = json.loads(ctx['from_date'])
#             # ctx['to_date'] = json.loads(ctx['to_date'])
#
#
#             # newctx = json.loads(ctx)
#
#             jsonreturn['daily_logs_stuff'] = newctx
#         else:
#             jsonreturn['daily_logs_stuff'] = False
#
#
#         return JsonResponse(jsonreturn)
#
#
#     except:
#         var = traceback.format_exc()
#
#         print('api_report -  error : ', var)
#         return HttpResponse(status=500)
#
#
# def ng_status_history(request):
#
#     try:
#         print('hello?')
#         stuff = json.loads(request.body.decode('utf-8'))
#         loc = Location.objects.get(secret_key=stuff['loc']['secret_key'])
#         # print(loc)
#
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         socket.timeout(5.0)
#
#         port = 8000
#         s.connect(('proxy.kiteandlightning.com', port))
#
#
#         proxy_ident = {
#
#                     'method':'proxy.ident',
#                     'params': ['client']
#         }
#         s.sendall((json.dumps(proxy_ident)+"\r\n").encode('utf-8'))
#
#
#
#         proxy_setdefaultserver = {
#                   'method':'proxy.setdefaultserver',
#                   'params': [loc.key, loc.secret_key]
#         }
#         s.sendall((json.dumps(proxy_setdefaultserver)+"\r\n").encode('utf-8'))
#
#
#         kl_get_controller_status = {
#                   'method':'kl.get_controller_status',
#                   'params': [ stuff['con']['_id']['$oid'], stuff['fromtime'], stuff['totime'], ["state","2c3s","sockets","ts"]],
#                   'id':124
#         }
#
#
#
#         s.sendall((
#             json.dumps(kl_get_controller_status) + "\r\n").encode('utf-8'))
#
#
#         mycount = 1
#         data = ''
#         msgs = 0
#         while True:
#           newdata = s.recv(2048).decode('utf-8')
#           if not newdata:
#               break
#           msgs = msgs + newdata.count("\n")
#           if msgs == mycount:
#               data = data + newdata
#               break
#           else:
#               data = data + newdata
#
#         if len(data) == 0:
#             loc.is_online = False
#             jsonoffline = {
#
#                 "offline": 'offline'
#             }
#             return JsonResponse(jsonoffline)
#
#         sepdata = data.split("\r\n")[:-1]
#         # print(sepdata)
#         jsondata = []
#         jsonreturn = {
#
#
#             "status": {}
#
#
#         }
#
#         for thing in sepdata:
#
#
#             blah = json.loads(thing)
#
#             if blah['result'] == None:
#                 jsonreturn['status']['error'] = blah['error']
#             else:
#
#                 jsonreturn['status']['result'] = blah['result']
#
#
#
#         return JsonResponse(jsonreturn)
#
#
#     except:
#         var = traceback.format_exc()
#
#         print('api_report -  error : ', var)
#         return HttpResponse(status=500)
#
# def ng_status_history1(request):
#
#     try:
#         stuff = json.loads(request.body.decode('utf-8'))
#         loc = Location.objects.get(secret_key=stuff['loc']['secret_key'])
#         # print(loc)
#
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         socket.timeout(5.0)
#
#         port = 8000
#         s.connect(('proxy.kiteandlightning.com', port))
#
#
#         proxy_ident = {
#
#                     'method':'proxy.ident',
#                     'params': ['client']
#         }
#         s.sendall((json.dumps(proxy_ident)+"\r\n").encode('utf-8'))
#
#
#
#         proxy_setdefaultserver = {
#                   'method':'proxy.setdefaultserver',
#                   'params': [loc.key, loc.secret_key]
#         }
#         s.sendall((json.dumps(proxy_setdefaultserver)+"\r\n").encode('utf-8'))
#
#
#         kl_get_controller_status = {
#                   'method':'kl.get_controller_status',
#                   'params': [ stuff['con']['_id']['$oid'], stuff['fromtime'], stuff['totime'], ["state","2c3s","sockets","ts"]],
#                   'id':124
#         }
#         kl_get_controller_schedules = {
#                   'method':'kl.get_controller_schedule',
#                   'params': [ stuff['con']['_id']['$oid']],
#                   'id':125
#         }
#         kl_get_controller_modes = {
#                   'method':'kl.get_controller_modes',
#                   'params': [ stuff['con']['_id']['$oid']],
#                   'id':126
#         }
#         kl_get_controller_setting1 = {
#                   'method':"kl.get_controller_setting",
#                   'params': [ stuff['con']['_id']['$oid'], "hvac.override_min"],
#                   'id':127
#         }
#         kl_get_controller_setting2 = {
#                   'method':"kl.get_controller_setting",
#                   'params': [ stuff['con']['_id']['$oid'], "hvac.sp_adjustment_increment"],
#                   'id':128
#         }
#         kl_get_controller_setting3 = {
#                   'method':"kl.get_controller_setting",
#                   'params': [ stuff['con']['_id']['$oid'], "hvac.sp_max_adjustment"],
#                   'id':129
#         }
#
#         s.sendall((
#             json.dumps(kl_get_controller_status) + "\r\n" +
#             json.dumps(kl_get_controller_schedules) + "\r\n" +
#             json.dumps(kl_get_controller_modes) + "\r\n" +
#             json.dumps(kl_get_controller_setting1) + "\r\n" +
#             json.dumps(kl_get_controller_setting2) + "\r\n" +
#             json.dumps(kl_get_controller_setting3) + "\r\n").encode('utf-8'))
#
#
#         mycount = 6
#         data = ''
#         msgs = 0
#         while True:
#           newdata = s.recv(2048).decode('utf-8')
#           if not newdata:
#               break
#           msgs = msgs + newdata.count("\n")
#           if msgs == mycount:
#               data = data + newdata
#               break
#           else:
#               data = data + newdata
#
#         if len(data) == 0:
#             loc.is_online = False
#             jsonoffline = {
#
#                 "offline": 'offline'
#             }
#             return JsonResponse(jsonoffline)
#
#         sepdata = data.split("\r\n")[:-1]
#         # print(sepdata)
#         jsondata = []
#         jsonreturn = {
#
#
#             "history": {},
#             "schedules":{},
#             "modes":{},
#             "settings":{}
#
#
#         }
#
#         for thing in sepdata:
#
#
#             blah = json.loads(thing)
#
#             if blah['id'] == 124:
#                 if blah['result'] == None:
#                     jsonreturn['history']['error'] = blah['error']
#                 else:
#
#                     jsonreturn['history']['result'] = blah['result']
#
#
#             elif blah['id'] == 125:
#
#                 if blah['result'] == None:
#
#                     jsonreturn['schedules']['error'] = blah['error']
#                 else:
#
#                     jsonreturn['schedules']['result'] = blah['result']
#
#
#
#             elif blah['id'] == 126:
#                 if blah['result'] == None:
#
#                     jsonreturn['modes']['error'] = blah['error']
#                 else:
#
#                     jsonreturn['modes']['result'] = blah['result']
#
#             elif blah['id'] == 127:
#                 if blah['result'] == None:
#
#                     jsonreturn['settings']['error'] = blah['error']
#                 else:
#
#                     jsonreturn['settings']['override_min'] = blah['result']
#
#             elif blah['id'] == 128:
#                 if blah['result'] == None:
#
#                     jsonreturn['settings']['error'] = blah['error']
#                 else:
#
#                     jsonreturn['settings']['sp_adjustment_increment'] = blah['result']
#             elif blah['id'] == 129:
#                 if blah['result'] == None:
#
#                     jsonreturn['settings']['error'] = blah['error']
#                 else:
#
#                     jsonreturn['settings']['sp_max_adjustment'] = blah['result']
#
#
#
#
#         return JsonResponse(jsonreturn)
#
#
#     except:
#         var = traceback.format_exc()
#
#         print('api_report -  error : ', var)
#         return HttpResponse(status=500)
#
# def ng_hvac_override(request):
#
#     try:
#         stuff = json.loads(request.body.decode('utf-8'))
#         loc = Location.objects.get(secret_key=stuff['loc']['secret_key'])
#
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         socket.timeout(5.0)
#
#         port = 8000
#         s.connect(('proxy.kiteandlightning.com', port))
#
#
#         proxy_ident = {
#
#                     'method':'proxy.ident',
#                     'params': ['client']
#         }
#         s.sendall((json.dumps(proxy_ident)+"\r\n").encode('utf-8'))
#
#
#
#         proxy_setdefaultserver = {
#                   'method':'proxy.setdefaultserver',
#                   'params': [loc.key, loc.secret_key]
#         }
#         s.sendall((json.dumps(proxy_setdefaultserver)+"\r\n").encode('utf-8'))
#
#
#         kl_controller_override = {}
#
#         if (stuff['init']):
#             kl_controller_override['params'] = [ stuff['con']['_id']['$oid'], {"dur_sec": 7200, "adj": stuff['adj']}]
#             kl_controller_override['method'] = "kl.set_controller_override"
#
#         else:
#             kl_controller_override['params'] = [ stuff['con']['_id']['$oid']]
#
#             kl_controller_override['method'] = "kl.clear_controller_override"
#
#
#         s.sendall((
#
#             json.dumps(kl_controller_override) + "\r\n" ).encode('utf-8'))
#
#         jsonreturn = {"result": "success"}
#
#
#         return JsonResponse(jsonreturn)
#
#
#     except:
#         var = traceback.format_exc()
#
#         print('api_report -  error : ', var)
#         return HttpResponse(status=500)
#
#
# def ng_hvac_setting(request):
#
#     try:
#         stuff = json.loads(request.body.decode('utf-8'))
#         loc = Location.objects.get(secret_key=stuff['loc']['secret_key'])
#
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         socket.timeout(5.0)
#
#         port = 8000
#         s.connect(('proxy.kiteandlightning.com', port))
#
#
#         proxy_ident = {
#
#                     'method':'proxy.ident',
#                     'params': ['client']
#         }
#         s.sendall((json.dumps(proxy_ident)+"\r\n").encode('utf-8'))
#
#
#
#         proxy_setdefaultserver = {
#                   'method':'proxy.setdefaultserver',
#                   'params': [loc.key, loc.secret_key]
#         }
#         s.sendall((json.dumps(proxy_setdefaultserver)+"\r\n").encode('utf-8'))
#
#
#         h_sp = {}
#         c_sp = {}
#         fan = {}
#         fc_only = {}
#         setback = {}
#
#         h_sp['params'] = [ stuff['con']['_id']['$oid'], stuff['changes']['mode'], "h_sp", stuff['changes']['h_sp']]
#         h_sp['method'] = "kl.set_controller_mode_property"
#
#         c_sp['params'] = [ stuff['con']['_id']['$oid'], stuff['changes']['mode'], "c_sp", stuff['changes']['c_sp']]
#         c_sp['method'] = "kl.set_controller_mode_property"
#
#         fan['params'] = [ stuff['con']['_id']['$oid'], stuff['changes']['mode'], "fan", stuff['changes']['fan']]
#         fan['method'] = "kl.set_controller_mode_property"
#
#         fc_only['params'] = [ stuff['con']['_id']['$oid'], stuff['changes']['mode'], "fc_only", stuff['changes']['fc_only']]
#         fc_only['method'] = "kl.set_controller_mode_property"
#
#         setback['params'] = [ stuff['con']['_id']['$oid'], stuff['changes']['mode'], "setback", stuff['changes']['setback']]
#         setback['method'] = "kl.set_controller_mode_property"
#
#
#
#         s.sendall((
#             json.dumps(h_sp) + "\r\n" +
#             json.dumps(c_sp) + "\r\n" +
#             json.dumps(fan) + "\r\n" +
#             json.dumps(fc_only) + "\r\n" +
#             json.dumps(setback) + "\r\n").encode('utf-8'))
#
#         jsonreturn = {"result": "success"}
#
#
#         return JsonResponse(jsonreturn)
#
#
#     except:
#         var = traceback.format_exc()
#
#         print('api_report -  error : ', var)
#         return HttpResponse(status=500)
#
# def ng_light_override(request):
#
#     try:
#         stuff = json.loads(request.body.decode('utf-8'))
#         loc = Location.objects.get(secret_key=stuff['loc']['secret_key'])
#
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         socket.timeout(5.0)
#
#         port = 8000
#         s.connect(('proxy.kiteandlightning.com', port))
#
#
#         proxy_ident = {
#
#                     'method':'proxy.ident',
#                     'params': ['client']
#         }
#         s.sendall((json.dumps(proxy_ident)+"\r\n").encode('utf-8'))
#
#
#
#         proxy_setdefaultserver = {
#                   'method':'proxy.setdefaultserver',
#                   'params': [loc.key, loc.secret_key]
#         }
#         s.sendall((json.dumps(proxy_setdefaultserver)+"\r\n").encode('utf-8'))
#
#
#         kl_controller_override = {}
#
#         if (stuff['init']):
#             kl_controller_override['params'] = [ stuff['con']['_id']['$oid'], {"dur_sec": 3600, "level": stuff['adj']}]
#             kl_controller_override['method'] = "kl.set_controller_override"
#
#         else:
#             kl_controller_override['params'] = [ stuff['con']['_id']['$oid']]
#
#             kl_controller_override['method'] = "kl.clear_controller_override"
#
#
#         s.sendall((
#
#             json.dumps(kl_controller_override) + "\r\n" ).encode('utf-8'))
#
#         jsonreturn = {"result": "success"}
#
#
#         return JsonResponse(jsonreturn)
#
#
#     except:
#         var = traceback.format_exc()
#
#         print('api_report -  error : ', var)
#         return HttpResponse(status=500)
#
#
# def ng_zone_data(request):
#     try:
#
#         stuff = json.loads(request.body.decode('utf-8'))
#         controllerkeys = stuff['controllerkeys']
#
#         incomingLoc = stuff['location']
#
#         loc = Location.objects.get(secret_key=incomingLoc['secret_key'])
#         if loc.name == "A Royal Flush":
#             print(controllerkeys)
#
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         socket.timeout(5.0)
#
#         port = 8000
#         s.connect(('proxy.kiteandlightning.com', port))
#
#
#         proxy_ident = {
#
#                     'method':'proxy.ident',
#                     'params': ['client']
#         }
#         s.sendall((json.dumps(proxy_ident)+"\r\n").encode('utf-8'))
#
#
#
#         proxy_setdefaultserver = {
#                   'method':'proxy.setdefaultserver',
#                   'params': [loc.key, loc.secret_key]
#         }
#         s.sendall((json.dumps(proxy_setdefaultserver)+"\r\n").encode('utf-8'))
#
#
#         controllerString = ''
#         offset = 1000
#
#         for i in range(len(controllerkeys)):
#             get_modes = {
#                       'method':'kl.get_controller_modes',
#                       'params': [controllerkeys[i]],
#                       'id': i
#             }
#             get_schedules = {
#                       'method':'kl.get_controller_schedule',
#                       'params': [controllerkeys[i]],
#                       'id': i+offset
#             }
#             controllerString = controllerString + json.dumps(get_modes)+"\r\n"+json.dumps(get_schedules)+"\r\n"
#
#
#         s.sendall(controllerString.encode('utf-8'))
#
#         data = ''
#         msgs = 0
#         mycount = len(controllerkeys)*2
#         while True:
#           newdata = s.recv(2048).decode('utf-8')
#           if not newdata:
#               break
#           msgs = msgs + newdata.count("\n")
#           if msgs == mycount:
#               data = data + newdata
#               break
#           else:
#               data = data + newdata
#
#         if len(data) == 0:
#             loc.is_online = False
#             jsonoffline = {
#
#                 "offline": 'offline'
#             }
#             return JsonResponse(jsonoffline)
#
#         sepdata = data.split("\r\n")[:-1]
#
#         jsonreturn = {
#
#             "return": []
#
#         }
#
#         for thing in sepdata:
#
#
#             blah = json.loads(thing)
#
#             for i in range(len(controllerkeys)):
#                 if (i == blah['id']) or (i+offset == blah['id']):
#                     blah['controller'] = controllerkeys[i]
#
#
#
#             jsonreturn['return'].append(blah)
#
#
#
#         return JsonResponse(jsonreturn)
#
#
#
#     except:
#         e = sys.exc_info()
#         edict = {
#             'error':str(e)
#         }
#         print('api_report -  error : ', e)
#         return HttpResponse(status=500)
#
#
#
#
# def ng_authenticate(request):
#
#
#  try:
#
#      #stuff = json.loads(request.body)
#      stuff = json.loads(request.body.decode('utf-8'))
#      username = stuff['username']
#      password = stuff['password']
#      user = authenticate(username=username, password=password)
#      if user is not None:
#
#          up = user.profile
#          up.last_mobile_login = datetime.datetime.now(tz=timezone.utc)
#          up.save()
#
#
#          obj = {
#             'type' : 'null',
#             'id': user.id,
#             'username': user.username,
#             'firstName': user.first_name,
#             'lastName': user.last_name,
#             'token': 'fake-jwt-token',
#             'dealers': 'null',
#             'is_authenticated': False,
#             'isAdmin': user.profile.is_admin,
#             'locations': 'null',
#             'role': user.profile.role,
#             'permission': user.profile.mobile
#          }
#          jsondealers = []
#          if user.profile.is_admin:
#            jsonlocs = []
#            locs = Location.objects.all()
#            # locnum = len(locs)
#            # batchsize = locnum / 3
#            # count = 0
#
#            for loc in locs:
#                # 'is_online': True,
#                # 'loc_data': 'null'
#                jsonloc = {
#                   'name' : loc.name,
#                   'online' : loc.is_online,
#                   'secret_key' : loc.secret_key,
#                   'has_unity' : True,
#                   'client': loc.client.name,
#                   'batchnum': 0
#
#                }
#
#                # print('yo')
#                # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                #
#                # port = 8000
#                # s.connect(('proxy.kiteandlightning.com', port))
#                #
#                #
#                # proxy_ident = {
#                #
#                #             'method':'proxy.ident',
#                #             'params': ['client']
#                # }
#                # s.sendall((json.dumps(proxy_ident)+"\r\n").encode('utf-8'))
#                #
#                #
#                #
#                # proxy_setdefaultserver = {
#                #           'method':'proxy.setdefaultserver',
#                #           'params': [loc.key, loc.secret_key]
#                # }
#                # s.sendall((json.dumps(proxy_setdefaultserver)+"\r\n").encode('utf-8'))
#                #
#                #
#                # kl_get_settings = {
#                #           'method':'kl.get_settings',
#                #           'params': [["energy.demand","energy.kw_sp","energy.kw_total","energy.demand_mode"]],
#                #           'id':124
#                # }
#                # ## also get socket field from controller in excess of flash app
#                # kl_get_controllers = {
#                #
#                #             'method':'kl.get_controllers',
#                #             'params': [["name","type","subtype","enabled","status","map_entries"],[["type",1],["subtype",1],["name",1]]],
#                #             'id':125
#                # }
#                # kl_get_devices = {
#                #
#                #             'method':'kl.get_devices',
#                #             'id':126
#                # }
#                #
#                # s.sendall((
#                #     json.dumps(kl_get_settings) + "\r\n" +
#                #     json.dumps(kl_get_controllers) + "\r\n" +
#                #     json.dumps(kl_get_devices) + "\r\n").encode('utf-8'))
#                #
#                # data = ''
#                # count = 0
#                # while True:
#                #   newdata = s.recv(2048).decode('utf-8')
#                #
#                #   if len(newdata) == 0:
#                #       break
#                #
#                #
#                #
#                #   index = newdata.find("\r\n")
#                #
#                #   if index != -1:
#                #
#                #       if count == 2:
#                #
#                #           data = data + newdata[:index]
#                #           break
#                #       else:
#                #           data = data + newdata
#                #           count = count+1
#                #
#                #
#                #   else:
#                #     data = data + newdata
#                #
#                # if len(data) == 0:
#                #     jsonloc['is_online'] = False
#                #     jsonlocs.append(jsonloc)
#                #
#                # else:
#                #
#                #     sepdata = data.split("\r\n")
#                #     locdata = {
#                #
#                #         "settings": {
#                #             "demand": 'null',
#                #             'kw_total': 'null',
#                #             'kw_sp': 'null',
#                #             'demand_mode': 'null'
#                #         },
#                #         "devices": 'null',
#                #         "hello": []
#                #
#                #
#                #     }
#                #     devices = []
#                #     controllers = []
#                #     for thing in sepdata:
#                #
#                #
#                #         blah = json.loads(thing)
#                #
#                #         if blah['id'] == 124:
#                #
#                #             locdata['settings']['demand'] = blah['result']["energy.demand"]
#                #             locdata['settings']['kw_total'] = blah['result']["energy.kw_total"]
#                #             locdata['settings']['kw_sp'] = blah['result']["energy.kw_sp"]
#                #             locdata['settings']['demand_mode'] = blah['result']["energy.demand_mode"]
#                #
#                #
#                #         elif blah['id'] == 125:
#                #             locdata['controllers'] = blah['result']
#                #
#                #             for thing in blah['result']:
#                #                 controllerid = thing['_id']['$oid']
#                #                 controllers.append(controllerid)
#                #         else:
#                #             for thing in blah['result']:
#                #                 deviceid = thing['device_id']
#                #                 devices.append(deviceid)
#                #
#                #             locdata['devices'] = blah['result']
#                # jsonloc['loc_data'] = locdata
#
#                jsonlocs.append(jsonloc)
#
#
#
#            obj['locations'] = jsonlocs
#
#
#
#          elif user.profile.dealer:
#              obj['type'] = 'dealer'
#              jsondealer = {
#                 'name' : user.profile.dealer.name,
#                 'clients' : 'null'
#
#              }
#              clients = Client.objects.filter(dealer=profile.dealer)
#              jsonclients = []
#              for client in clients:
#                  jsonclient = {
#                     'name' : client.name,
#                     'locations' : 'null'
#                  }
#                  locs = Location.objects.filter(client=client)
#                  jsonlocs = []
#                  for loc in locs:
#                      jsonloc = {
#                         'name' : loc.name,
#                         'online' : loc.is_online,
#                         'secret_key' : loc.secret_key,
#                         'has_unity' : True,
#                         'batchnum': 0
#                      }
#                      jsonlocs.append(jsonloc)
#                  jsonclient['locations'] = jsonlocs
#                  jsonclients.append(jsonclient)
#              jsondealer['clients'] = jsonclients
#              jsondealers.append(jsondealer)
#              obj['dealers'] = jsondealers
#
#          elif user.profile.client:
#
#
#              obj['type'] = 'client'
#
#              jsondealer = {
#                 'name' : 'null',
#                 'clients' : 'null'
#
#              }
#              if user.profile.client.dealer:
#                  jsondealer['name'] = user.profile.client.dealer.name
#              else:
#                  jsondealer['name'] = 'dealerless'
#
#              jsonclients = []
#              client = user.profile.client
#              jsonclient = {
#                 'name' : client.name,
#                 'locations' : 'null'
#              }
#              locs = Location.objects.filter(client=client)
#              jsonlocs = []
#              for loc in locs:
#                  jsonloc = {
#                     'name' : loc.name,
#                     'online' : loc.is_online,
#                     'secret_key' : loc.secret_key,
#                     'has_unity' : True,
#                     'batchnum': 0
#
#                  }
#                  jsonlocs.append(jsonloc)
#              jsonclient['locations'] = jsonlocs
#              jsonclients.append(jsonclient)
#              jsondealer['clients'] = jsonclients
#              jsondealers.append(jsondealer)
#              obj['dealers'] = jsondealers
#          else:
#              obj['type'] = 'ronin'
#              locs = user.profile.locations.all()
#              clients = Client.objects.filter(location__in=locs).distinct()
#              dealers = Dealer.objects.filter(client__in=clients).distinct()
#
#
#              dealerless = False
#              # Are there dealerless clients?
#              for iclient in clients:
#                  if not iclient.dealer:
#
#                      dealerless = True
#                      break
#              jsondealers = []
#
#              if dealerless:
#                  jsondealer = {
#                     'name' : 'dealerless',
#                     'clients' : 'null'
#                  }
#
#                  jsonclients = []
#
#                  for iclient in clients:
#                      if not iclient.dealer:
#
#                          jsonclient = {
#                             'name' : iclient.name,
#                             'locations' : 'null'
#                          }
#                          jsonlocs = []
#                          for loc in locs:
#                              if loc.client.name == iclient.name:
#                                  jsonloc = {
#                                     'name' : loc.name,
#                                     'online' : loc.is_online,
#                                     'secret_key' : loc.secret_key,
#                                     'has_unity' : True,
#                                     'batchnum': 0
#
#                                  }
#                                  jsonlocs.append(jsonloc)
#                          jsonclient['locations'] = jsonlocs
#                          jsonclients.append(jsonclient)
#                  jsondealer['clients'] = jsonclients
#                  jsondealers.append(jsondealer)
#              else:
#                  for idealer in dealers:
#                      jsondealer = {
#                         'name' : idealer.name,
#                         'clients' : 'null'
#                      }
#
#                      jsonclients = []
#
#                      for iclient in clients:
#                          if iclient.dealer:
#
#                              jsonclient = {
#                                 'name' : iclient.name,
#                                 'locations' : 'null'
#                              }
#                              jsonlocs = []
#                              for loc in locs:
#                                  if loc.client.name == iclient.name:
#                                      jsonloc = {
#                                         'name' : loc.name,
#                                         'online' : loc.is_online,
#                                         'secret_key' : loc.secret_key,
#                                         'has_unity' : True,
#                                         'batchnum' : 0
#
#                                      }
#                                      jsonlocs.append(jsonloc)
#                              jsonclient['locations'] = jsonlocs
#                              jsonclients.append(jsonclient)
#                      jsondealer['clients'] = jsonclients
#                      jsondealers.append(jsondealer)
#              obj['dealers'] = jsondealers
#
#              jsonlocs = []
#              locs = get_locations_for_profile(user.profile)
#              # locs = Location.objects.all()
#              # locnum = len(locs)
#              # batchsize = locnum / 3
#              # count = 0
#
#              for loc in locs:
#                  # 'is_online': True,
#                  # 'loc_data': 'null'
#                  jsonloc = {
#                     'name' : loc.name,
#                     'online' : loc.is_online,
#                     'secret_key' : loc.secret_key,
#                     'has_unity' : True,
#                     'client': loc.client.name,
#                     'batchnum': 0
#
#                  }
#
#
#
#                  jsonlocs.append(jsonloc)
#
#
#
#              obj['locations'] = jsonlocs
#
#
#          return JsonResponse(obj)
#
#      else:
#          return HttpResponse('Username or password is incorrect', status=401)
#
#  except:
#    e = sys.exc_info()
#    edict = {
#        'error':str(e)
#    }
#    print('api_report -  error : ', e)
#    return HttpResponse(status=500)
#
#
# def ng_energy_report(request):
#
#     try:
#         logger.debug('api_report - request : %s',request)
#         stuff = json.loads(request.body.decode('utf-8'))
#         secret_key = stuff['key']
#         logger.debug('api_report - secret_key : '+secret_key)
#         loc = Location.objects.get(secret_key=secret_key)
#         logger.debug('api_report - location : %s', loc)
#
#         from_date = stuff['from_date']
#         to_date = stuff['to_date']
#         logger.debug('api_report - dates : %s , %s', from_date, to_date)
#
#         start_ts = datetime.datetime.strptime(from_date, "%m/%d/%Y")
#         end_ts = datetime.datetime.strptime(to_date, "%m/%d/%Y")
#
#         logger.debug('api_report -  : %s %s %s %s %s', secret_key, from_date, to_date, start_ts, end_ts)
#         locname = loc.name
#     except:
#         e = sys.exc_info()[0]
#         edict = {
#             'error':str(e)
#         }
#         logger.debug('api_report -  error : %s', e)
#         # write_to_page( "<p>Error: %s</p>" % e )
#         return HttpResponse(json.dumps(edict))
#         # return base_views.index(request)
#     adminDb = pymongoclient['admin']
#     adminDb.authenticate("root","beetroot");
#
#     logger.debug('api_report -  prolog complete')
#     key = loc.key
#     hvacs = []
#     lights = []
#     kwmeters = []
#     kwrep = None
#     historical_kw = get_historical_usage_map(key)
#
#     alarms = list(dailydb.alarms.find({'key':key, 'ts':{'$gte':start_ts, '$lte':end_ts}}))
#     hvac_alarms = []
#
#     ids = dailydb.daily_logs.find({'key':key}).distinct('controller_id')
#     for i in ids:
#         c = dailydb.daily_logs.find({'key':key, 'controller_id':i}).sort('ts', -1).limit(1)[0]
#         # if c['type'] == 'hvac':
#         #     logger.debug('api_report -  processing hvac controller : %s', i)
#         #     id = c['controller_id']
#         #     rep = get_hvac_report(key, id, start_ts, end_ts)
#         #     if rep:
#         #         rep['controller_id'] = id
#         #         rep['name'] = c['name']
#         #         rep['alarms'] = []
#         #         for a in alarms:
#         #             if a['source_id'] == id:
#         #                 rep['alarms'].append(a)
#         #                 hvac_alarms.append(a)
#         #         logger.debug('api_report -  appending alarms to hvacs []')
#         #         hvacs.append(rep)
#         # elif c['type'] == 'light':
#         #     id = c['controller_id']
#         #     rep = get_light_report(key, id, start_ts, end_ts)
#         #     if rep:
#         #         rep['controller_id'] = id
#         #         rep['name'] = c['name']
#         #         lights.append(rep)
#         # elif c['type'] == 'kw_meter':
#         if c['type'] == 'kw_meter':
#             id = c['controller_id']
#             rep = get_kw_report(key, id, start_ts, end_ts)
#             if rep:
#                 rep['controller_id'] = id
#                 rep['name'] = c['name']
#                 kwmeters.append(rep)
#         elif c['type'] == 'demand analyzer':
#             id = c['controller_id']
#             rep = get_kw_report(key, id, start_ts, end_ts)
#             if rep:
#                 rep['controller_id'] = id
#                 rep['name'] = 'Energy Usage'
#                 kwrep = rep
#
#     # sort the controller lists
#     sortkey = lambda s: s['name'].lower()
#
#     # free_alarms = [x for x in alarms if not x in hvac_alarms]
#
#     hvacs = sorted(hvacs, key=sortkey)
#     lights = sorted(lights, key=sortkey)
#     kwmeters = sorted(kwmeters, key=sortkey)
#
#     # don't show individual kwmeters unless there's more than 1
#     if len(kwmeters) <= 1: kwmeters = []
#
#     dict = {
#         'key':key, 'locname':locname,
#         'kwmeters':kwmeters, 'kw':kwrep,
#         'from_date':from_date, 'to_date':to_date,
#         # 'hvacs':hvacs,
#         # 'lights':lights,
#         # 'free_alarms':free_alarms
#     }
#     return HttpResponse(json.dumps(dict, default=json_util.default))
#
# def ng_performance_report(request):
#
#     try:
#         logger.error('ng_performance_report - request : %s',request)
#         stuff = json.loads(request.body.decode('utf-8'))
#         secret_key = stuff['key']
#         logger.error('ng_performance_report - secret_key : '+secret_key)
#         loc = Location.objects.get(secret_key=secret_key)
#         logger.error('ng_performance_report - location : %s', loc)
#
#         from_date = stuff['from_date']
#         to_date = stuff['to_date']
#         logger.error('ng_performance_report - dates : %s , %s', from_date, to_date)
#
#         start_ts = datetime.datetime.strptime(from_date, "%m/%d/%Y")
#         end_ts = datetime.datetime.strptime(to_date, "%m/%d/%Y")
#
#         logger.error('ng_performance_report -  : %s %s %s %s %s', secret_key, from_date, to_date, start_ts, end_ts)
#         locname = loc.name
#     except:
#         e = sys.exc_info()[0]
#         edict = {
#             'error':str(e)
#         }
#         logger.error('ng_performance_report -  error : %s', e)
#         return HttpResponse(json.dumps(edict))
#
#     logger.error('ng_performance_report -  prolog complete')
#     key = loc.key
#     hvacs = []
#     lights = []
#     kwmeters = []
#     kwrep = None
#     historical_kw = get_historical_usage_map(key)
#
#     alarms = list(dailydb.alarms.find({'key':key, 'ts':{'$gte':start_ts, '$lte':end_ts}}))
#     hvac_alarms = []
#
#     ids = dailydb.daily_logs.find({'key':key}).distinct('controller_id')
#     for i in ids:
#         c = dailydb.daily_logs.find({'key':key, 'controller_id':i}).sort('ts', -1).limit(1)[0]
#         if c['type'] == 'hvac':
#             logger.debug('api_report -  processing hvac controller : %s', i)
#             id = c['controller_id']
#             rep = get_hvac_report(key, id, start_ts, end_ts)
#             if rep:
#                 rep['controller_id'] = id
#                 rep['name'] = c['name']
#                 rep['alarms'] = []
#                 for a in alarms:
#                     if a['source_id'] == id:
#                         rep['alarms'].append(a)
#                         hvac_alarms.append(a)
#                 logger.debug('api_report -  appending alarms to hvacs []')
#                 hvacs.append(rep)
#         elif c['type'] == 'light':
#             id = c['controller_id']
#             rep = get_light_report(key, id, start_ts, end_ts)
#             if rep:
#                 rep['controller_id'] = id
#                 rep['name'] = c['name']
#                 lights.append(rep)
#     sortkey = lambda s: s['name'].lower()
#
#     free_alarms = [x for x in alarms if not x in hvac_alarms]
#
#     hvacs = sorted(hvacs, key=sortkey)
#     lights = sorted(lights, key=sortkey)
#
#     dict = {
#         'key':key, 'locname':locname,
#         'from_date':from_date, 'to_date':to_date,
#         'hvacs':hvacs,
#         'lights':lights,
#         'free_alarms':free_alarms
#     }
#     return HttpResponse(json.dumps(dict, default=json_util.default))
#
# def ng_alarm_report(request):
#
#     try:
#         logger.debug('ng_alarm_report - request : %s',request)
#         stuff = json.loads(request.body.decode('utf-8'))
#         secret_key = stuff['key']
#         logger.debug('ng_alarm_report - secret_key : '+secret_key)
#         loc = Location.objects.get(secret_key=secret_key)
#         logger.debug('ng_alarm_report - location : %s', loc)
#
#         from_date = stuff['from_date']
#         to_date = stuff['to_date']
#         logger.debug('ng_alarm_report - dates : %s , %s', from_date, to_date)
#
#         start_ts = datetime.datetime.strptime(from_date, "%m/%d/%Y")
#         end_ts = datetime.datetime.strptime(to_date, "%m/%d/%Y")
#
#         logger.debug('ng_alarm_report -  : %s %s %s %s %s', secret_key, from_date, to_date, start_ts, end_ts)
#         locname = loc.name
#     except:
#         e = sys.exc_info()[0]
#         edict = {
#             'error':str(e)
#         }
#         logger.debug('ng_alarm_report -  error : %s', e)
#         return HttpResponse(json.dumps(edict))
#
#     logger.debug('ng_alarm_report -  prolog complete')
#     key = loc.key
#     hvacs = []
#     lights = []
#     kwmeters = []
#     kwrep = None
#     historical_kw = get_historical_usage_map(key)
#
#     alarms = list(dailydb.alarms.find({'key':key, 'ts':{'$gte':start_ts, '$lte':end_ts}}))
#     hvac_alarms = []
#
#     ids = dailydb.daily_logs.find({'key':key}).distinct('controller_id')
#     for i in ids:
#         c = dailydb.daily_logs.find({'key':key, 'controller_id':i}).sort('ts', -1).limit(1)[0]
#         if c['type'] == 'hvac':
#             logger.debug('api_report -  processing hvac controller : %s', i)
#             id = c['controller_id']
#             rep = get_hvac_report(key, id, start_ts, end_ts)
#             if rep:
#                 rep['controller_id'] = id
#                 rep['name'] = c['name']
#                 rep['alarms'] = []
#                 for a in alarms:
#                     if a['source_id'] == id:
#                         rep['alarms'].append(a)
#                         hvac_alarms.append(a)
#                 logger.debug('api_report -  appending alarms to hvacs []')
#                 hvacs.append(hvac_alarms)
#         elif c['type'] == 'light':
#             id = c['controller_id']
#             rep = get_light_report(key, id, start_ts, end_ts)
#             if rep:
#                 rep['controller_id'] = id
#                 rep['name'] = c['name']
#                 lights.append(rep)
#     sortkey = lambda s: s['name'].lower()
#
#     free_alarms = [x for x in alarms if not x in hvac_alarms]
#     logger.debug('ng_alarm_report');
#
#     # hvacs = sorted(hvacs, key=sortkey)
#     # lights = sorted(lights, key=sortkey)
#
#     dict = {
#         'key':key, 'locname':locname,
#         'from_date':from_date, 'to_date':to_date,
#         # 'hvacs':hvacs,
#         # 'lights':lights,
#         'free_alarms':free_alarms
#     }
#     return HttpResponse(json.dumps(dict, default=json_util.default))
#
#
# def get_historical_usage_map(key):
#     months = ["January", "February", "March", "April",
#               "May", "June", "July", "August", "September",
#               "October", "November", "December"]
#     data = []
#     try:
#         loc = HistoricalKWInfo.objects.get(location__key=key)
#         totals_str = loc.history
#         if len(totals_str) > 0:
#             for idx, val in enumerate(totals_str.split(',')):
#                 data.append({"month":months[idx], "total":int(val.strip())})
#     except: pass
#     return data
#
#
#
# ########################
# # RPC
#
# def status(request):
#   tunnels = []
#   try:
#     host = "http://bounce.kiteandlightning.com:4567/ports.json"
#     urls = urllib2.urlopen(host).readlines()
#     for u in urls:
#       tunnels.append(int(u) - 20000)
#   except: pass
#
#   locs = Location.objects.filter(notify_when_offline=True).order_by('tunnel_offset')
#   #locs = Location.objects.all().order_by('tunnel_offset')
#   out = []
#   for l in locs:
#     out.append({
#       "name":l.name,
#       "id":l.key,
#       "is_online":l.is_online,
#       "tunnel_offset":l.tunnel_offset,
#       "tunnel_online": True if l.tunnel_offset in tunnels else False
#     })
#   return json_response(out)
#
#
#
# def call(request):
#   if request.method == 'POST':
#     body = request.body.decode('utf-8')
#
#   else:
#     body = request.GET.dict()
#
#   try:
#     if request.method == 'POST':
#       c = json.loads(body)
#       # print(c)
#     else:
#       # construct a dict from query string params
#       c = body
#       c['params'] = [v for k, v in c.items() if k != 'method']
#
#     if not 'id' in c: c['id'] = 0
#     method = c['method']
#
#
# # "{'method': 'info';'params':[['f5e4591b4114e379d45463ad9e0985769da231f8']]}"
#
#   except:
#     return JsonResponse({'error':'parse error', 'input':body})
#
#   try:
#     if c['params']:
#       result = METHODS[method](*c['params'])
#     else:
#       result = METHODS[method]()
#     return JsonResponse({'result':result, 'error':None, 'id':c['id']})
#   except Exception as e:
#     return JsonResponse({'error':str(e), 'id':c['id']})
#
#
#
# def clean_emails(s):
#   return [x.strip() for x in s.split(',') if len(x) > 0]
#
# def method_send_notification(*args):
#   loc = Location.objects.get(key=args[0])
#   emails = clean_emails(loc.notification_emails)
#   if len(emails) > 0:
#     type = args[1]
#     send_mail('test mail', 'test body',
#               settings.DEFAULT_FROM_EMAIL, emails,
#               fail_silently=False)
#   return 1
#
#
# def method_get_notification_list(*args):
#   loc = Location.objects.get(key=args[0])
#   return clean_emails(loc.notification_emails)
#
#
# def method_upload_alarms(*args):
#   key = args[0]
#   loc = dailydb.locations.find_one({'key':key})
#   if loc:
#     alarms = args[1]
#     if alarms:
#       last_alarm = dailydb.alarms.find_one({"key":key}, sort=[("ts", -1)])
#       for a in alarms:
#         # annotate each item with the installation key
#         a['key'] = key
#         # convert timestamp to python datetime
#         a['ts'] = datetime.datetime.utcfromtimestamp(a['ts'])
#
#         if (last_alarm is None) or (a['ts'] > last_alarm['ts']):
#           dailydb.alarms.insert(a)
#
#   return 1
#
#
# def method_update_notify(*args):
#   key = args[0]
#   loc = Location.objects.get(key=key)
#
#   if loc:
#       new_emails = args[1]['local'] + loc.notification_emails.split(",")
#       new_emails = set(new_emails)
#       toadd = ""
#       count = 0
#       for thing in new_emails:
#           if count != 0:
#               toadd = toadd + "," + thing
#           else:
#               toadd = thing
#               count = count + 1
#
#       print(toadd)
#       loc.notification_emails = toadd
#
#       new_emails = args[1]['admins'] + loc.admin_emails.split(",")
#       new_emails = set(new_emails)
#       toadd = ""
#       count = 0
#       for thing in new_emails:
#           if count != 0:
#               toadd = toadd + "," + thing
#           else:
#               toadd = thing
#               count = count + 1
#       print(toadd)
#       loc.admin_emails = toadd
#       loc.notify_admins = args[1]['notify_admins']
#       loc.has_notifications = args[1]['enabled']
#       loc.save()
#
#
#
#
#
#
#   return 1
#
#
# def method_notify(*args):
#   key = args[0]
#   loc = Location.objects.get(key=key)
#
#   if loc:
#       if len(loc.notification_emails) > 1:
#
#           alert = args[1]
#           alarms = {
#           'alarm': {
#             'name': "%s Alarm",
#             'desc': "The %s alarm has triggered." },
#           'heat_fail': {
#             'name': "Heating Failure in %s unit",
#             'desc': "This alarm means that the %s unit is failing to heat correctly. It may indicate that the unit needs maintenance or repair."
#             },
#           'cool_fail': {
#             'name': "Cooling Failure in %s unit",
#             'desc': "This alarm means that the %s unit is failing to cool. It may indicate that the unit needs maintenance or repair."
#             },
#           'fz_low': {
#             'name': "Temperature Too Low in %s unit",
#             'desc': "The space temperature for this unit is too far below the setpoint. This may indicate that the unit needs adjustment."
#             },
#           'fz_high': {
#             'name': "Temperature Too High in %s unit",
#             'desc': "The space temperature for this unit is too high above the setpoint. This may indicate that a door has been left open."
#             },
#           'contact': {
#             'name': "Contact Closure Alarm from %s",
#             'desc': "A contact has closed in the %s unit and you are being notified."
#             },
#           'freezer_door': {
#             'name': "Door Open Alarm from %s",
#             'desc': "This freezer/cooler's door has been left open."
#             },
#           'open_door': {
#             'name': "Door Open Alarm from %s",
#             'desc': "This door has been left open."
#             },
#           'low_battery': {
#             'name': "Low Battery Alarm from %s",
#             'desc': "The battery in the %s unit needs to be replaced."
#             },
#           'co2': {
#             'name': "High CO2 Alarm",
#             'desc': "The CO2 level has risen above the configured alarm limit."
#             },
#           'amps': {
#             'name': "Amperage out of range in %s unit",
#             'desc': "The amperage for this unit is outside of the specified range."
#             },
#           'humidity_high': {
#             'name': "High humidity detected: %s",
#             'desc': "Humidity is above the configured alarm limit. Source: %s"
#             },
#           'suction_temp_low': {
#             'name': "Suction Line temperature too low in %s unit",
#             'desc': "The suction line temperature for this unit is too low and the compressor is being shut down to prevent freezing."
#             }
#           }
#
#           if alert['code'] in alarms.keys():
#               emails = loc.notification_emails.split(',')
#               emails1 = []
#               for email in emails:
#                   emails1.append(email.strip())
#
#               name = alarms[alert['code']]['name']
#
#               desc = alarms[alert['code']]['desc']
#               source_name = alert['source_name'].upper()
#
#               subject = name.replace('%s',source_name)
#               body = desc.replace('%s',source_name)
#               message = "This is an automated alarm notification from your Unity system.\n\n--------------------\nLocation: " + loc.name + "\nAlarm Type: " + subject + "\n\n" + body + "\n--------------------"
#               newsubject = loc.name + ": " + subject
#               send_mail(
#                   newsubject,
#                   message,
#                   "notifications@unityesg.com",
#                   emails1,
#                   fail_silently=False,
#               )
#
#
#
#
#
#
#       # print(args)
#     # alarms = args[1]
#     # if alarms:
#     #   last_alarm = dailydb.alarms.find_one({"key":key}, sort=[("ts", -1)])
#     #   for a in alarms:
#     #     # annotate each item with the installation key
#     #     a['key'] = key
#     #     # convert timestamp to python datetime
#     #     a['ts'] = datetime.datetime.utcfromtimestamp(a['ts'])
#     #
#     #     if (last_alarm is None) or (a['ts'] > last_alarm['ts']):
#     #       dailydb.alarms.insert(a)
#
#   return 1
#
# def method_upload_logs(*args):
#   key = args[0]
#   loc = dailydb.locations.find_one({'key':key})
#   # print(loc)
#   out = []
#   if loc:
#     packet = args[1]
#     if packet:
#       dates = []
#
#       for p in packet:
#         # annotate each item with the installation key
#         p['key'] = key
#
#         # convert date string to python datetime
#         p['ts'] = datetime.datetime.strptime(p['ts'], "%Y-%m-%d %H:%M:%S UTC")
#
#         # make a list of dates included in the packet
#         if not p['ts'] in dates:
#           out.append(p['ts'])
#           dates.append(p['ts'])
#
#       if len(dates) > 0:
#         # remove all current daily logs that match the date list and key
#         dailydb.daily_logs.remove({'key':key, 'ts':{'$in':dates}})
#
#         # insert new packet
#         dailydb.daily_logs.insert(packet)
#
#         # update last_log_date in location collection
#         dates.sort()
#         dailydb.locations.update({'key':key}, {'$set':{'last_log_date':dates[-1]}})
#
#       return out
#   return 0
#
# # return the last log date
# def method_info(*args):
#   key = args[0]
#   loc = dailydb.locations.find_one({'key':key})
#   last_alarm = dailydb.alarms.find_one({"key":key}, sort=[("ts", -1)])
#
#   ret = {"key":key, "last_log_date":None, "last_alarm_date":None}
#
#   if last_alarm:
#     # ret['last_alarm_date'] = last_alarm['ts']
#     ret['last_alarm_date'] = {
#          '$date': int(time.mktime(last_alarm['ts'].timetuple()) * 1000)
#     }
#
#   if 'last_log_date' in loc:
#     #ret['last_log_date'] = loc['last_log_date']
#     ret['last_log_date'] = {
#          '$date': int(time.mktime(loc['last_log_date'].timetuple()) * 1000)
#     }
#
#   return ret
#
#
# def method_get_timestamps(*args):
#   key = args[0]
#   myDb = pymongoclient[key]
#   result = []
#   collections = ['alarms', 'controllers', 'hvac_perf', 'hardware_devices', 'hardware_items', 'notification_log', 'schedules',  'users' ]
#   for collection_name in collections:
#       # get all of settings, maps, not things,
#       #
#       collection = myDb[collection_name]
#
#       if collection_name == 'notification_log':
#           newest = collection.find({}).sort('last_notified',-1).limit(1)
#           newestrecord = False
#           for thing in newest:
#               newestrecord = thing
#
#
#           if newestrecord:
#
#               result.append({'collection': collection_name, 'ts': thing['last_notified']})
#           else:
#               result.append({'collection': collection_name, 'ts': 0})
#
#       elif collection_name == 'controllers':
#
#           newestcontroller = False
#           newestcontrollerstatus = False
#           newestcontrollercursor = collection.find({}).limit(1).sort("ts", -1)
#           for thing in newestcontrollercursor:
#               newestcontroller = thing
#           if newestcontroller:
#
#               newestcontrollerstatuscursor = collection.find({'status':{'$exists': True}}).limit(1).sort("status.ts", -1)
#               for thing in newestcontrollerstatuscursor:
#                   newestcontrollerstatus = thing
#
#               highest_ts = newestcontroller['ts']
#
#               if newestcontrollerstatus['status']['ts'] > newestcontroller['ts']:
#                   highest_ts = newestcontrollerstatus['status']['ts']
#               result.append({'collection': collection_name, 'ts': highest_ts})
#
#           else :
#               result.append({'collection': collection_name, 'ts': 0})
#
#
#
#
#       else:
#
#
#         newest = collection.find({}).limit(1).sort("ts", -1)
#         newestrecord = False
#         for thing in newest:
#             newestrecord = thing
#         if newestrecord:
#             result.append({'collection': collection_name, 'ts': thing['ts']})
#         else:
#             result.append({'collection': collection_name, 'ts': 0})
#
#   return result
#
# def method_upload_records(*args):
#   key = args[0]
#   records = args[1]
#   myDb = pymongoclient[key]
#   result = []
#
#   collections = ['alarms', 'controllers', 'hvac_perf', 'hardware_devices', 'hardware_items', 'notification_log', 'schedules',  'users' ]
#
#   for record in records:
#
#       for collection_name in collections:
#
#
#           if record["collection"] == collection_name:
#               toDelete = []
#
#               cursor = myDb[collection_name].find({})
#               for mydoc in cursor:
#                   if mydoc:
#                       found = False
#
#                       for incomingid in record["ids"]:
#                           if incomingid == mydoc["_id"]:
#                               found = True
#
#                       if not found:
#                           toDelete.push(mydoc)
#
#               # remove out of date records
#               for mydoc in toDelete:
#                   myDb[collection_name].remove({'_id': mydoc['_id']})
#
#
#               # upsert all new records
#
#               for indoc in record["records"]:
#
#                   spid = indoc['_id']['$oid']
#                   indoc.pop('_id')
#
#                   myDb[collection_name].replace_one({'_id': spid}, indoc, upsert=True)
#
#   return result
#
#
#
# #####################
# # ENDPOINTS FOR "NEW" API? USED TO BE FROM API.PY IN OLD SERVER
#
# def clean_comma_str(s):
#   return [x.strip() for x in s.split(',') if len(x) > 0]
#
#
#
# def location_list(request):
#   locs = Location.objects.all()
#   out = [{"name":x.name, "id":x.id} for x in locs]
#   return HttpResponse(json.dumps(out))
#
# def notification_emails(request, key):
#   loc = get_object_or_404(Location, key=key)
#   return HttpResponse(json.dumps(clean_comma_str(loc.notification_emails)))
#
# def kw_history(request, key):
#   hist = get_object_or_404(HistoricalKWInfo, location__key=key)
#   return HttpResponse(json.dumps(clean_comma_str(hist.history)))
#
#
#
# METHODS = {
#
#   'update_notify':method_update_notify,
#
#   'notify':method_notify,
#
#   'get_timestamps':method_get_timestamps,
#
#   'upload_records':method_upload_records,
#
#   # info
#   'info':method_info,
#
#   # log upload
#   'upload_logs':method_upload_logs,
#
#   'upload_alarms':method_upload_alarms,
#
#   # post a new notification
#   'send_notification':method_send_notification,
#
#   # get the notification list for a key
#   'get_notification_list':method_get_notification_list
#
#   }
