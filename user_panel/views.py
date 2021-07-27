from django.shortcuts import render, redirect
# from django.db import models
from django.contrib import messages
from application.models import *
from django.http import JsonResponse
from application.supporting_func import *
from datetime import datetime
from user_panel.supporting_func import *


def notifications(request):
    status_only = get_user_status_only(request.user)
    status_object = get_user_status(request.user)

    if status_only == "user":
        all_notification = list(Notification.objects.filter(
            cust_receiver=status_object).order_by("-id"))
    if status_only == "business_owner":
        all_notification = list(Notification.objects.filter(
            owner_receiver=status_object).order_by("-id"))

    context = {
        'all_notifications': all_notification,
        'user_status': get_user_status_only(request.user),
        'business_owner_details': status_object
    }

    if status_only == "user":
        Notification.objects.filter(
            cust_receiver=status_object).update(is_read=True)
    if status_only == "business_owner":
        Notification.objects.filter(
            owner_receiver=status_object).update(is_read=True)

    return render(request, "notification.html", context)


# render add listing page
def add_listing_page(request):

    if not request.user.is_authenticated:
        return redirect("login")

    context = {
        'user_status': get_user_status_only(request.user)
    }

    if Business_Owner.objects.filter(user=request.user).exists():
        context['business_owner_details'] = Business_Owner.objects.get(
            user=request.user)
        context['features'] = Business_Feature.objects.all()
        context['categories'] = Business_Category.objects.all()
    else:
        return redirect("index")

    return render(request, "add-listing.html", context)


# Create your views here.
def index(request):

    if not request.user.is_authenticated:
        return redirect("login")

    context = {
        'user_status': get_user_status_only(request.user)
    }

    if Business_Owner.objects.filter(user=request.user).exists():
        context['business_owner_details'] = Business_Owner.objects.get(
            user=request.user)
        context['features'] = Business_Feature.objects.all()
        context['categories'] = Business_Category.objects.all()

    print(context['user_status'])
    if context['user_status'] == "user":
        template = "buyer/dashboard.html"
        focused_customer = get_user_status(request.user)
        account = Account.objects.get(is_customer=focused_customer)
        account_info = account_details(focused_customer)
        context['account_details'] = account_info
        context['info'] = account_info

    else:
        template = "seller/dashboard.html"

    return render(request, template, context)


def particular_business(request, business_name):
    focused_business = business_name.split("-")[-1]
    try:
        focused_business_id = int(focused_business)
        if Business.objects.filter(id=focused_business_id).exists():
            focused_business_object = Business.objects.get(
                id=focused_business_id)
            context = {
                "business": focused_business_object,
                "business_owner_details": get_user_status(request.user),
                'user_status': get_user_status_only(request.user),
                "timestamp": datetime.now()
            }
            return render(request, "single-business.html", context)
        else:
            return redirect("index")
    except:
        return redirect("index")


def my_businesses(request):
    if not (request.user.is_authenticated and Business_Owner.objects.filter(user=request.user).exists()):
        return redirect("index")

    context = {'user_status': get_user_status_only(request.user),
               'business_owner_details': get_user_status(request.user)}
    list_of_my_business = Business.objects.filter(
        super_owner=context['business_owner_details'])
    context['all_businesses'] = list_of_my_business
    context['page_title'] = "My business"
    return render(request, "my-business-list.html", context)


def all_businesses(request):
    context = {'user_status': get_user_status_only(request.user),
               'business_owner_details': get_user_status(request.user)}
    list_of_my_business = Business.objects.all()
    context['all_businesses'] = list_of_my_business
    context['page_title'] = "All Business"
    return render(request, "my-business-list.html", context)


def create_business(request):
    if not request.user.is_authenticated:
        return redirect("index")

    context = {
        'user_status': get_user_status_only(request.user)
    }

    if request.method == "POST":
        # tempdesc = request.POST['tempdesc']
        bannerImage = request.FILES['bannerImage']
        titleName = request.POST['titleName']
        description = request.POST['description']
        selectedcategory = request.POST['selectedcategory']
        emailAddress = request.POST['emailAddress']
        phoneNumber = request.POST['phoneNumber']
        address = request.POST['address']
        selectedFeatures = request.POST['selectedFeatures']
        websiteLink = request.POST['websiteLink']

        isAnyEmpty = False

        for i, j in request.POST.items():
            print(i, "=>", j)
            if len(str(j)) == 0:
                isAnyEmpty = True

        return redirect("index")

        if isAnyEmpty:
            messages.error(
                request, "Kindly fill out all fields to create the business!")
            return redirect("index")

        new_business = Business(
            super_owner=Business_Owner.objects.get(user=request.user),
            title_name=titleName,
            banner_image=bannerImage,
            categories=selectedcategory,
            description=description,
            features=selectedFeatures,
            written_address=address,
            phone_number=phoneNumber,
            email_address=emailAddress,
            website_link=websiteLink
        )

        new_business.save()

        messages.info(request, "Business has been created successfully!")

    return redirect("index")


