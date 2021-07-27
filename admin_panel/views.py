import builtins
from django.core.checks import messages
from django.db.models.expressions import Value
from django.shortcuts import render, redirect
from application.models import *
from django.http import JsonResponse
import json
from user_panel.supporting_func import *
from admin_panel.supporting_func import *
from application.supporting_func import *
from django.db.models import Sum
from django.urls import resolve
from django.contrib import messages


def all_businesses(request):
    context = {
        'admin_account_info': get_admin_account_details()
    }
    list_of_my_business = Business.objects.all()
    context['all_businesses'] = list_of_my_business
    context['page_title'] = "All Business"
    context['admin'] = True
    return render(request, "my-business-list.html", context)


def send_points(request):
    output = {'status': False}
    if request.user.is_authenticated and request.user.is_superuser:
        admin_account_info = get_admin_account_details()
        if request.method == "GET" and request.is_ajax():
            business_id = request.GET['business_id']
            value = request.GET['value']
            if business_id and value:
                business_query = Business.objects.filter(id=business_id)
                if business_query.exists() and admin_account_info['total_balance']:
                    focused_business = business_query[0]
                    points_to_give = float(value)
                    # Adding new distribution
                    new_distribution = Distribution(
                        points_to_give=points_to_give,
                        business=focused_business
                    )
                    new_distribution.save()

                    # transfer funds FROM admin to Business account
                    new_distribution.transfer_to_business()
                    # Running distribution loop
                    new_distribution.run_now(points_to_give)
                    new_distribution.is_completed = True
                    new_distribution.save()

                    output['admin_account_info'] = get_admin_account_details()
                    output['status'] = True

    return JsonResponse(output)


def get_customer_list(request):
    output = None
    if request.method == "GET" and request.is_ajax():
        business_id = request.GET['business_id']
        business = Business.objects.get(id=business_id)
        customer_list_output = business.all_customers()
        output = customer_list_output
        output['image'] = str(business.banner_image)
    return JsonResponse(output)

# Create your views here.


def business(request):
    pass


def add_admin_points(request):
    if request.method == "POST":
        redirect_uri = request.POST['redirect_url']
        new_points = request.POST['new_points']

        if redirect_uri and new_points:
            new_points = float(new_points)

            new_transfer = Transfer()
            new_transfer.charge_admin_account(new_points)
            messages.info(request, "Points balance updated!")
            return redirect(redirect_uri)

    return redirect("index")


def buyer(request, customer_id):
    admin_account_info = get_admin_account_details()
    print(admin_account_info)
    redirect_url = redirect_uri(request)

    # return redirect()

    customer_query = Customer.objects.filter(id=customer_id)
    if customer_query.exists():
        customer = customer_query[0]
        account_info = account_details(customer)
        print(account_info)

        context = {
            'buyer': customer,
            'info': account_info,
            'admin_account_info': admin_account_info,
            'redirect_url': redirect_url
        }
        return render(request, "admin_panel/single_buyer.html", context)

    return redirect("index")


def buyers(request):
    admin_account_info = get_admin_account_details()
    redirect_url = redirect_uri(request)

    all_customer = Customer.objects.all()
    context = {
        "all_customer": all_customer,
        'admin_account_info': admin_account_info,
        'redirect_url': redirect_url
    }
    return render(request, "admin_panel/buyer.html", context)


def index(request):
    admin_account_info = get_admin_account_details()
    redirect_url = redirect_uri(request)

    if request.user.is_authenticated and request.user.is_superuser:
        context = {
            'admin_account_info': admin_account_info,
            'redirect_url': redirect_url
        }
        context['all_business_requests'] = Business_Owner.objects.filter(
            status=0).count()
        return render(request, "admin_panel/panel-dashboard.html", context)

    return redirect("index")


def mark_as(request):
    output = {}
    if request.method == "GET" and request.is_ajax():
        Type = request.GET['type']
        Id = request.GET['id']

        try:
            if request.user.is_authenticated and request.user.is_superuser:
                focused_business_owner = Business_Owner.objects.get(id=int(Id))

                if Type == "approv":
                    focused_business_owner.status = 1
                elif Type == "reject":
                    focused_business_owner.status = -1

                focused_business_owner.save()
                output['status'] = True
            else:
                output['status'] = False
        except:
            output['status'] = False

        return JsonResponse(output)


def owner(request, owner_id):
    admin_account_info = get_admin_account_details()
    redirect_url = redirect_uri(request)

    # return redirect()
    owner_query = Business_Owner.objects.filter(id=owner_id)
    if owner_query.exists():
        owner = owner_query[0]

        business_list = Business.objects.filter(super_owner=owner)

        # account_info = account_details(customer)
        context = {
            'owner': owner,
            # 'info': account_info,
            'all_business': business_list,
            'admin_account_info': admin_account_info,
            'redirect_url': redirect_url
        }

        # print(context['admin_account_info'])
        return render(request, "admin_panel/single_owner.html", context)

    return redirect("index")


def owners(request):
    admin_account_info = get_admin_account_details()
    redirect_url = redirect_uri(request)

    context = {
        'admin_account_info': admin_account_info,
        'redirect_url': redirect_url
    }

    context['all_approved'] = Business_Owner.objects.filter(status=1)
    context['all_approved_count'] = context['all_approved'].count()

    context['all_rejected'] = Business_Owner.objects.filter(status=-1)
    context['all_rejected_count'] = context['all_rejected'].count()

    context['all_pending'] = Business_Owner.objects.filter(status=0)
    context['all_pending_count'] = context['all_pending'].count()

    return render(request, "admin_panel/owners.html", context)
