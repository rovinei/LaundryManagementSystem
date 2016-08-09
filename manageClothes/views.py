from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.forms import modelformset_factory
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from .models import Clothe, handle_upload
from .forms import AddClotheForm
import os
from django.conf import settings
def upload_cloth(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
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
		return render(request,'manageClothes/cloth_list.html',context)
	else:
		context = {
			'message':'You must login!',
		}
		return redirect('/account/login')

def add_cloth(request):
	if request.user.is_authenticated():
		#form = AddClotheForm()
		#ClothFormSet = modelformset_factory(Clothe,form=AddClotheForm, extra=10)
		context = {
			'title':'Laundry Management | Add new cloth',
			#'form': form,
		}

		if request.method == 'POST':
			
			count_success_obj = 0;
			count_error_obj = 0;
			""""
			formset = ClothFormSet(request.POST, request.FILES,queryset=Clothe.objects.none())
			if formset.is_valid():
				for form in formset.cleaned_data:
					image = form['image']
					cloth = Clothes(image=image,user=request.user,type=request.POST['type'])
					cloth.save()
			"""
			print request.FILES
			print request.FILES.getlist('image')
			for cloth in enumerate(request.FILES.getlist('image')):
				form = AddClotheForm(request.POST,request.FILES)
				if form.is_valid():
					user = form.save(commit=False)
					user.user = request.user
					status = form.save()
					if status:
						count_success_obj += 1
					else:
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
		user_clothes = Clothe.objects.filter(user=request.user,is_laundry=True)

		context = {
			'user_clothes': user_clothes,
		}

		return render(request,'manageClothes/cloth_list.html',context)

	else:
		return redirect('/account/login')

def add_cloth_to_laundry(request):
	if request.user.is_authenticated():
		context = {
			'page_guide_msg': 'select clothes to add to laundry',
			'action_btn_name': 'Transfer',
		}
		if request.method == 'POST':
			clothes_dict = request.POST.getlist('clothes');
			added_cloth = Clothe.objects.filter(user=request.user, is_laundry=False, id__in=clothes_dict).update(is_laundry=True)
			if added_cloth:
				context.update({'status_add_msg': True,'count_obj':len(clothes_dict),})
			else:
				context.update({'status_add_msg': False,})

			user_clothes = Clothe.objects.filter(user=request.user ,is_laundry=False)
			laundry_cloth = Clothe.objects.filter(is_laundry=True)
			context.update({'user_clothes': user_clothes,'laundry_cloth': laundry_cloth,})

			
		else:

			user_clothes = Clothe.objects.filter(user=request.user ,is_laundry=False)
			laundry_cloth = Clothe.objects.filter(is_laundry=True)
			context.update({'user_clothes': user_clothes,'laundry_cloth': laundry_cloth,})

		return render(request,'manageClothes/checkable_cloth_list.html',context)

	else:
		return redirect('/account/login')

def remove_cloth_from_laundry(request):
	if request.user.is_authenticated():

		if request.user.is_admin:

			context = {
				'page_guide_msg': 'select clothes to take out from laundry',
				'action_btn_name': 'Remove',
			}

			if request.method == 'POST':

				clothes_dict = request.POST.getlist('clothes');
				removed_cloth = Clothe.objects.filter(is_laundry=True, id__in=clothes_dict).update(is_laundry=False)
				if removed_cloth:
					context.update({'status_remove_laundry_msg': True,'count_obj':len(clothes_dict),})
				else:
					context.update({'status_remove_laundry_msg': False,})

				user_clothes = Clothe.objects.filter(user=request.user, is_laundry=True)
				context.update({'user_clothes': user_clothes,})

				return render(request,'manageClothes/checkable_cloth_list.html',context)
			else:

				user_clothes = Clothe.objects.filter(is_laundry=True)
				context.update({'user_clothes': user_clothes,})

				return render(request,'manageClothes/checkable_cloth_list.html',context)
		else:

			return redirect('/admin/login')

	else:

		return redirect('/account/login')

def laundry_cloth(request):
	if request.user.is_authenticated():
		user_clothes = Clothe.objects.filter(is_laundry=True);
		
		context = {
			'user_clothes': user_clothes,
		}
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
		if request.user.is_admin:

			"""
			if cloth is already in laundry,
			take it out from laundry.
			"""
			if cloth.is_laundry == True:
				status = Clothe.objects.filter(pk=cloth.id).update(is_laundry=False)
				if status:
					context.update({'removestatus': True,})
				else:
					context.update({'removestatus': False,})

				user_clothes = Clothe.objects.filter(is_laundry=True)
				context.update({'user_clothes': user_clothes,})
				return render(request,'manageClothes/cloth_list.html',context)

			""" 
			if cloth not in laundry yet,
			"""
			if cloth.is_laundry == False:

				"""
				Admin/user can add only their own cloth,
				to laundry.
				"""
				if cloth.user == request.user:
					status = Clothe.objects.filter(pk=cloth.id).update(is_laundry=True)
					if status:
						context.update({'transferstatus': True,})
					else:
						context.update({'transferstatus': False,})
				else:
					context.update({'nopermissionadd': True})

				user_clothes = Clothe.objects.filter(is_laundry=True)
				context.update({'user_clothes': user_clothes,})
				return render(request,'manageClothes/cloth_list.html',context)


		""" if user is not an admin """
		if request.user.is_admin == False:

			"""
			if cloth not yet at laundry,
			"""
			if cloth.is_laundry == False:
				if cloth.user == request.user:
					status = Clothe.objects.filter(pk=cloth.id).update(is_laundry=True)
					if status:
						context.update({'transferstatus': True,})
					else:
						context.update({'transferstatus': False})

					user_clothes = Clothe.objects.filter(user=request.user ,is_laundry=True)
					context.update({'user_clothes': user_clothes,})
					return render(request,'manageClothes/cloth_list.html',context)

				else:
					user_clothes = Clothe.objects.filter(user=request.user ,is_laundry=True)
					context.update({'user_clothes': user_clothes,'nopermissionadd': True,})
					return render(request,'manageClothes/cloth_list.html',context)
					

			"""
			Cloth is not own by user,
			"""
			if cloth.is_laundry == True:
				user_clothes = Clothe.objects.filter(user=request.user ,is_laundry=True)
				context.update({'user_clothes': user_clothes,})
				if cloth.user == request.user:
					context.update({'already_at_laundry': True,})
				else:
					context.update({'existing_other_cloth': True,})
				return render(request,'manageClothes/cloth_list.html',context)
			
	else:
		return redirect('/account/login')

def user_dirty_bucket(request):
	if request.user.is_authenticated():
		context = {}

		user_clothes = Clothe.objects.filter(user=request.user, is_dirty=True, is_laundry=False)
		context.update({'user_clothes': user_clothes})
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
				context.update({'status_add_msg': True,'count_obj':len(clothes_dict),})
			else:
				context.update({'status_add_msg': False,})

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

