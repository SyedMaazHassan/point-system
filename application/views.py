from django.shortcuts import render, redirect
from .models import *
from .supporting_func import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json


# main page function

def home(request):
    return render(request, "home.html")


def index(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.is_superuser:
        return redirect("admin-panel/")
    else:
        return redirect("user-panel/")

# function to create owner


def createOwner(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        organization_no = request.POST['orgNo']
        telephone = request.POST['telephone']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        context = {
            "name": name,
            "telephone": telephone,
            "l_name": l_name,
            "email": email,
            "orgNo": organization_no,
            "pass1": pass1,
            "pass2": pass2,
            "type": "#myOwnerTriggerForm",
            "btn": "#myOwnerTrigger"

        }
        if pass1 == pass2:
            if User.objects.filter(username=email).exists():
                messages.info(request, "Entered email already in use!")
                context['border'] = "email"
                return render(request, "register.html", context)

            if User.objects.filter(email=telephone).exists():
                messages.info(request, "Entered telephone already in use!")
                context['border'] = "telephone"
                return render(request, "register.html", context)

            if not validate_org_no(organization_no):
                messages.info(
                    request, "Kindly enter a valid orgnanization number!")
                context['border'] = "org"
                return render(request, "register.html", context)

            new_user = User.objects.create_user(
                username=email, email=telephone, first_name=name, password=pass1, last_name=l_name)
            new_user.save()

            new_business_owner = Business_Owner(
                user=new_user,
                owner_first_name=name,
                owner_last_name=l_name,
                business_email=email,
                business_telephone=telephone
            )

            new_business_owner.save()
            messages.info(request, "You have been registered successfully!")
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "register.html", context)


def createUser(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        telephone = request.POST['telephone']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        address = request.POST['address']
        areaCode = request.POST['areaCode']
        city = request.POST['city']

        context = {
            "name": name,
            "telephone": telephone,
            "l_name": l_name,
            "email": email,
            "pass1": pass1,
            "pass2": pass2,
            "address": address,
            "areaCode": areaCode,
            "city": city,
            "type": "#myUserTriggerForm",
            "btn": "#myUserTrigger"

        }
        if pass1 == pass2:
            if User.objects.filter(username=email).exists():
                messages.info(request, "Entered email already in use!")
                context['border'] = "email"
                return render(request, "register.html", context)

            if User.objects.filter(email=telephone).exists():
                messages.info(request, "Entered telephone already in use!")
                context['border'] = "telephone"
                return render(request, "register.html", context)

            new_user = User.objects.create_user(
                username=email, email=telephone, first_name=name, password=pass1, last_name=l_name)
            new_user.save()

            new_customer = Customer(
                user=new_user,
                user_first_name=name,
                user_last_name=l_name,
                user_email=email,
                user_telephone=telephone,
                user_address=address,
                user_area_code=areaCode,
                user_city=city
            )

            new_customer.save()

            # Create user account
            new_customer_account = Account()
            new_customer_account.create_customer_account(new_customer)

            messages.info(request, "You have been registered successfully!")
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "register.html", context)


# function for signup

def signup(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name": name,
            "l_name": l_name,
            "email": email,
            "pass1": pass1,
            "pass2": pass2,
        }
        if pass1 == pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email"
                return render(request, "register.html", context)

            user = User.objects.create_user(
                username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()
            messages.info(request, "You have been registered successfully!")
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "register.html", context)

    return render(request, "register.html")


# function for login

def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admin-panel/")
        else:
            return redirect("admin-panel/")

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'email': email,
            'password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)

            if request.user.is_superuser:
                return redirect("admin-panel/")

            return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return render(request, "signin.html", context)
            # return redirect("login")
    else:
        return render(request, "signin.html")


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("login")
