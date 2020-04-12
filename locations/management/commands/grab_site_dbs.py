## THIS WAS AN ATTEMPT TO HAVE THIS RUN AS A CRONJOB, PERIODICALLY USING THE
## RPC API OF EACH BOX TO LOAD CURRENT INFORMATION INTO A SINGLE MONGODB 
## INSTANCE, WHICH ANGULAR/MOBILE WOULD THEN USE TO GET LIVE DATA. TOO SLOW.
## TOO MANY LOGS TO UPLOAD TO HAVE SECOND BY SECOND LIVE STATUS. WORTH LOOKING
## INTO.


from django.core.management.base import BaseCommand, CommandError
import json
from locations.models import Location
from urllib.request import urlopen
from time import gmtime, strftime
from pymongo import MongoClient
from django.conf import settings
import socket
import traceback
from bson.objectid import ObjectId

# in crontab
# */3 * * * *	PYTHONPATH=/var/django/kl /var/django/kl/manage.py check_online




class Command(BaseCommand):
  args = '<none>'
  help = 'Queries the proxy server and marks locations on or offline'
  defaultdbs = ['admin', 'config', 'daily', 'local']
  def check_db():
    # if can't connect to db there will be an error in the log file
    client = MongoClient(settings.MONGO_HOST,settings.MONGO_PORT)
    # print(client.database_names)

    adminDb=client.admin
    adminDb.authenticate("root", "beetroot")
    print(client.database_names)
  def handle(self, *args, **options):
    try:
        locs = Location.objects.filter(client__name="Stagg")
        client = MongoClient(settings.MONGO_HOST,settings.MONGO_PORT)
        count = 1
        for loc in locs:


            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.timeout(5.0)

            port = 8000
            s.connect(('proxy.kiteandlightning.com', port))


            proxy_ident = {

                        'method':'proxy.ident',
                        'params': ['client']
            }
            s.sendall((json.dumps(proxy_ident)+"\r\n").encode('utf-8'))



            proxy_setdefaultserver = {
                      'method':'proxy.setdefaultserver',
                      'params': [loc.key, loc.secret_key]
            }
            s.sendall((json.dumps(proxy_setdefaultserver)+"\r\n").encode('utf-8'))


            kl_get_controllers = {

                        'method':'kl.get_controllers',
                        'params': [["name","type","subtype", "ts", "enabled","status","map_entries"],[["type",1],["subtype",1],["name",1]]],
                        'id':125
            }

            kl_get_users = {

                        'method':'kl.get_users',
                        'params': [],
                        'id':126
            }


            s.sendall((
                json.dumps(kl_get_controllers) + "\r\n" +
                json.dumps(kl_get_users) + "\r\n").encode('utf-8'))
            #
            # s.sendall((
            #     json.dumps(kl_get_controllers) + "\r\n").encode('utf-8'))

            mycount = 2
            data = ''
            msgs = 0
            while True:
              newdata = s.recv(2048).decode('utf-8')
              # print(newdata)
              # print('len newdata')
              # print(len(newdata))
              if not newdata:
                  break
              # print(newdata.count("\n"))

              msgs = msgs + newdata.count("\n")

              if msgs == mycount:
                  data = data + newdata
                  break
              else:
                  data = data + newdata

            if len(data) != 0:

                sepdata = data.split("\r\n")[:-1]
                # jsondata = json.loads(sepdata[1])
                # print(jsondata)
                for sep in sepdata:
                    jsondata = json.loads(sep)
                    # print(jsondata)

                    if jsondata['id'] == 125:

                        db=client[loc.key]

                        cursor = db['controllers'].find({})
                        for thing in cursor:
                            found = False
                            for controller in jsondata['result']:
                                if str(controller['_id']['$oid']) == str(thing['_id']):
                                    found = True
                                    db['controllers'].update({'_id': thing['_id']},
                                    {'$set':{
                                        'enabled': controller['enabled'],
                                        'subtype': controller['subtype'],
                                        'name': controller['name'],
                                        'type': controller['type']}})
                                    if 'status' in controller:
                                        db['controllers'].update({'_id': thing['_id']},
                                        {'$set':{'status': controller['status']}})
                                    else:
                                        db['controllers'].update({'_id': thing['_id']},
                                        {'$unset':{'status': ''}})
                                    if 'map_entries' in controller:
                                        db['controllers'].update({'_id': thing['_id']},
                                        {'$set':{'map_entries': controller['map_entries']}})
                                    else:
                                        db['controllers'].update({'_id': thing['_id']},
                                        {'$unset':{'map_entries': ''}})
                                    # print(controller['_id']['$oid'])
                                    # print(thing['_id'])
                                else:
                                    print('whatever')
                            # print('hello')
                            # print(thing)

                        for controller in jsondata['result']:
                            _id=ObjectId(controller['_id']['$oid'])
                            # gregm, test inserting id controller['meta_id'] = controller['_id']['$oid']
                            # controller['meta_id'] = controller['_id']['$oid']
                            # print(db['controllers'])
                            # print(db['controllers'].find_one({'meta_id': controller['meta_id']}))
                            # gregm, test inserting real id # db['controllers'].update({'meta_id': controller['meta_id']},
                            db['controllers'].update_one({'_id': _id},
                            {'$set':{
                                # gregm, don't need to set _id if in query '_id': ObjectId(controller['meta_id']),
                                # 'meta_id': controller['meta_id'],
                                'enabled': controller['enabled'],
                                'subtype': controller['subtype'],
                                # 'ts': controller['ts'],
                                'name': controller['name'],
                                'type': controller['type']}}, upsert = True)
