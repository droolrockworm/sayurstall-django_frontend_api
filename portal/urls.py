"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.contrib import admin
from django.urls import include, path
import locations
# from locations import views


# from portal.views import ng_authenticate, ng_location_data
urlpatterns = [ url(r'^admin/', admin.site.urls),
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#
    url(r'^ng_api/', include('locations.urls')),
#
#     # There maybe shouldn't be a login url
#     url('login/', locations.views.login),
#     url('get_email/', locations.views.get_email),
#
#
#     url(r'^logout/', locations.views.logout_view),
#
#
#     url(r'^$', locations.views.dashboard),
#
#     url(r'^dashboard2/$', locations.views.dashboard2),
#
#     url(r'^dashboard2/([-\w]+)/$', locations.views.client_dashboard),
#
#     url(r'^client/', locations.views.client),
#
#     url(r'^report/', locations.views.report),
#
#     url(r'^internal_reports/', locations.views.internal_reports),
#
#
#     url(r'^robots.txt', locations.views.robots),
#
#     url(r'^test.json', locations.views.test_multi_kw),
#
#
#     url(r'^site_setup/', locations.views.site_setup),
#
#
#     url(r'^status/', locations.views.status),
#
#
#     url(r'^daily_logs_api/', locations.views.call),
#
#
#     ## THESE TWO PAGES DON't Really do anything:
#     ## notification emails works, but kw_history returns
#     ## 404 for every locations ive tried. I actually can't
#     ## figure out what in this whole system uses these endpoints
#
#     url(r'^api/location/(?P<key>[a-f0-9]{40})/notification_emails/?$',
#       locations.views.notification_emails),
#
#     url(r'^api/location/(?P<key>[a-f0-9]{40})/kw_history/?$', locations.views.kw_history)
#
#
#
]
