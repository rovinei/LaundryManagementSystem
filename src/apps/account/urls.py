from django.conf.urls import url
from src.apps.account import views

app_name = 'account'

urlpatterns = [
	url(r'^register$', views.register, name='register'),
	url(r'^login$', views.login, name='login'),
	url(r'^profile$', views.profile, name='profile'),
	url(r'^user/(?P<userid>\d+)/profile$', views.user_timeline, name='timeline'),
	url(r'^logout$', views.logout, name='logout'),

]