# Point system
def purchase_history(request):
    context = {}
    if request.user.is_authenticated:
        user_status = get_user_status_only(request.user)
        user_object = get_user_status(request.user)
        context['user_status'] = user_status
        context['business_owner_details'] = user_object

        if user_status == "user":
            not_exist_msg = "You haven't purchase anything from here!"
            business_list = []
            all_transactions = Transaction.objects.filter(
                customer=user_object
            ).order_by("-id")
            for transaction in all_transactions:
                if transaction.business not in business_list:
                    business_list.append(transaction.business)

            context['all_businesses'] = business_list
        else:
            not_exist_msg = "This business has no transaction yet!"
            all_business = Business.objects.filter(super_owner=user_object)
            context['all_businesses'] = all_business

        if request.method == "GET" and 'selected_business' in request.GET:
            selected_business = request.GET['selected_business']
            business = Business.objects.filter(id=selected_business)
            if business.exists():
                business = business[0]

                if user_status == "user":
                    all_transactions = all_transactions.filter(
                        customer=user_object, business=business).order_by("-id")
                else:
                    all_transactions = Transaction.objects.filter(
                        business=business,
                    ).order_by("-id")

                context['business'] = business
                if all_transactions.exists():
                    context['all_transactions'] = all_transactions
                else:
                    context['message'] = not_exist_msg
            else:
                context['message'] = "Invalid business selected!"

    return render(request, "purchase-history.html", context)


def get_user(request):
    output = {'result': False}
    if request.method == "GET" and request.is_ajax():
        customer_id = request.GET['customer_id']
        business_id = request.GET['business_id']
        try:
            customer_id = int(customer_id)
            customer = Customer.objects.filter(id=customer_id)
            business = Business.objects.filter(id=business_id)
            if customer.exists() and business.exists():
                customer = customer[0]
                business = business[0]
                account_info = account_details_wrt_business(customer, business)

                output['result'] = {
                    'name': f'{customer.user_first_name} {customer.user_last_name}',
                    'account_info': account_info
                }
        except:
            print(output)

    return JsonResponse(output)


def add_new_transaction(request):
    output = {'result': False}
    if request.method == "GET" and request.is_ajax():
        customer_id = int(request.GET['customer_id'])
        price = float(request.GET['price'])
        receipt = request.GET['receipt']
        business_id = int(request.GET['business_id'])

        via_money = float(request.GET['via_money'])
        via_points = float(request.GET['via_points'])

        customer = Customer.objects.get(id=customer_id)
        added_by = request.user
        business = Business.objects.get(id=business_id)

        reward_points = (via_money / 100) * customer.membership_level
        reward_points = round(reward_points, 2)

        if Transaction.objects.filter(receipt=receipt, business=business).exists():
            output['msg'] = "This receipt already exists in this business"
        else:
            # Add new transaction
            new_transaction = Transaction(
                customer=customer,
                price=price,
                receipt=receipt,
                business=business,
                via_money=via_money,
                via_points=via_points,
                current_membership_level=customer.membership_level,
                added_by=added_by
            )
            new_transaction.save()

            if via_points > 0:
                # FROM customer to business
                FROM = Account.objects.get(is_customer=customer)
                TO = Account.objects.get(is_business=business)
                new_points_transaction = PointTransaction(
                    FROM=FROM,
                    TO=TO,
                    points=via_points
                )
                new_points_transaction.save()
                new_points_transaction.execute()

                # FROm customer to ADMIN
                FROM = Account.objects.get(is_business=business)
                TO = Account.objects.get(is_admin=True)
                new_points_transaction = PointTransaction(
                    FROM=FROM,
                    TO=TO,
                    points=via_points
                )
                new_points_transaction.save()
                new_points_transaction.execute()

            # charge account for owe reward points
            new_points_owe = Points_owe(
                credit=reward_points,
                transaction_source=new_transaction,
                customer=customer
            )
            new_points_owe.save()

            new_notification = Notification(
                cust_receiver=customer
            )
            new_notification.notify_for_reward(
                no_of_points=reward_points,
                price=price,
                business_name=business.title_name
            )

            output['result'] = True

    return JsonResponse(output)
