from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.forms import modelformset_factory
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from .models import Clothe, LaundrySchedule, handle_upload
from .forms import AddClotheForm
from accommodations.models import Accommodation
import os
import json
from datetime import datetime, date
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError 
today = date.today()

def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    progress_id = ''
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')

def upload_cloth(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			clothes_img = request.POST.getlist('image')
			
			form = AddClotheForm(request.POST,request.FILES)
			if form.is_valid():
				user = form.save(commit=False)
				user.user = request.user
				form.save()
		else:
			form = AddClotheForm()

		clothes = Clothe.objects.all()
		context = {
			'title':'Dashboard page',
			'form': form,
			'clothes': clothes,
		}
		return render(request,'manageClothes/dashboard.html',context)
	else:
		return redirect('/account/login')

def cloth_list(request):
	if request.user.is_authenticated():
		user_clothes = Clothe.objects.filter(user=request.user)
		context = {
			'user_clothes': user_clothes,
		}

		if(not len(user_clothes)>0):
			context.update({'page_guide_msg': 'no cloth found',})
		else:
			context.update({'page_guide_msg': 'Total clothes found : '+str(len(user_clothes)),})

		return render(request,'manageClothes/cloth_list.html',context)
	else:
		context = {
			'message':'You must login!',
		}
		return redirect('/account/login')

def add_cloth(request):
	if request.user.is_authenticated():
		
		context = {
			'title':'Laundry Management | Add new cloth',
		}

		if request.method == 'POST':
			
			count_success_obj = 0;
			count_error_obj = 0;
			cloth_imgs = request.FILES.getlist('image')
			form = AddClotheForm(request.POST,request.FILES)
			print cloth_imgs
			for img in cloth_imgs:
				
				if form.is_valid():
					# cloth = form.save(commit=False)
					cloth = Clothe(type=request.POST['type'],image=img, user=request.user)
					try:
						cloth.save()
						count_success_obj += 1
					except Exception, e:
						count_error_obj += 1
						
				else:
					pass

			user_clothes = Clothe.objects.filter(user=request.user).order_by('-timestamp')
			context.update({
				'count_success_obj': count_success_obj,
				'count_error_obj':count_error_obj,
				'user_clothes': user_clothes,
			})

			return render(request,'manageClothes/add_cloth.html',context)

		else:
			user_clothes = Clothe.objects.filter(user=request.user).order_by('-timestamp')
			context.update({'user_clothes': user_clothes,})
			return render(request,'manageClothes/add_cloth.html',context)

	else:
		return redirect('/account/login')

def user_laundry_cloth(request):
	if request.user.is_authenticated():
		user_clothes = Clothe.objects.filter(user=request.user,is_laundry=True,is_dirty=True)

		context = {
			'user_clothes': user_clothes,
		}

		if(not len(user_clothes)>0):
			context.update({'page_guide_msg': 'no cloth found at laundry',})
		else:
			context.update({'page_guide_msg': 'Total clothes found : '+str(len(user_clothes)),})

		return render(request,'manageClothes/cloth_list.html',context)

	else:
		return redirect('/account/login')

def add_cloth_to_laundry(request):
	if request.user.is_authenticated and request.user.is_admin:
		context = {
			'page_guide_msg': 'select clothes to add to laundry',
			'action_btn_name': 'Transfer',
		}

		if request.method == 'POST':
			clothes_dict = request.POST.getlist('clothes');
			added_cloth = Clothe.objects.filter(
											is_laundry=False,
											is_dirty=True,
											id__in=clothes_dict
											).update(is_laundry=True)
			if added_cloth:
				context.update({'status_add_msg': True,'count_obj':len(clothes_dict),})
			else:
				context.update({'status_add_msg': False,})

			user_clothes = Clothe.objects.filter(is_laundry=False,is_dirty=True)
			
			context.update({'user_clothes': user_clothes,})

			
		else:

			user_clothes = Clothe.objects.filter(is_laundry=False,is_dirty=True)
			#laundry_cloth = Clothe.objects.filter(is_laundry=True)
			context.update({'user_clothes': user_clothes,})

		return render(request,'manageClothes/checkable_cloth_list.html',context)

	else:
		return redirect('/admin/login')

def remove_cloth_from_laundry(request):
	if request.user.is_authenticated and request.user.is_admin:

		context = {
			'page_guide_msg': 'select clothes to take out from laundry',
			'action_btn_name': 'Remove',
		}

		if request.method == 'POST':

			clothes_dict = request.POST.getlist('clothes');
			removed_cloth = Clothe.objects.filter(
												is_laundry=True,
												is_dirty=True,
												id__in=clothes_dict
												).update(
												is_laundry=False,
												is_dirty=False
												)
			if removed_cloth:
				context.update({'status_remove_laundry_msg': True,'count_obj':len(clothes_dict),})
			else:
				context.update({'status_remove_laundry_msg': False,})

			user_clothes = Clothe.objects.filter(is_laundry=True,is_dirty=True)
			context.update({'user_clothes': user_clothes,})

			return render(request,'manageClothes/checkable_cloth_list.html',context)
		else:

			user_clothes = Clothe.objects.filter(is_laundry=True,is_dirty=True)
			context.update({'user_clothes': user_clothes,})

			return render(request,'manageClothes/checkable_cloth_list.html',context)
	else:

		return redirect('/admin/login')


def laundry_cloth(request):
	if request.user.is_authenticated():
		user_clothes = Clothe.objects.filter(is_laundry=True,is_dirty=True);
		
		context = {
			'user_clothes': user_clothes,
		}

		if(not len(user_clothes)>0):
			context.update({'page_guide_msg': 'no cloth at laundry',})
		else:
			context.update({'page_guide_msg': 'Total clothes at laundry found : '+str(len(user_clothes)),})

		return render(request,'manageClothes/cloth_list.html',context)

	else:
		return redirect('/account/login')

def remove_user_cloth(request):
	if request.user.is_authenticated():
		
		context = {
			'page_guide_msg': 'select clothes to remove',
			'action_btn_name': 'Remove',
		}

		if request.method == 'POST':
			clothes_dict = request.POST.getlist('clothes');
			removed_cloth = Clothe.objects.filter(user=request.user, id__in=clothes_dict,is_laundry=False).delete()

			if removed_cloth:
				
				context.update({'status_remove_msg': True,'count_obj':len(clothes_dict),})
			else:
				context.update({'status_remove_msg': False,})

			user_clothes = Clothe.objects.filter(user=request.user,is_laundry=False)
			context.update({'user_clothes': user_clothes,})
			return render(request,'manageClothes/checkable_cloth_list.html',context)

		else:
			user_clothes = Clothe.objects.filter(user=request.user,is_laundry=False)
			context.update({'user_clothes': user_clothes,})
			return render(request,'manageClothes/checkable_cloth_list.html',context)

	else:
		return redirect('/account/login')

def add_remove_with_qr(request,code):
	if request.user.is_authenticated():

		context = {}

		try:
			cloth = Clothe.objects.get(shortcode=code)
		except Clothe.DoesNotExist:
			context.update({'notexist': True,})
			user_clothes = Clothe.objects.filter(is_laundry=True)
			context.update({'user_clothes': user_clothes,})
			return render(request,'manageClothes/cloth_list.html',context)

		""" 
		if the user is admin
		"""
		"""
		if request.user.is_admin:

			
			if cloth is already in laundry,
			take it out from laundry.
			
			if cloth.is_laundry == True and cloth.is_dirty == True:
				status = Clothe.objects.filter(pk=cloth.id).update(is_laundry=False,is_dirty=False)
				if status:
					context.update({'removestatus': True,})
				else:
					context.update({'removestatus': False,})

				user_clothes = Clothe.objects.filter(is_laundry=True,is_dirty=True)
				context.update({'user_clothes': user_clothes,})
				return render(request,'manageClothes/cloth_list.html',context)


			elif cloth.is_dirty == False and cloth.is_laundry == False:
				if cloth.user == request.user:
					status = Clothe.objects.filter(pk=cloth.id).update(is_dirty=True)
					if status:
							context.update({'buckettransferstatus': True,})
					else:
						context.update({'buckettransferstatus': False,})
				else:
					context.update({'nopermissionadd': True,})

				user_clothes = Clothe.objects.filter(user=request.user,is_laundry=False,is_dirty=True)
				context.update({'user_clothes': user_clothes,})
				return render(request,'manageClothes/cloth_list.html',context)

			else:
				user_clothes = Clothe.objects.filter(user=request.user,is_laundry=False,is_dirty=True)
				context.update({'user_clothes': user_clothes,})
				return render(request,'manageClothes/cloth_list.html',context)


		#if user is not an admin
		elif request.user.is_admin == False:
		"""

		"""
		if cloth not yet at laundry and not dirty,
		add cloth to dirty bucket
		"""
		if cloth.is_dirty == False and cloth.is_laundry == False:
			if cloth.user == request.user:
				status = Clothe.objects.filter(pk=cloth.id).update(is_dirty=True)
				if status:
					context.update({'buckettransferstatus': True,})
				else:
					context.update({'buckettransferstatus': False,})

				user_clothes = Clothe.objects.filter(user=request.user ,is_laundry=False,is_dirty=True)
				context.update({'user_clothes': user_clothes,})

				if not len(user_clothes)>0:
					context.update({'page_guide_msg': 'no dirty cloth',})
				else:
					context.update({'page_guide_msg': 'Total dirty clothes found : '+str(len(user_clothes)),})

				return render(request,'manageClothes/cloth_list.html',context)

			else:
				user_clothes = Clothe.objects.filter(user=request.user ,is_laundry=False,is_dirty=True)
				context.update({'user_clothes': user_clothes,'nopermissionadd': True,})

				if not len(user_clothes)>0:
					context.update({'page_guide_msg': 'no dirty cloth',})
				else:
					context.update({'page_guide_msg': 'Total dirty clothes found : '+str(len(user_clothes)),})

				return render(request,'manageClothes/cloth_list.html',context)
				

		# if cloth already in dirty bucket
		elif cloth.is_dirty == True and cloth.is_laundry == False:
			user_clothes = Clothe.objects.filter(user=request.user ,is_dirty=True,is_laundry=False)
			context.update({'user_clothes': user_clothes,})

			if not len(user_clothes)>0:
					context.update({'page_guide_msg': 'no dirty cloth',})
			else:
				context.update({'page_guide_msg': 'Total dirty clothes found : '+str(len(user_clothes)),})

			if cloth.user == request.user:
				context.update({'already_dirty': True,})

			else:
				context.update({'nopermissionadd': True,})
			return render(request,'manageClothes/cloth_list.html',context)

		# if cloth is already at laundry
		elif cloth.is_dirty == True and cloth.is_laundry == True:

			if request.user.is_admin == True:
				status = Clothe.objects.filter(pk=cloth.id).update(is_laundry=False,is_dirty=False)
				if status:
					context.update({'removestatus': True,})
				else:
					context.update({'removestatus': False,})

				user_clothes = Clothe.objects.filter(is_laundry=True,is_dirty=True)
				context.update({'user_clothes': user_clothes,})

				if not len(user_clothes)>0:
					context.update({'page_guide_msg': 'no cloth in laundry',})
				else:
					context.update({'page_guide_msg': 'Total clothes found : '+str(len(user_clothes)),})

				return render(request,'manageClothes/cloth_list.html',context)
			else:
				user_clothes = Clothe.objects.filter(user=request.user,is_dirty=True,is_laundry=False)
				context.update({'user_clothes': user_clothes,})

				if not len(user_clothes)>0:
					context.update({'page_guide_msg': 'no dirty cloth',})
				else:
					context.update({'page_guide_msg': 'Total dirty clothes found : '+str(len(user_clothes)),})

				if cloth.user == request.user:
					context.update({'already_at_laundry': True,})
				else:
					context.update({'nopermissionadd': True,})
				return render(request,'manageClothes/cloth_list.html',context)

		else:
			user_clothes = Clothe.objects.filter(user=request.user,is_dirty=True,is_laundry=False)
			context.update({'user_clothes': user_clothes,})
			if not len(user_clothes)>0:
					context.update({'page_guide_msg': 'no dirty cloth',})
			else:
				context.update({'page_guide_msg': 'Total dirty clothes found : '+str(len(user_clothes)),})

			return render(request,'manageClothes/cloth_list.html',context)
	else:
		return redirect('/account/login')

def user_dirty_bucket(request):
	if request.user.is_authenticated():
		context = {}

		user_clothes = Clothe.objects.filter(user=request.user, is_dirty=True, is_laundry=False)
		context.update({'user_clothes': user_clothes})
		if(not len(user_clothes)>0):
			context.update({'page_guide_msg': 'no cloth found',})
		else:
			context.update({'page_guide_msg': 'Total clothes found : '+str(len(user_clothes)),})
		return render(request,'manageClothes/cloth_list.html',context)
	else:
		return redirect('/account/login')

def room_dirty_bucket(request):
	if request.user.is_authenticated():
		context = {}
		

	else:
		return redirect('/account/login')

def transfer_to_dirty_bucket(request):
	if request.user.is_authenticated():
		context = {
			'page_guide_msg': 'select clothes to add to bucket',
			'action_btn_name': 'Transfer',
		}

		if request.method == 'POST':
			clothes_dict = request.POST.getlist('clothes')
			added_cloth = Clothe.objects.filter(user=request.user, is_laundry=False, is_dirty=False, id__in=clothes_dict).update(is_dirty=True)
			if added_cloth:
				context.update({'status_add_bucket': True,'count_obj':len(clothes_dict),})
			else:
				context.update({'status_add_bucket': False,})

			user_clothes = Clothe.objects.filter(user=request.user ,is_laundry=False,is_dirty=False)
			context.update({'user_clothes': user_clothes,})

			if(not len(user_clothes) > 0):
				context.update({'page_guide_msg': 'no cloth to transfer',})
			

			return render(request,'manageClothes/checkable_cloth_list.html',context)

		else:

			user_clothes = Clothe.objects.filter(user=request.user ,is_laundry=False,is_dirty=False)
			context.update({'user_clothes': user_clothes,})

			if(not len(user_clothes) > 0):
				context.update({'page_guide_msg': 'no cloth to transfer',})
			

			return render(request,'manageClothes/checkable_cloth_list.html',context)
			

	else:
		return redirect('/account/login')

def remove_from_bucket(request):
	if request.user.is_authenticated():
		context = {
			'page_guide_msg': 'select cloth to remove',
			'action_btn_name': 'Remove',
		}

		if request.method == 'POST':
			clothes_dict = request.POST.getlist('clothes')
			removed_cloth = Clothe.objects.filter(
												user=request.user,
												is_dirty=True,
												is_laundry=False,
												id__in=clothes_dict
												).update(is_dirty=False)
			if removed_cloth:
				context.update({'status_remove_msg': True,'count_obj':len(clothes_dict),})
			else:
				context.update({'status_remove_msg': False,})
			
			user_clothes = Clothe.objects.filter(user=request.user,is_dirty=True,is_laundry=False)
			context.update({'user_clothes': user_clothes,})
			if(not len(user_clothes)>0):
				context.update({'page_guide_msg': 'no dirty cloth to remove',})
		else:

			user_clothes = Clothe.objects.filter(user=request.user,is_dirty=True,is_laundry=False)
			context.update({'user_clothes': user_clothes,})
			if(not len(user_clothes)>0):
				context.update({'page_guide_msg': 'no dirty cloth to remove',})

		return render(request,'manageClothes/checkable_cloth_list.html',context)

	else:
		return redirect('/account/login')

def collect_dirty_cloth(request):
	if request.user.is_authenticated and request.user.is_admin:
	
		context = {}
		if request.method == 'POST':
			room_dict = request.POST.getlist('room')
			status = Clothe.objects.filter(
										user__room__in=room_dict,
										is_dirty=True,
										is_laundry=False
										).update(is_laundry=True)
			if status:
				context.update({'success_collect_dirty': True,})
			else:
				context.update({'success_collect_dirty': False,})
			
		else:
			rooms = LaundrySchedule.objects.filter(day=today.strftime("%A"))
			user_clothes = Clothe.objects.filter(is_dirty=True,is_laundry=False)
			print today.strftime("%A")
			if not len(user_clothes)>0:
				context.update({'page_guide_msg':'no dirty cloth',})
			else:
				context.update({'page_guide_msg':'Total dirty clothes found : '+str(len(user_clothes)),})
			context.update({'user_clothes': user_clothes,'rooms':rooms,})

		return render(request,'manageClothes/collect_cloth.html',context)
			
	else:
		return redirect('/account/login')

def cloth_detail(request,code):
	if request.user.is_authenticated():
		try:
			cloth = Clothe.objects.get(shortcode=code)
		except cloth.DoesNotExist:
			cloth = None
			return cloth
		context = {
			'cloth': cloth,
		}
		return render(request,'manageClothes/cloth_detail.html',context)

	else:
		return redirect('/account/login')

