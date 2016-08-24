from __future__ import unicode_literals

from django.db import models
import string
BUILDING_TYPE = (
	('jasmine_hill','Jasmine Hill'),
	('hotel_container','Hotel Container'),
	('borey_a','Borey A'),
	('staff_house','Staff House'),
	('teacher_building','Teacher Building'),
)

class Accommodation(models.Model):
	type = models.CharField(max_length=200,choices=BUILDING_TYPE)
	roomnumber = models.CharField(max_length=50,unique=True,db_index=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	update = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		ordering = ["-timestamp","roomnumber"]

	def __unicode__(self):
		return (self.type +"_"+ self.roomnumber).replace("_"," ").capitalize()
	def __str__(self):
		return (self.type +"_"+ self.roomnumber).replace("_"," ").capitalize()

	def get_fullname(self):
		return (self.type +"_"+ self.roomnumber).replace("_"," ").capitalize()
