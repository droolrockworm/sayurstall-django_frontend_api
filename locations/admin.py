# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from locations.models import *

class UsersAdmin(admin.ModelAdmin):
    list_display = ['name_title']


admin.site.register(Users, UsersAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Category, CategoryAdmin)

class AisleAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Aisle, AisleAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(SubCategory, SubCategoryAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['email']


admin.site.register(Customer, CustomerAdmin)
class ProductInline(admin.TabularInline):
    model = Product
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name','quantity']
    def product_name(self, obj):
        return obj.product.name
    product_name.admin_order_field  = 'product'  #Allows column order sorting
    product_name.short_description = 'Product Name'  #Renames column head
    # product_name.admin_order_field  = 'product_order__product_name'
    #Filtering on side - for some reason, this works
    #list_filter = ['title', 'author__name']
    readonly_fields = ['product_price_per_kg']
    def product_price_per_kg(self, obj):
        return obj.product.price_per_kg
    #
    # inlines = [
    #     ProductInline,
    # ]


admin.site.register(ProductOrder, ProductOrderAdmin)

class ProductOrderInline(admin.TabularInline):
    model = ProductOrder



class OrderAdmin(admin.ModelAdmin):
    list_display = ['id']
    inlines = [
        ProductOrderInline,
    ]


admin.site.register(Order, OrderAdmin)

# class ScrapeStatusFilter(SimpleListFilter):
#   title = 'Scrape status' # a label for our filter
#   parameter_name = 'pages' # you can put anything here
#
#   def lookups(self, request, model_admin):
#     # This is where you create filter options; we have two:
#     return [
#         ('scraped', 'Scraped'),
#         ('not_scraped', 'Not scraped'),
#     ]
#
#   def queryset(self, request, queryset):
#     # This is where you process parameters selected by use via filter options:
#     if self.value() == 'scraped':
#         # Get websites that have at least one page.
#   return queryset.distinct().filter(pages__isnull=False)
#     if self.value():
#         # Get websites that don't have any pages.
#         return queryset.distinct().filter(pages__isnull=True)
#

#
# admin.site.register(Dealer)
#
# admin.site.register(HistoricalKWInfo)
#
# class LocationAdmin(admin.ModelAdmin):
#   list_display = ('name', 'client', 'installation_date', 'client_version', 'tunnel_offset', 'is_online')
#   list_filter = ('client','installation_date','client_version', 'is_online')
#   readonly_fields = ('key', 'secret_key',)
#   search_fields = ('name',)
#   ordering = ('name',)
#   filter_horizontal = ('devices',)
#
#
#
# admin.site.register(Location, LocationAdmin)
#
#
# class UserProfileAdmin(admin.ModelAdmin):
#   list_display = ('user', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'last_portal_login', 'last_mobile_login')
#   list_filter = ('email','phone', 'mobile', 'last_portal_login','last_mobile_login','client',)
#   search_fields = ('user__username',)
#   #ordering = ('user__username',)
#   filter_horizontal = ('locations',)
#
# admin.site.register(UserProfile, UserProfileAdmin)
#
# # class UserAdmin(admin.ModelAdmin):
# #   list_display = ('username', 'last_login', 'email', 'first_name', 'last_name',  'is_staff' )
# #     # id, password, last_login, is_superuser, username, first_name, last_name, email ,is_staff | is_active | date_joined
# #
# #   # list_filter = ('last_login', 'username', 'email_address', 'first_name', 'last_name', 'staff_status',)
# #   search_fields = ('username',)
# #   #ordering = ('user__username',)
# #   # filter_horizontal = ('locations',)
# #
# #
# # admin.site.unregister(User)
# #
# # admin.site.register(User, UserAdmin)
#
# class ClientAdmin(admin.ModelAdmin):
#   list_display = ('name',)
#   list_filter = ('name',)
#   search_fields = ('name',)
#   ordering = ('name',)
#   # filter_horizontal = ('locations',)
#   # ordering = ('name',)
#
# admin.site.register(Client, ClientAdmin)
#
#
# class DeviceAdmin(admin.ModelAdmin):
#   list_display = ('name',)
#   list_filter = ('name',)
#   search_fields = ('name',)
#   ordering = ('name',)
#   # filter_horizontal = ('locations',)
#   # ordering = ('name',)
#
# admin.site.register(Device, DeviceAdmin)