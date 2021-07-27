from application.models import *
from django.db.models import Sum


def get_account_credit_details(account_object):
    return {
        'credit': 0,
        'debit': 0,
        'net': 0
    }


def account_details_wrt_business(customer, business):
    customer_account = Account.objects.get(is_customer=customer)
    business_account = Account.objects.get(is_business=business)
    total_get = total_consumed = 0

    filtered_credit_query = PointTransaction.objects.filter(
        FROM=business_account, TO=customer_account)
    if filtered_credit_query.exists():
        total_get = filtered_credit_query.aggregate(Sum('points'))[
            'points__sum']

    filtered_debit_query = PointTransaction.objects.filter(
        FROM=customer_account, TO=business_account)
    if filtered_debit_query.exists():
        total_consumed = filtered_debit_query.aggregate(Sum('points'))[
            'points__sum']

    return {
        'membership_level': customer.membership_level,
        'total_balance': round(total_get - total_consumed, 2)
    }


def account_details(customer_object, is_admin=False):

    if is_admin:
        account = Account.objects.get(is_admin=True)
    else:
        account = Account.objects.get(is_customer=customer_object)
    filtered_records = Transfer.objects.filter(account=account)
    total_reward = total_points_owe = total_debit = total_credit = total_balance = 0

    if filtered_records.exists():
        total_debit = filtered_records.aggregate(Sum('debit'))['debit__sum']
        total_credit = filtered_records.aggregate(Sum('credit'))['credit__sum']
        # print(total_debit, total_credit)
        total_balance = total_credit - total_debit

    account_info = {
        # 'account_id': account.id,
        # 'customer_name': f'{customer_object.user_first_name} {customer_object.user_last_name}',
        # 'created_at': account.created_at,
        'total_debit': round(total_debit, 2),
        'total_credit': round(total_credit, 2),
        'total_balance': round(total_balance, 2),
    }

    if not is_admin:
        filtered_points_owe = Points_owe.objects.filter(
            customer=customer_object)
        if filtered_points_owe.exists():
            total_reward = filtered_points_owe.aggregate(Sum('credit'))[
                'credit__sum']

        total_points_owe = total_reward - total_balance

        account_info['membership_level'] = customer_object.membership_level
        account_info['total_points_owe'] = round(total_points_owe, 2)
        account_info['total_reward'] = round(total_reward, 2)

    # print(account_info)
    return account_info
