from django.db import models
from datetime import datetime
import json
from django.contrib.auth.models import User, auth
from django.db import connection
from django.db.models import Sum
from django.db.models.base import ModelBase
from django.db.models.fields import related

# Create your models here.

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver


class Business_Owner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_first_name = models.CharField(max_length=50)
    owner_last_name = models.CharField(max_length=50)
    business_email = models.CharField(max_length=50)
    organization_no = models.CharField(max_length=11, default="None")
    business_telephone = models.CharField(max_length=50)
    status = models.IntegerField(default=0)
    registered_time = models.DateTimeField(default=datetime.now())
    profile_picture = models.ImageField(upload_to="business-owner", null=True)
    #  0 = unseen
    # -1 = rejected
    # 1 = approved

    def get_status(self):
        my_status_dict = {
            0: 'pending',
            -1: 'rejected',
            1: 'approved'
        }
        return my_status_dict[self.status]

    def option_to_create_business(self):
        if self.status == 1:
            if not Business.objects.filter(super_owner=self).exists():
                return True

        return False


class Business(models.Model):
    super_owner = models.ForeignKey(Business_Owner, on_delete=models.CASCADE)
    title_name = models.CharField(max_length=255)
    banner_image = models.ImageField(upload_to='banners')
    categories = models.TextField()
    description = models.TextField()
    features = models.TextField()
    organization_no = models.CharField(default="1541-4541", max_length=15)
    written_address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email_address = models.CharField(max_length=20)
    website_link = models.URLField(max_length=200)
    status = models.IntegerField(default=1)
    # 0 = invisible
    # 1 = pending
    # 2 = active

    def bubbleSort(self, arr):
        n = len(arr)

        # Traverse through all array elements
        for i in range(n):

            # Last i elements are already in place
            for j in range(0, n-i-1):

                # traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                if arr[j]['total_points_owe'] > arr[j+1]['total_points_owe']:
                    arr[j], arr[j+1] = arr[j+1], arr[j]

    def all_customers(self):
        output = {
            'business_name': self.title_name
        }
        customer_list = []
        total = 0

        all_customers = Transaction.objects.raw(
            f'SELECT * FROM application_transaction where business_id={self.id} group by customer_id')
        for cust in all_customers:
            individual_points = cust.customer.business_transaction_details(
                cust.business)
            total += individual_points

            if individual_points > 0:
                link_element = '''<a class='text-dark' href="admin-panel/buyers/'''+f'{cust.customer.id}'+'''" target="_blank">''' + \
                    f'{cust.customer.user_first_name} {cust.customer.user_last_name}' + '''</a>'''
                customer_dict = {
                    'id': cust.customer.id,
                    'name': link_element,
                    'total_points_owe': round(individual_points, 2)
                }
                customer_list.append(customer_dict)

        self.bubbleSort(customer_list)
        output['customer_list'] = customer_list
        output['total'] = round(total, 2)
        return output

        # all_transaction_query = Transaction.objects.filter(business = self)
        # for transaction in all_transaction_query:
        #     if transaction.customer not in customer_list

    # opening_hours = ....
    # questionnaire = ....
    # price range = ......
    # photo galler = .....

    def get_features(self):
        new_features = json.loads(self.features)
        new_features_list = list(
            map(lambda x: Business_Feature.objects.get(id=int(x)), new_features))
        return new_features_list

    def get_categories(self):
        new_categories = json.loads(self.categories)
        new_categories_list = list(
            map(lambda x: Business_Category.objects.get(id=int(x)), new_categories))
        return new_categories_list

    def link_name(self):
        new_name = self.title_name.replace(" ", "-")
        return new_name + f'-{self.id}'

    def wrapped_text(self, my_limit, text):
        if len(text) > my_limit:
            return text[0: my_limit] + "..."
        return text

    def wrapped_description(self):
        return self.wrapped_text(100, self.description)

    def wrapped_location(self):
        return self.wrapped_text(50, self.written_address)


class Social_media(models.Model):
    # social_media_link = models.TextField(null = True)
    pass


class Business_location(models.Model):
    # location_latitude = models.FloatField(null = True)
    # location_langitude = models.FloatField(null = True)
    pass


class Opening_Hours(models.Model):
    pass


class Questionnaire(models.Model):
    pass


class Price_Range(models.Model):
    pass


class Business_Category(models.Model):
    name = models.CharField(max_length=255)


class Business_Feature(models.Model):
    name = models.CharField(max_length=255)


