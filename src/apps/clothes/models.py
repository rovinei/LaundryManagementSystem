from __future__ import unicode_literals
from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import UserManager
from src.apps.accommodations.models import Accommodation
from image_cropping import ImageRatioField
import random, string, qrcode, os
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from datetime import datetime
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

today = datetime.today()
clothes_type = (
	('Shirt','Shirt'),
	('T-Shirt','T-Shirt'),
	('Trouser','Trouser'),
	('Jean','Jean'),
	('Shock','Shock'),
	('Towel','Towel'),
	('Short','Short'),
	('Jacket','Jacket'),
	('Blanket','Blanket'),
	('Skirt','Skirt'),
)

DAYS_CHOICE = (
	('Monday','Monday'),
	('Tuesday','Tuesday'),
	('Wednesday','Wednesday'),
	('Thursday','Thursday'),
	('Friday','Friday'),
	('Saturday','Saturday'),
	('Sunday','Sunday'),
)


def random_string(length,chars=string.ascii_uppercase+string.ascii_lowercase+string.digits):
	return ''.join(random.choice(chars) for x in range(length))


def handle_upload(instance, filename):
	filename_string = string.ascii_lowercase+string.digits
	return "{}/{}/{}/{}".format(instance.user.id,'clothes',today.strftime('%Y/%m/%d'),random_string(30,filename_string)+".png")


def qrcode_location(instance, filename):
	return "{}/{}/{}".format(instance.user.id,'qrimage',filename)


class QRCode(models.Model):
	qrimage = models.ImageField(upload_to=handle_upload)


class ClothQuerySet(models.query.QuerySet):

	def all_cloth(self):
		return self.all()

	def laundry_cloth(self):
		return self.filter(is_laundry=True)

	def user_cloth(self,user):
		return self.filter(user=user)

	def user_laundry_cloth(self,user):
		return self.filter(user=user,is_laundry=True)

	def specific_type(self,type):
		return self.filter(type=type)

	def user_specific_type(self,user,type):
		return self.filter(user=user,type=type)


class ClothManager(UserManager):
	def get_queryset(self):
		return ClothQuerySet(self.model, using=self._db)

	def all_cloth(self):
		return self.get_queryset().all_cloth()

	def laundry_cloth(self):
		return self.get_queryset().laundry_cloth()

	def user_cloth(self,user):
		return self.get_queryset().user_cloth()

	def user_laundry_cloth(self,user):
		return self.get_queryset().user_laundry_cloth()

	def specific_type(self,type):
		return self.get_queryset().specific_type()

	def user_specific_type(self,user,type):
		return self.get_queryset().user_specific_type()


class Clothe(models.Model):
	type = models.CharField(max_length=200, choices=clothes_type)
	shortcode = models.CharField(max_length=10, unique=True)
	image = models.ImageField(upload_to=handle_upload)
	qrimage = models.ImageField(upload_to=qrcode_location, blank=True, null=True, default=None)
	square_image = ImageRatioField('image', '640x640')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	is_laundry = models.BooleanField(default=False)
	is_dirty = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __unicode__(self):
		return self.type

	def __str__(self):
		return self.type

	def generate_qr(self):
		qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_L,
			box_size=10,
			border=4
		)

		qr.add_data('http://192.168.96.162:8000'+ reverse('clothes:add_remove',kwargs={'code':self.shortcode,}))
		"""
		data = {
			'Username': self.user.username,
			'Type': self.type,
			'Shortcode': self.shortcode,
			'Email': self.user.email,
			'Contact': self.user.phonenumber,
		}
		qr.add_data(data)
		"""
		qr.make(fit=True)
		img = qr.make_image()
		buffer = BytesIO()
		img.save(buffer)
		filename = 'qrcode_{}.png'.format(self.shortcode)
		filebuffer = InMemoryUploadedFile(
			buffer, None, filename, 'image/png', len(buffer.getvalue()), None)
		self.qrimage.save(filename, filebuffer, False)

	def get_qrcode_url(self):
		if self.qrimage and hasattr(self.qrimage, 'url'):
			return self.qrimage.url
		else:
			return None

	def img_thumbnail(self):
		if self.image:
			return format_html('<img class="admin_clothe_thumb" src="{}" height="90px">',self.image.url)

	def is_being_laundry(self):
		return self.is_laundry

	def save(self,*args,**kwargs):

		self.shortcode = random_string(10,string.ascii_uppercase+string.digits)
		self.generate_qr()
		super(Clothe,self).save(*args,**kwargs)


@receiver(post_delete, sender=Clothe)
def auto_delete_file_on_delete(sender, instance, **kwargs):
	if instance.image:
		if os.path.isfile(instance.image.path):
			os.remove(instance.image.path)
	if instance.qrimage:
		if os.path.isfile(instance.qrimage.path):
			os.remove(instance.qrimage.path)


@receiver(pre_save, sender=Clothe)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_file = Clothe.objects.get(pk=instance.pk).image
    except Clothe.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class LaundrySchedule(models.Model):
	"""
	Schedule for laundry
	"""
	room = models.ForeignKey(Accommodation,on_delete=models.CASCADE)
	day = models.CharField(max_length=50,choices=DAYS_CHOICE)
	timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
	updated = models.DateTimeField(auto_now_add=False,auto_now=True)
	
	class Meta:
		unique_together = (('room', 'day'),)





		

