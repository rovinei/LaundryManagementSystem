from django.contrib import admin
from .models import Accommodation


class AccommodationAdmin(admin.ModelAdmin):
	list_display = ('type','roomnumber','timestamp','update',)
	empty_value_display = '-empty-'
	fields = ('type', 'roomnumber',)
	search_fields = ('type', 'roomnumber',)
	list_filter= ('type','roomnumber',)


admin.site.register(Accommodation, AccommodationAdmin)
