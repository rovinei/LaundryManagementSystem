from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from account.models import User
from account.forms.register import RegistrationForm

class UserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('username', 'firstname', 'lastname', 'gender', 'email', 'phonenumber', 'profilepic', 'password', 'is_admin','is_active')
	def clean_password(self):
	# Regardless of what the user provides, return the initial value.
	# This is done here, rather than on the field, because the
	# field does not have access to the initial value
		return self.initial["password"]


class UserAdmin(BaseUserAdmin):
	# The forms to add and change user instances
	form = UserChangeForm
	add_form = RegistrationForm

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ('username', 'firstname', 'lastname', 'gender','is_admin')
	list_filter = ('is_admin','username', 'gender')
	fieldsets = (
		(_('Personal info'),{'fields':('username', 'firstname', 'lastname', 'gender')}),
		(_('Profile'),{'fields':('profilepic',)}),
		(_('Contact info'),{'fields':('email', 'phonenumber',)}),
		(_('Permission'),{'fields':('is_admin',)}),
		(_('Account status'),{'fields':('is_active',)}),
		(_('Security'),{'fields':('password',)})
	)

	add_fieldsets = (
		('Personal info',{'classes':'wide','fields':('username','firstname','lastname', 'gender')}),
		('Contact info',{'classes':'wide','fields':('email', 'phonenumber',)}),
		(_('Profile'),{'fields':('profilepic',)}),
		('Permission',{'classes':'wide','fields':('is_admin',)}),
		('Account status',{'classes':'wide','fields':('is_active',)}),
		('Security',{'fields':('password1', 'password2',)}),
	)
	ordering = ('username','joined')
	empty_value_display = '-empty-'
# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)