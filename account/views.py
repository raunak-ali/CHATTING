from typing import ContextManager
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
import requests
import random

from account.forms import AccountUpdateForm, RegistrationForm, AccountAuthenticationForm
from account.models import Account
def search_view(request, *args, **kwargs):
    print("yooooo")
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = Account.objects.filter(Q(username__icontains=search_query) | Q(email__icontains=search_query))
            user = request.user
            accounts = [] # [(account1, True), (account2, False), ...]
            for s in search_results:
                accounts.append((s, False)) # you have no friends yet
            context["accounts"] = accounts
    return render(request, 'results.html', context)


def register_view(request,*args,**kwargs):
    context={}
    
    user=request.user
    if user.is_authenticated:
        return HttpResponse(f"You are  already authenticated as : {user.email}.")
       
        
    if request.POST:
        form=RegistrationForm(request.POST)
        cap=request.POST.get("captha")
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                form.save()
                email=form.cleaned_data.get('email').lower()
                raw_password=form.cleaned_data.get('password1')
                account = authenticate(email=email, password=raw_password)
                login(request, account)
                destination = kwargs.get("next")
                if destination:
                    return redirect(destination)
                return redirect('personal:home')
                
            else:
                return HttpResponse(f"Please fill correct capcha")
        else:
                    context["registration_form"] = form      
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    
    return render(request,'register.html',context)

def logout_view(request):
    logout(request)
    return redirect("personal:home")
def login_view(request,*args,**kwargs):
    context={}
    user=request.user
    if user.is_authenticated:
        return redirect("personal:home")
    destination=get_redirect_if_exists(request)
    print("destination: " + str(destination))
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("personal:home")
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, "login.html", context)

def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect
def account_views(request,*args,**kwargs):
    context={}
    user_id=kwargs.get("user_id")
    try:
        account=Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return HttpResponse("NOPE NOT USER")
    if account:
        context['id']=account.id
        context['username']=account.username
        context['email']=account.email
        is_self=True
        user=request.user
        if user.is_authenticated and user!=account:
            is_self=False
        elif not user.is_authenticated:
            is_self=False
        context['is_self']=is_self
        context['BASE']=settings.BASE_URL
        return render(request, "account.html", context)
def edit_account_view(request,*args,**kwargs):
    if not request.user.is_authenticated:
        return redirect("Login")
    user_id =kwargs .get("user_id")
    try:
        account=Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return HttpResponse("SOmething is wrong")
    if account.pk !=request.user.pk:
        return HttpResponse("yOu cannot edit others")
    context={}
    if request.POST:
        form=AccountUpdateForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect ("account:view",user_id=account.pk)
        else:
            form=AccountUpdateForm(request.POST, instance=request.user,
                initial={
                   "id":account.pk,
                   "email":account.email,
                   "username":account.username,
                   "hide_email":account.hide_email,

                }
            )
            context['form']=form
    else:
        form=AccountUpdateForm(
                initial={
                   "id":account.pk,
                   "email":account.email,
                   "username":account.username,
                   "hide_email":account.hide_email,

                }
            )

        context['form']=form
    return render(request, "edit_account.html", context)