class BusinessView(models.Model):
    business_id = models.IntegerField()


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_first_name = models.CharField(max_length=50)
    user_last_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    user_telephone = models.CharField(max_length=50)
    user_address = models.CharField(max_length=50)
    user_area_code = models.CharField(max_length=50)
    user_city = models.CharField(max_length=50)
    membership_level = models.IntegerField(default=5)
    registered_time = models.DateTimeField(default=datetime.now())
    is_block = models.BooleanField(default=0)

    def business_transaction_details(self, business):
        TOTAL_POINTS_WON = 0
        POINTS_ACHIEVED = 0
        all_points_get = Points_owe.objects.filter(customer=self)
        for single_point_owe in all_points_get:
            if single_point_owe.transaction_source.business == business:
                TOTAL_POINTS_WON += single_point_owe.credit

        sender_account = Account.objects.get(is_business=business)
        receiver_account = Account.objects.get(is_customer=self)
        filtered_records = PointTransaction.objects.filter(
            FROM=sender_account, TO=receiver_account)
        if filtered_records.exists():
            POINTS_ACHIEVED = filtered_records.aggregate(Sum('points'))[
                'points__sum']

        return TOTAL_POINTS_WON - POINTS_ACHIEVED


class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.FloatField()
    receipt = models.CharField(max_length=255)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    via_money = models.FloatField(default=0)
    via_points = models.FloatField(default=0)
    current_membership_level = models.IntegerField(default=5)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now())

    def __str__(self) -> str:
        return f'Price:{self.price}, Via money: {self.via_money}, Via points: {self.via_points}'

    def get_reward_points(self):
        reward_points = (self.via_money / 100) * self.current_membership_level
        reward_points = round(reward_points, 2)
        return reward_points


class Account(models.Model):
    is_customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True)
    is_business = models.ForeignKey(
        Business, on_delete=models.CASCADE, null=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def create_customer_account(self, customer_object):
        self.is_customer = customer_object
        self.save()

    def create_business_account(self, business_object):
        self.is_business = business_object
        self.save()

    def create_admin_account(self):
        self.is_admin = True
        self.save()


class Transfer(models.Model):

    debit = models.FloatField(default=0)
    credit = models.FloatField(default=0)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def charge_admin_account(self, quantity):
        admin_account = Account.objects.get(is_admin=True)
        self.account = admin_account
        self.credit = quantity
        self.save()


class Points_owe(models.Model):
    debit = models.FloatField(default=0)
    credit = models.FloatField(default=0)
    transaction_source = models.ForeignKey(
        Transaction, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class General_Receiver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)


class Notification(models.Model):
    title = models.CharField(max_length=100)
    TYPE = models.IntegerField(default=1)
    # type dict {
    #   1 = won points
    #   2 = congratz
    # }
    content = models.TextField()
    cust_receiver = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True)
    owner_receiver = models.ForeignKey(
        Business_Owner, on_delete=models.CASCADE, null=True)
    general_receivers = models.ManyToManyField(General_Receiver, null=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def notify_for_clearance(self, no_of_points, busineess_name):
        self.TYPE = 2
        self.title = "Points are available now!"
        self.content = f'Hi {self.cust_receiver.user_first_name}! <b>{round(no_of_points, 2)} points</b> have been cleared and available in your account. You can use these points in your next purchase from <b>{busineess_name}</b>!'
        self.save()

    def notify_for_reward(self, no_of_points, price, business_name):
        self.title = "You won points"
        self.content = f'<b>Congratulations!</b> you got <b>{round(no_of_points, 2)} FREE points</b> for your purchase of ${price} from <b>{business_name}</b>. You can use these points for your next purchase from this seller!'
        self.save()

    def get_icon(self):
        dictionary = {
            1: '''<img src="static/images/won.png" class="notification-icon" alt="">''',
            2: '''<img src="static/images/cong.png" class="notification-icon" alt="">''',
            3: '''<span class="material-icons mr-2">notifications</span>'''
        }
        return dictionary[self.TYPE]


class PointTransaction(models.Model):
    FROM = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="Sender")
    TO = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="Receiver")
    timestamp = models.DateTimeField(auto_now_add=True)
    points = models.FloatField()
    related_transfers = models.ManyToManyField(Transfer, null=True)

    def execute(self):
        # Adding debit transaction
        new_debit_transfer = Transfer(
            debit=self.points,
            account=self.FROM
        )
        new_debit_transfer.save()

        # adding credit transaction
        new_credit_transfer = Transfer(
            credit=self.points,
            account=self.TO
        )
        new_credit_transfer.save()

        # Registering into many to many field
        self.related_transfers.add(new_debit_transfer, new_credit_transfer)
        self.save()


