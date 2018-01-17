from django.conf.urls import url
from . import views

app_name = 'clothes'

urlpatterns = [
	url(r'^$', views.cloth_list),
    url(r'^clothes/',  views.cloth_list),
    url(r'^dashboard/', views.cloth_list),
    url(r'^managecloth/cloth/add', views.add_cloth, name='add_cloth'),
    url(r'^managecloth/cloth/remove', views.remove_user_cloth, name='remove_user_cloth'),
    url(r'^managecloth/cloth/mycloth', views.cloth_list),
    url(r'^managecloth/cloth/(?P<code>\w{10})/detail', views.cloth_detail,name="cloth_detail"),
    url(r'^managecloth/user/dirty_bucket/$', views.user_dirty_bucket),
    url(r'^managecloth/user/dirty_bucket/transfer/$', views.transfer_to_dirty_bucket, name="add_to_bucket"),
    url(r'^managecloth/user/dirty_bucket/remove/$', views.remove_from_bucket, name="remove_from_bucket"),
    url(r'^managecloth/room/dirty_bucket', views.cloth_list),

    url(r'^managecloth/laundry/mycloth', views.user_laundry_cloth, 'user_laundry_cloth'),
    url(r'^managecloth/laundry/allcloth', views.laundry_cloth, name='laundry_cloth'),
    url(r'^managecloth/laundry/collect', views.collect_dirty_cloth, name='collect_dirty_cloth'),
    url(r'^managecloth/laundry/transfer', views.add_cloth_to_laundry, name='add_cloth_to_laundry'),
    url(r'^managecloth/laundry/remove', views.remove_cloth_from_laundry, 'remove_cloth_from_laundry'),
    url(r'^managecloth/qrcode/(?P<code>\w{10})/add_remove', views.add_remove_with_qr,name="add_remove"),
    url(r'^file/upload_progress/', views.upload_progress)
]