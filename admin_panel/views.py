from json.decoder import JSONDecodeError
from re import S
from django.db.models.query import prefetch_related_objects
from application.views import login
import builtins
from django.core.checks import messages
from django.db.models.expressions import Value
from django.shortcuts import render, redirect
from application.models import *
from django.http import JsonResponse
import json
from django.db.models import Q
from user_panel.supporting_func import *
from admin_panel.supporting_func import *
from application.supporting_func import *
from django.db.models import Sum, Case, When
from django.urls import resolve
from django.contrib import messages
from django.db import connection


def selected_receiver(request):
    output = {
        'names': None
    }
    notification = request.GET.get("notification")
    receiver_list = get_user_objects(json.loads(notification))
    output['names'] = receiver_list[0]
    return JsonResponse(output)


def send_general_notification(request):
    output = {
        'status': False,
        'message': ""
    }

    try:
        notification = request.GET.get("notification")
        notification = json.loads(notification)
        receiver = notification['receiver']
        receiver_list = get_user_objects(receiver)

        # new notification
        new_notification = Notification(
            title=notification['subject'],
            TYPE=3,
            content=notification['body']
        )
        new_notification.save()

        for single_receiver in receiver_list[1]:
            new_notification.general_receivers.create(
                user=single_receiver
            )
        output['status'] = True
        output['message'] = "Notification has been sent successfully!"

    except Exception as e:
        output['message'] = str(e)

    return JsonResponse(output)


def change_member_info(request):
    output = {
        'status': False,
        'message': 'Something went wrong!',
        'to_show': False
    }
    try:
        if request.method == "GET" and request.is_ajax():
            id_list = my_membership_level = block_status = None
            if 'id_list' in request.GET:
                id_list = request.GET['id_list']
                id_list = json.loads(id_list)
                if len(id_list) > 1:
                    output['to_show'] = True
                    output['message'] = "Values have been updated successfully!"
                else:
                    output['message'] = "Info updated successfully!"

            if 'membership_level' in request.GET:
                my_membership_level = request.GET['membership_level']

            if 'block_status' in request.GET:
                block_status = request.GET['block_status']

            if id_list:
                # Select relavent members
                filtered_members = Customer.objects.filter(pk__in=id_list)

                if my_membership_level:
                    my_membership_level = int(my_membership_level)
                    filtered_members.update(
                        membership_level=my_membership_level)

                if block_status:
                    block_status = True if block_status == "true" else False
                    filtered_members.update(is_block=block_status)

                output['status'] = True
    except:
        output = output

    return JsonResponse(output)


def whole_submit_member(request):
    pass


def reset_db(request):
    l = [Distribution, Notification, PointTransaction,
         Points_owe, Transaction, Transfer]
    for i in l:
        i.objects.all().delete()
    return redirect("index")


def all_listings(request):
    admin_account_info = get_admin_account_details()
    redirect_url = redirect_uri(request)

    if request.method == "GET" and "query" in request.GET:
        query = request.GET['query']

        if query.isnumeric() and len(query) < 9:
            results = Business.objects.filter(id=query)
        else:
            results = Business.objects.filter(
                Q(title_name__contains=query) | Q(organization_no__contains=query) | Q(email_address__contains=query) | Q(phone_number__contains=query))

        print(results)
        my_all_businesses = results

    else:
        my_all_businesses = Business.objects.all()

    context = {
        'is_listing': True,
        'admin_account_info': admin_account_info,
        'redirect_url': redirect_url,
        'all_business': my_all_businesses
    }

    return render(request, "admin_panel/all_listing.html", context)


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


def particular_business_2(request, business_name):
    focused_business = business_name.split("-")[-1]
    try:
        focused_business_id = int(focused_business)
        if Business.objects.filter(id=focused_business_id).exists():
            focused_business_object = Business.objects.get(
                id=focused_business_id)
            context = {
                "business": focused_business_object,
            }

            new_view = BusinessView(business_id=focused_business_id)
            new_view.save()
            return render(request, "single-business.html", context)
        else:
            return redirect("index")
    except:
        return redirect("index")


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
        'redirect_url': redirect_url,
        'membership_level_list': [5, 10, 15, 20, 25]
    }
    return render(request, "admin_panel/buyer.html", context)


def create_notification(request):
    admin_account_info = get_admin_account_details()
    redirect_url = redirect_uri(request)

    if request.user.is_authenticated and request.user.is_superuser:
        context = {
            'admin_account_info': admin_account_info,
            'redirect_url': redirect_url
        }
        context['listing'] = get_listing_summary()
        context['visibility'] = get_views_reviews()
        context['all_business_requests'] = Business_Owner.objects.filter(
            status=0).count()

        # Fetch all customers
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, user_first_name, user_last_name, user_email, 'user' AS my_status FROM application_customer;")
        customer_data = cursor.fetchall()
        cursor.close()

        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, owner_first_name, owner_last_name, business_email, 'owner' AS my_status FROM application_Business_Owner where status=1;")
        business_owner_data = cursor.fetchall()
        cursor.close()

        print(json.dumps(business_owner_data))
        print("=====")
        print(json.dumps(customer_data))

        context['all_business_owners'] = list(
            map(lambda single_owner: list(single_owner), business_owner_data)
        )
        context['all_members'] = list(
            map(lambda single_customer: list(single_customer), customer_data)
        )
        return render(request, "admin_panel/notifications.html", context)

    return redirect("index")


def index(request):
    admin_account_info = get_admin_account_details()
    redirect_url = redirect_uri(request)

    if request.user.is_authenticated and request.user.is_superuser:
        context = {
            'admin_account_info': admin_account_info,
            'redirect_url': redirect_url
        }
        context['listing'] = get_listing_summary()
        context['visibility'] = get_views_reviews()
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