class Distribution(models.Model):
    points_to_give = models.FloatField()
    individual_percent = models.FloatField(null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    transfers = models.ManyToManyField(PointTransaction, null=True)
    is_completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def amount(self, individual_customer_points):
        individual_percent_in_points = self.individual_percent / 100
        if 0 < individual_customer_points <= 1:
            points_customer_wil_get = individual_customer_points
        else:
            points_customer_wil_get = individual_percent_in_points * individual_customer_points
        return round(points_customer_wil_get, 2)

    def transfer_to_business(self):
        admin_account = Account.objects.get(is_admin=True)
        business_account = Account.objects.get(is_business=self.business)
        # Adding point transfer set
        new_point_transaction = PointTransaction(
            FROM=admin_account,
            TO=business_account,
            points=self.points_to_give
        )
        new_point_transaction.save()
        new_point_transaction.execute()

        # register this transfer set into transfer
        self.transfers.add(new_point_transaction)
        self.save()

    def run_now(self, point_to_distribute):
        print("====")
        print("RUNNING NOW")
        print("====")
        business_points_info = self.business.all_customers()
        individual_percent = (
            point_to_distribute / business_points_info['total']) * 100
        self.individual_percent = round(individual_percent, 2)
        for single_customer in business_points_info['customer_list']:
            if 0 < single_customer["total_points_owe"] <= 1:
                single_customer_points = self.amount(
                    single_customer["total_points_owe"])

                if single_customer["total_points_owe"] < single_customer_points:
                    single_customer_points -= single_customer_points - \
                        single_customer["total_points_owe"]

                string = f'{single_customer["name"]} has {single_customer["total_points_owe"]}, will get {self.individual_percent}% ({single_customer_points})'

                # Selet FROM and TO accounts
                business_account = Account.objects.get(
                    is_business=self.business)
                customer_account = Account.objects.get(
                    is_customer_id=single_customer['id'])

                # Adding point transfer set
                new_point_transaction = PointTransaction(
                    FROM=business_account,
                    TO=customer_account,
                    points=single_customer_points
                )
                new_point_transaction.save()
                new_point_transaction.execute()

                # register this transfer set into transfer
                self.transfers.add(new_point_transaction)

                # Send notification to customer
                this_customer_object = customer_account.is_customer
                new_notification = Notification(
                    cust_receiver=this_customer_object)
                new_notification.notify_for_clearance(
                    single_customer_points, self.business.title_name)

                print("====")
                print(string)
                point_to_distribute = point_to_distribute - single_customer_points
                print(f'Remaining: {point_to_distribute}')
                print("====")

        if point_to_distribute > 0:
            self.run_now_big(point_to_distribute)
        # print(point_to_distribute)

    def run_now_big(self, point_to_distribute):
        print("====")
        print("RUNNING NOW BIG")
        print("====")
        business_points_info = self.business.all_customers()
        individual_percent = (
            point_to_distribute / business_points_info['total']) * 100
        self.individual_percent = round(individual_percent, 2)

        for single_customer in business_points_info['customer_list']:
            if single_customer["total_points_owe"] > 1:
                single_customer_points = self.amount(
                    single_customer["total_points_owe"])

                if single_customer["total_points_owe"] < single_customer_points:
                    single_customer_points -= single_customer_points - \
                        single_customer["total_points_owe"]

                string = f'{single_customer["name"]} has {single_customer["total_points_owe"]}, will get {self.individual_percent}% ({single_customer_points})'

                # Selet FROM and TO accounts
                business_account = Account.objects.get(
                    is_business=self.business)
                customer_account = Account.objects.get(
                    is_customer_id=single_customer['id'])

                # Adding point transfer set
                new_point_transaction = PointTransaction(
                    FROM=business_account,
                    TO=customer_account,
                    points=single_customer_points
                )
                new_point_transaction.save()
                new_point_transaction.execute()

                # register this transfer set into transfer
                self.transfers.add(new_point_transaction)

                # Send notification to customer
                this_customer_object = customer_account.is_customer
                new_notification = Notification(
                    cust_receiver=this_customer_object)
                new_notification.notify_for_clearance(
                    single_customer_points, self.business.title_name)

                print("====")
                print(string)
                point_to_distribute = round(
                    point_to_distribute - single_customer_points, 2)
                print(f'Remaining: {point_to_distribute}')
                print("====")

        if point_to_distribute > 0:
            self.run_now_big(point_to_distribute)
