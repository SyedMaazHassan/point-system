from .models import *


def validate_org_no(number):
    status = True
    status = status and "-" in number
    if status:
        breaking = number.split("-")
        status = status and len(breaking[0]) == 6
        status = status and len(breaking[1]) == 4
        try:
            first_portion = int(breaking[0])
            status = status and True
        except:
            status = status and False

        try:
            second_portion = int(breaking[1])
            status = status and True
        except:
            status = status and False
        
    return status



def get_user_status(particular_user):
    if Business_Owner.objects.filter(user = particular_user).exists():
        return Business_Owner.objects.get(user = particular_user)
    else:
        return Customer.objects.get(user = particular_user)


def get_user_status_only(particular_user):
    if Business_Owner.objects.filter(user = particular_user).exists():
        return "business_owner"
    else:
        return "user"