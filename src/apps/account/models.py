from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from src.apps.accommodations.models import Accommodation
import uuid, string, random
from datetime import datetime
today = datetime.today()


def random_string(length, chars=string.ascii_uppercase+string.ascii_lowercase+string.digits):
	return ''.join(random.choice(chars) for x in range(length))


def handle_upload_profile(instance, filename):
	filename_string = random_string(30, string.ascii_lowercase+string.digits)+".png"
	return "{}/{}/{}/{}".format(instance.id, 'profile', today.strftime('%Y/%m/%d'), str(instance.uuid) + filename_string)


def handle_upload_cover(instance, filename):
	filename_string = random_string(30, string.ascii_lowercase+string.digits)+".png"
	return "{}/{}/{}/{}".format(instance.id, 'backgroundcover', today.strftime('%Y/%m/%d'), str(instance.uuid) + filename_string)


Gender = (
	('M', 'Male'),
	('F', 'Female'),
	('Other', 'Other'),
)

departmentList = (
	('KIT', 'Kirirom Institute Of Technology'),
	('VKP', 'Vkirirom Pine Resort'),
	('A2A', 'A2A Town Cambodia'),
	('Other', 'Other'),
)

"""
class Organization(models.Model):
	name = models.CharField(max_length=500,unique=True,blank=False,null=False,db_index=True)
	total_employee = models.PositiveIntegerField(default=0)
	address = models.TextField(blank=False,null=False)
	registered_date = models.DateTimeField(auto_now=False,auto_now_add=True)
	updated = models.DateTimeField(auto_now=True,auto_now_add=False)

class Department(models.Model):
	name = models.CharField(max_length=500,blank=False,null=False)
	total_staff = models.PositiveIntegerField(default=0)
	organization = models.ForeignKey(Organization,on_delete=models.CASCADE)
	registered_date = models.DateTimeField(auto_now=False,auto_now_add=True)
	updated = models.DateTimeField(auto_now=True,auto_now_add=False)
"""


class AccountUserManager(BaseUserManager):
	def create_user(self, username, firstname, lastname, gender, password=None, **kwargs):
		if not username:
			raise ValueError('User must have a username')
		if not lastname:
			raise ValueError('Please enter a valid name')
		if not gender:
			raise ValueError('Please tell your gender')
		user = self.model(
			username=username,
			firstname=firstname,
			lastname=lastname,
			gender=gender,
			**kwargs
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, firstname, lastname, gender, password, **kwargs):
		u = self.create_user(username, firstname, lastname, gender, password=password, **kwargs)
		u.is_admin = True
		u.save(using=self._db)
		return u


class User(AbstractBaseUser, PermissionsMixin):
	"""
	Custom user model for A2A user
	"""
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	firstname = models.CharField(max_length=50, blank=True, null=True)
	lastname = models.CharField(max_length=50, blank=False, null=False)
	username = models.CharField(max_length=100, blank=False, null=False, unique=True, db_index=True)
	email = models.EmailField(max_length=150, unique=True, blank=True, null=True)
	phonenumber = models.IntegerField(blank=True, null=True)
	profilepic = models.ImageField(upload_to=handle_upload_profile, default='/images/default_user_profile.png')
	background_cover = models.ImageField(upload_to=handle_upload_cover, default='/images/default_user_cover_photo_gallaxy.png')
	gender = models.CharField(max_length=6, choices=Gender, default='Other')
	room = models.ForeignKey(Accommodation, null=True, blank=True, on_delete=models.CASCADE)
	department = models.CharField(max_length=50, choices=departmentList, default='Other')
	joined = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	objects = AccountUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['firstname', 'lastname', 'gender']

	def __unicode__(self):
		return self.username

	def __str__(self):
		return self.username

	def get_profile_pic(self):
		if self.profilepic and hasattr(self.profilepic, 'url'):
			return self.profilepic.url
		else:
			return '/images/default_user_profile.png'

	def get_background_cover(self):
		if self.background_cover and hasattr(self.background_cover, 'url'):
			return self.background_cover.url
		else:
			return '/images/default_user_cover_photo_gallaxy.png'

	def get_timeline_url(self):
		return '/account/user/{}/profile'.format(self.id)

	def get_full_name(self):
		return str(self.firstname + self.lastname)

	def get_short_name(self):
		return self.username

	#@property
	#def is_superuser(self):
		#return self.is_admin

	@property
	def is_staff(self):
		return self.is_admin

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return self.is_admin