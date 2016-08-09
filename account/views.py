from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.contrib.auth import login as account_login, authenticate, logout as account_logout
from django.views.decorators.csrf import csrf_protect
from .forms import AuthenticationForm, RegistrationForm
from .models import User
from manageClothes.models import Clothe

clothes_type = [
	'Shirt',
	'T-Shirt',
	'Trouser',
	'Jean',
	'Shock',
	'Towel',
	'Short',
	'Jacket',
	'Blanket',
]

@csrf_protect
def login(request):
	if request.user.is_authenticated():
		return redirect('/')
	else:
		if request.method == 'POST':
			form = AuthenticationForm(data=request.POST)
			if form.is_valid():
				user = authenticate(username=request.POST['username'],password=request.POST['password'])
				if user is not None:
					if user.is_active:
						account_login(request,user)
						return redirect('/dashboard')

		else:
			form = AuthenticationForm()

	return render(request,'account/login.html',{'form':form})

@csrf_protect
def register(request):
	if request.user.is_authenticated():
		return redirect('/')
	else:
		if request.method == 'POST':
			form = RegistrationForm(data=request.POST)
			if form.is_valid():
				user = form.save()
				return redirect('/account/login')

		else:
			form = RegistrationForm()

	return render(request,'account/register.html',{'form':form})

@csrf_protect
def profile(request):
	if request.user.is_authenticated():
		user = User.objects.get(id=request.user.id)
		user_clothes = Clothe.objects.filter(user=request.user)
		context = {
			'user': user,
			'user_clothes':user_clothes,
		}
		return render(request,'manageClothes/cloth_list.html',context)
	else:
		redirect('/account/login')

def user_timeline(request,userid):
	user = User.objects.get(pk=userid)
	user_clothes = Clothe.objects.filter(user=user).order_by('-timestamp')
	laundry_clothes = user_clothes.filter(is_laundry=True)
	total_cloth = {}
	total_laundry = {}
	total_laundry_clothes = 0
	total_clothes = 0
	for i in range(len(clothes_type)):
		cloth_count = user_clothes.filter(type=clothes_type[i]).count()
		total_cloth.update({clothes_type[i].replace('-','').lower():cloth_count,})

		laundry_count = user_clothes.filter(type=clothes_type[i],is_laundry=True).count()
		total_laundry.update({clothes_type[i].replace('-','').lower():laundry_count,})
		total_clothes = total_clothes + cloth_count
		total_laundry_clothes = total_laundry_clothes + laundry_count
	
	context = {
		'user': user,
		'user_clothes': user_clothes,
		'total_cloth': total_cloth,
		'total_laundry': total_laundry,
		'total_laundry_clothes': total_laundry_clothes,
		'total_clothes': total_clothes,
	}
	if request.user.is_authenticated():
		return render(request,'manageClothes/user_timeline.html',context)
	else:
		return render(request,'manageClothes/user_timeline.html',context)

def logout(request):
	"""
	log user out
	"""
	account_logout(request)
	return redirect('/account/login')
	

