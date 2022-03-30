from django.urls import resolve
from application.models import *
from user_panel.supporting_func import *
import json
from django.db.models import Sum, Case, When


def redirect_uri(request):
    current_url = resolve(request.path_info).url_name
    source = "/admin-panel/"
    return source + current_url


def get_admin_account_details():
    admin_account = Account.objects.get(is_admin=True)
    return account_details(None, True)


def get_listing_summary():
    all_listing = Business.objects.all()
    invisible_listing = all_listing.filter(status=0)
    pending_listing = all_listing.filter(status=1)
    active_listing = all_listing.filter(status=2)
    return {
        'all': all_listing.count(),
        'invisible': invisible_listing.count(),
        'pending': pending_listing.count(),
        'active': active_listing.count(),
    }


def get_views_reviews():
    all_views = BusinessView.objects.all()
    all_reviews = 0
    all_bookmarked = 0
    return {
        'views': all_views.count(),
        'reviews': all_reviews,
        'bookmarked': all_bookmarked
    }


def get_user_objects(notification):
    # print(notification)
    source = []
    receiver_list = []
    if notification['quantity'] == "all":
        selected_businesses_owners = Business_Owner.objects.all()
        selected_customers = Customer.objects.all()
    else:
        owner_list = notification['selected_receiver']['owner']
        preserved = Case(*[When(pk=pk, then=pos)
                           for pos, pk in enumerate(owner_list)])
        selected_businesses_owners = Business_Owner.objects.filter(
            pk__in=owner_list).order_by(preserved)

        user_list = notification['selected_receiver']['user']
        preserved = Case(*[When(pk=pk, then=pos)
                           for pos, pk in enumerate(user_list)])
        selected_customers = Customer.objects.filter(
            pk__in=user_list).order_by(preserved)

    source = list(selected_businesses_owners) + list(selected_customers)
    names = []
    receiver_list = []

    for i in source:
        names.append(i.user.first_name + ' ' + i.user.last_name)
        receiver_list.append(i.user)

    return (names, receiver_list)
