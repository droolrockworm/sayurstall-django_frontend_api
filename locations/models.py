# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

MEASURE_CHOICES = [
    ('Tied Bunch','Tied Bunch'),
    ('Kg', 'Kg'),
    ('Unit','Unit'),
]

class Customer(models.Model):
      first_name = models.CharField(max_length=100)
      last_name = models.CharField(max_length=100)
      email = models.CharField(max_length=100)
      phone = models.CharField(max_length=100)
      address = models.CharField(max_length=100)
      optional = models.CharField(max_length=100)
      province = models.CharField(max_length=100)
      postal_code = models.CharField(max_length=100)
      city = models.CharField(max_length=100)
      country = models.CharField(max_length=100)
      state = models.CharField(max_length=100, blank=True, null=True)


class Order(models.Model):

      additional = models.TextField(blank=True, null=True)
      estimated_total = models.IntegerField(blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
      date_created = models.DateTimeField(null=True,blank=True)
      customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
      date_fulfilled = models.DateTimeField(null=True,blank=True)
      date_payed = models.DateTimeField(null=True,blank=True)
      total = models.IntegerField(blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.


class Aisle(models.Model):
      name = models.CharField(max_length=100)


      def __str__(self):
        return self.name
      def __unicode__(self):
        return self.name


class Category(models.Model):
      name = models.CharField(max_length=100)
      aisle = models.ForeignKey(Aisle, on_delete=models.CASCADE, blank=True, null=True)


      def __str__(self):
        return self.name
      def __unicode__(self):
        return self.name

class SubCategory(models.Model):
      name = models.CharField(max_length=100)
      category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)


      def __str__(self):
        return self.name
      def __unicode__(self):
        return self.name

class Product(models.Model):
      name = models.CharField(max_length=100)
      image = models.ImageField(upload_to="images/", null = True, blank = True)
      description = models.CharField(max_length=100, blank=True, null=True)
      price_per_kg = models.IntegerField(blank=True, null=True)
      price_per_tied_bunch = models.IntegerField(blank=True, null=True)
      price_per_unit = models.IntegerField(blank=True, null=True)
      subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)

      def __str__(self):
        return self.name
      def __unicode__(self):
        return self.name



class ProductOrder(models.Model):
      product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
      unit_price = models.IntegerField(blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
      measurement = models.CharField(max_length=100, choices=MEASURE_CHOICES, default='kg')
      quantity = models.IntegerField(blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
      order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
      # def get_choices(self, obj):
      #     temp = []
      #
      #     return obj.product.price_per_kg








class Users(models.Model):
    field_name_field = models.CharField(db_column='\ufeff"Name"', max_length=16)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    name_title = models.IntegerField(db_column='Name: Title', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    name_first = models.CharField(db_column='Name: First', max_length=11)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    name_middle = models.IntegerField(db_column='Name: Middle', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    name_last = models.CharField(db_column='Name: Last', max_length=11)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    email = models.CharField(db_column='Email', max_length=29)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=9)  # Field name made lowercase.
    user_status = models.CharField(db_column='User Status', max_length=8)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    user_roles = models.CharField(db_column='User Roles', max_length=119, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    people = models.CharField(db_column='People', max_length=16, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=19, blank=True, null=True)  # Field name made lowercase.
    tab_company = models.CharField(db_column='TAB Company', max_length=27, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    support = models.IntegerField(db_column='Support', blank=True, null=True)  # Field name made lowercase.
    open_sr_assigned = models.DecimalField(db_column='Open SR Assigned', max_digits=38, decimal_places=0)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sr_created = models.DecimalField(db_column='SR Created', max_digits=38, decimal_places=0)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    created = models.DateTimeField(db_column='Created', blank=True, null=True)  # Field name made lowercase.
    client_portal_company = models.CharField(db_column='Client Portal Company', max_length=25, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    given_password = models.CharField(db_column='Given Password', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    payroll = models.IntegerField(db_column='Payroll', blank=True, null=True)  # Field name made lowercase.
    jacktestcompany = models.CharField(db_column='JackTestCompany', max_length=21, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'users'