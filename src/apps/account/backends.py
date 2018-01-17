from src.apps.account.models import User


class AccountAuthBackend(object):
	def authenticate(self, username=None, password=None):

		try:
			user = User.objects.get(username=username)
			if user.check_password(password):
				return user

		except User.DoesNotExist:
			return None

	def get_user(self, user_id):

		try:
			user = User.objects.get(pk=user_id)
			if user.is_active:
				return user
			return None

		except User.DoesNotExist:
			return None