<<<<<<< HEAD
=======


                            ## there are not necessarily guaranteed "status" and "map_entries" fields

                            # gregm, try this with real _id
>>>>>>> 1af561ad249339a53e4bfc5562e3814b1b72e6d5
                            if 'status' in controller:
                                db['controllers'].update_one({'_id': _id},
                                {'$set':{'status': controller['status']}},
                                upsert=True)
                            else:
                                db['controllers'].update_one({'_id': _id},
                                {'$unset':{'status': ''}},
                                upsert=True)
                            if 'map_entries' in controller:
                                db['controllers'].update_one({'_id': _id},
                                {'$set':{'map_entries': controller['map_entries']}},
                                upsert=True)
                            else:
                                db['controllers'].update_one({'_id': _id},
                                {'$unset':{'map_entries': ''}},
                                upsert=True)

<<<<<<< HEAD
                            # there are not necessarily guaranteed "status" and "map_entries" fields


=======
                            if 'ts' in controller:
                                print("ts found in controller ",controller['_id']['$oid']," ts: ",controller['ts'])
                                db['controllers'].update_one({'_id': _id},
                                {'$set':{'ts': controller['ts']}},
                                upsert=True)

                            # if 'status' in controller:
                            #     db['controllers'].update({'meta_id': controller['meta_id']},
                            #     {'$set':{'status': controller['status']}}, upsert=True)
                            # else:
                            #     db['controllers'].update({'meta_id': controller['meta_id']},
                            #     {'$unset':{'status': ''}},
                            #     upsert=True)
                            # if 'map_entries' in controller:
                            #     db['controllers'].update({'meta_id': controller['meta_id']},
                            #     {'$set':{'map_entries': controller['map_entries']}}, upsert=True)
                            # else:
                            #     db['controllers'].update({'meta_id': controller['meta_id']},
                            #     {'$unset':{'map_entries': ''}},
                            #     upsert=True)
>>>>>>> 1af561ad249339a53e4bfc5562e3814b1b72e6d5


                    # if jsondata['id'] == 126:
                    #     for thing in jsondata['result']:
                    #         print(thing)


            else:
                # otherwise this location is offline, but don't delete the data
                print("report this location offline")

            # if count < 2:
            #     count = count + 1
            #     for thing in sepdata:
            #         print(count,"\n")
            #
            #         print(thing)






    except Exception as e:
        var = traceback.format_exc()

        print('api_report -  error : ', var)
      # raise CommandError(e)





 # totals = list(db.daily_logs.find({'key':key,
 #                              'controller_id':'demand analyzer',
 #                             'ts':{'$gte':start_ts, '$lte':end_ts}},
 #                             ['ts', 'total']))
 # print(totals)

      # if cant find database
      #   if (loc.new_proxy):

 #            if not (loc.key in keys1):
 #
 #              if loc.is_online:
 #                print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "(GMT) -", loc.name, "went offline of", '"',NEW_PROXY_URL,'"!\n')
 #                loc.is_online = False
 #                loc.save()
 #            else:
 #
 #              if not loc.is_online:
 #
 #                print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "(GMT) -", loc.name, "is back online of", '"',NEW_PROXY_URL,'"!\n')
 #
 #
 #                loc.is_online = True
 #                loc.save()
 #        else:
 #
 #            if not (loc.key in keys):
 #
 #              if loc.is_online:
 #                print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "(GMT) -", loc.name, "went offline of", '"',PROXY_URL,'"!\n')
 #
 #                loc.is_online = False
 #                loc.save()
 #            else:
 #              if not loc.is_online:
 #                print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "(GMT) -", loc.name, "is back online of", '"',PROXY_URL,'"!\n')
 #
 #
 #                loc.is_online = True
 #                loc.save()
