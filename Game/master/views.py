from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from math import floor, ceil
from .models import Profile
from . import definitions

def calc_prod(player):
	call_time = now()
	prod_duration = call_time - player.last_active
	ticks = prod_duration.seconds
	total_production = ticks * player.production

	# Available production
	if player.resource < total_production * 5:
		total_production = ceil(player.resource / 5)
	
	# Available storage
	if (player.storage - player.products) < (player.production * ticks):
		total_production = (player.storage - player.products)
	
	player.products += total_production
	player.resource -= total_production * 5
	player.last_active = now()
	player.save()

@login_required
def index(request):
	context = {}
	player = Profile.objects.get(user = request.user)
	calc_prod(player)
	context["player"] = player
	if request.method == "POST":
		player.tax += player.products
		player.money += ( player.products * player.selling_mult )
		player.products -= player.products
		player.save()
	return render(request = request, template_name = "index.html", context = context)

@login_required
def profile(request):
	context = {}
	player = Profile.objects.get(user = request.user)
	calc_prod(player)
	context["player"] = player
	return render(request = request, template_name = "profile.html", context = context)

@login_required
def worker(request):
	context = {}
	context["workers"] = definitions.workers
	context["player"] = Profile.objects.get(user = request.user)
	if request.method == "POST":
		id = int(request.POST.get("id"))
		target = definitions.workers[id]
		player = context["player"]
		if player.money >= target["cost"] and player.level >= target["level"]:
			player.money -= target["cost"]
			player.production += target["production"]
			player.save()
		else:
			print("Not enough.")
	return render(request = request, template_name = "worker.html", context = context)

@login_required
def storage(request):
	context = {}
	context["storages"] = definitions.storages
	context["player"] = Profile.objects.get(user = request.user)
	if request.method == "POST":
		id = int(request.POST.get("id"))
		target = definitions.storages[id]
		player = context["player"]
		if player.money >= target["cost"] and player.level >= target["level"] and (player.tax > 20000 + 20000 * player.level):
			player.money -= target["cost"]
			player.storage += target["storage"]
			player.save()
		else:
			print("Not enough.")
	return render(request = request, template_name = "storage.html", context = context)

@login_required
def reputation(request):
	context = {}
	context["reps"] = definitions.reputations
	context["player"] = Profile.objects.get(user = request.user)
	if request.method == "POST":
		id = int(request.POST.get("id"))
		target = definitions.reputations[id]
		player = context["player"]
		if player.money >= target["cost"]:
			player.money -= target["cost"]
			player.reputation += target["rep"]
			if player.reputation >= definitions.level_req[player.level]:
				player.level += 1
				player.selling_mult = definitions.selling_mult[player.level]
			player.save()
		else:
			print("Not enough.")
	return render(request = request, template_name = "reputation.html", context = context)

@login_required
def resource(request):
	context = {}
	context["player"] = Profile.objects.get(user = request.user)
	if request.method == "POST":
		resource_request = int(request.POST.get("resource"))
		player = context["player"]
		if player.money >= resource_request:
			player.money -= resource_request
			player.resource += resource_request
			player.save()
		else:
			print("Not enough.")
	return render(request = request, template_name = "resource.html", context = context)

@login_required
def tax(request):
	context = {}
	context["player"] = Profile.objects.get(user = request.user)
	context["tax_limit"] = 20000 + 20000 * context["player"].level
	if request.method == "POST":
		tax_request = int(request.POST.get("resource"))
		player = context["player"]
		if player.money >= tax_request and tax_request < player.tax:
			player.money -= tax_request
			player.tax -= tax_request
			player.save()
		else:
			print("Not enough. Or overpaid.")
	return render(request = request, template_name = "tax.html", context = context)

def register(request):
	context = {}
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			profile = Profile(user = user)
			profile.save()
			auth_login(request = request, user = user)
			return redirect("master:index")
		else:
			print(form.errors)
			print(form.error_messages)
			context["user_form"] = UserCreationForm()
			return render(request = request, template_name = "register.html", context = context)
	else:
		context["user_form"] = UserCreationForm()
	return render(request = request, template_name = "register.html", context = context)

def login(request):
	context = {}
	if request.method == "POST":
		user = authenticate(request, username = request.POST.get("username"), password = request.POST.get("password"))
		if user is not None:
			auth_login(request, user)
			return redirect("master:index")
		else:
			return render(request = request, template_name = "index.html", context = context)
	else:
		pass
	return render(request = request, template_name = "login.html", context = context)

@login_required
def logout(request):
	context = {}
	auth_logout(request = request)
	return redirect("master:login")

def about(request):
	context = {}
	return render(request = request, template_name = "about.html", context = context)