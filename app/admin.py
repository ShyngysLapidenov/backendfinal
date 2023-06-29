from django.contrib import admin
from .models import City, Hotel
# Register your models here.
class HotelAdmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields=('name',)
admin.site.register(Hotel)
admin.site.register(City, HotelAdmin)
