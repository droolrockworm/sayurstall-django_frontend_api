# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.conf import settings
from hashlib import sha1 as sha_constructor
from pymongo import MongoClient
import datetime
# for key generation
import random

client = MongoClient(settings.MONGO_URL)
db=client[settings.MONGO_DB]

ROLE_CHOICES = [
    ('read','READ'),
    ('ov', 'OV'),
    ('modes','MODES'),
]


class Dealer(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

class Client(models.Model):
  name = models.CharField(max_length=100)
  logo = models.ImageField(upload_to="logos/", null = True, blank = True)
  dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, blank=True, null=True)
  slug = models.SlugField(max_length=100, unique=True, editable=False)

  def generate_slug(self):
    slug = slugify(self.name)
    self.slug = slug
    suffix = 2
    while Client.objects.filter(slug=self.slug).exists():
      self.slug = "%s-%d" % (slug, suffix)
      suffix = suffix + 1

  def save(self, *args, **kwargs):
      self.generate_slug()
      super(Client, self).save(*args, **kwargs)
      if (self.logo):
          IMG_SIZE=(200,200)
          try:
            if (self.logo.width > IMG_SIZE[0] or self.logo.height > IMG_SIZE[1]):
              from PIL import Image
              image = Image.open(self.logo.path)
              if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')
              image.thumbnail(IMG_SIZE, Image.ANTIALIAS)
              image.save(self.logo.path, quality=95)

          except IOError:
              pass






  def __str__(self):
    return self.name

  class Meta:
    ordering = ['name']

REPORT_TYPE_CHOICES = [
  ('standard', 'Unity Standard Report')
]


class Device(models.Model):
  name = models.CharField(max_length=100)
  type = models.CharField(max_length=100)
  brand = models.CharField(max_length=100)
  model = models.CharField(max_length=100)
  serial = models.CharField(max_length=100)

  def __str__(self):
    return self.name

  class Meta:
    ordering = ['name']

  # def __str__(self):
  #   return self.user.username
  #
  # class Meta:
  #   verbose_name_plural = "User Profiles"
  #   ordering = ('user__username',)


class Location(models.Model):

  name = models.CharField(max_length=100)
  client = models.ForeignKey(Client, on_delete=models.CASCADE)
  installation_date = models.DateField(default=datetime.date.today)
  city = models.CharField(max_length=100, blank=True, null=True)
  state = models.CharField(max_length=100, blank=True, null=True)
  zip_code = models.CharField(max_length=100, blank=True, null=True)
  address = models.CharField(max_length=100, blank=True, null=True)
  notification_emails = models.TextField(help_text="Comma delimited list of email addresses.",
                                         blank=True)
  admin_emails = models.TextField(help_text="Comma delimited list of admin email addresses.",
                                         blank=True)
  has_notifications = models.BooleanField(help_text="Does this installation send notifications for alarms?",
                             default=True)
  notify_admins = models.BooleanField(help_text="Also notify admin emails for alarms?",
                             default=True)
  key = models.CharField(max_length=40, blank=True)
  secret_key = models.CharField(max_length=20, blank=True)
  has_unity = models.BooleanField(help_text="Does this installation have a Unity base station?",
                                  default=True)
  report_type = models.CharField(max_length=20, blank=True, choices=REPORT_TYPE_CHOICES,
                                 default='standard')
  client_version = models.IntegerField(default=4)
  is_online = models.BooleanField(default=False)
  notify_when_offline = models.BooleanField(default=True)
  tunnel_offset = models.IntegerField(default=0)
  devices = models.ManyToManyField(Device, blank=True)
  new_proxy = models.BooleanField(default=False)



  def save(self, *args, **kwargs):
    # if no key is present, generate one
    if not self.key:
      salt = sha_constructor(str(random.random()).encode('utf-8')).hexdigest()[:5]
      self.key = sha_constructor((salt+self.name).encode('utf-8')).hexdigest()

      salt = sha_constructor(str(random.random()).encode('utf-8')).hexdigest()[:5]
      self.secret_key = sha_constructor((salt+self.name).encode('utf-8')).hexdigest()[:20]

    # create mongo record (upsert)

    # always use the new daily mongodb hosted at db.unityesg
    db.locations.update({'key':self.key}, {'$set': {
        'name':self.name,
        'secret_key':self.secret_key
      }}, True)

    super(Location, self).save(*args, **kwargs)

  def delete(self, *args, **kwargs):
    # remove from mongo db
    db.locations.remove({'key':self.key})

    super(Location, self).delete(*args, **kwargs)


  def __str__(self):
    return self.name

  class Meta:
    ordering = ('name',)



class HistoricalKWInfo(models.Model):
  location = models.ForeignKey(Location, on_delete=models.CASCADE)
  history = models.TextField(help_text="Comma delimited list of 12 numbers")

  def __str__(self):
    return self.location.name

  class Meta:
    verbose_name_plural = "Historical KW Info"



class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  email = models.CharField(max_length=100, blank=True, null=True)
  first_name = models.CharField(max_length=100, blank=True, null=True)
  last_name = models.CharField(max_length=100, blank=True, null=True)
  phone = models.CharField(max_length=100, blank=True, null=True)
  role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='read')
  remote_username = models.CharField(help_text="The user to log in as when remote controlling Unity. Make sure there's actually a user by this name set up in Unity! Leave blank to use the username.", max_length=40, blank=True, null=True)
  company = models.CharField(max_length=100, blank=True, null=True, default='client__name')
  is_admin = models.BooleanField(default=False, help_text="Admins have access to all Locations. Only for K&L staff.")
  mobile = models.BooleanField(default=False, help_text="Permission to use mobile app")
  client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True, help_text="Choose a client to give this user access to ALL locations that belong to that Client. Leave blank to choose specific Locations.")
  dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, blank=True, null=True, help_text="Choose a dealer to give this user access to ALL Clients that belong to that Dealer. Leave blank to choose specific Locations.")
  locations = models.ManyToManyField(Location, blank=True)
  # test = models.CharField(max_length=100, blank=True, null=True)
  last_portal_login = models.DateTimeField(null=True,blank=True)

  last_mobile_login = models.DateTimeField(null=True,blank=True)
  new_email_update = models.DateTimeField(null=True,blank=True)

  def __str__(self):
    return self.user.username

  class Meta:
    verbose_name_plural = "User Profiles"
    ordering = ('user__username',)
