from django.contrib import admin
from .models import Clothe, LaundrySchedule
from image_cropping import ImageCroppingMixin          

         
"""
class UserAdmin(admin.ModelAdmin):
	list_display = ('__unicode__','email','phonenumber','uniqueid','timestamp')
	empty_value_display = '-empty-'
	fields = ('firstname', 'lastname', 'username','email','phonenumber')
"""

class ClotheAdmin(ImageCroppingMixin, admin.ModelAdmin):
	list_display = ('user','__unicode__','shortcode','img_thumbnail','is_laundry', 'is_dirty')
	empty_value_display = '-empty-'
	fields = ('type', 'image', 'is_laundry', 'is_dirty', 'user')
	search_fields = ('user','type','is_laundry', 'is_dirty')
	list_filter= ('user','type','is_laundry', 'is_dirty')

	"""
	def save_model(self,request,obj,form,change):
		obj.user = request.user
		obj.save()
	"""
class ScheduleAdmin(admin.ModelAdmin):
	list_display = ('room','day',)
	fields = ('room','day')
	search_fields = ('day','room')
	list_filter = ('day','room')

#admin.site.register(User,UserAdmin)
admin.site.register(Clothe,ClotheAdmin)
admin.site.register(LaundrySchedule,ScheduleAdmin)