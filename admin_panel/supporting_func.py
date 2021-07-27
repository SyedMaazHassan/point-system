from django.urls import resolve
from application.models import *
from user_panel.supporting_func import *


def redirect_uri(request):
    current_url = resolve(request.path_info).url_name
    source = "/admin-panel/"
    return source + current_url


def get_admin_account_details():
    admin_account = Account.objects.get(is_admin=True)
    return account_details(None, True)
