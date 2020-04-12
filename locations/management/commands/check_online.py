from django.core.management.base import BaseCommand, CommandError
import json
from locations.models import Location
from urllib.request import urlopen
from time import gmtime, strftime

# in crontab
# */3 * * * *	PYTHONPATH=/var/django/kl /var/django/kl/manage.py check_online


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
