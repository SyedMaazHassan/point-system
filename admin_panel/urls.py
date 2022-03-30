from os import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name=""),
    path('owners', views.owners, name="owners"),
    path('owners/<owner_id>', views.owner, name="owners"),
    path('buyers', views.buyers, name="buyers"),
    path('buyers/<customer_id>', views.buyer, name="buyers"),
    path('mark_as', views.mark_as, name="mark_as"),
    path('add-admin-points', views.add_admin_points, name="add-admin-points"),
    path('business/<business_name>', views.particular_business_2, name="business"),
    path('get_customer_list', views.get_customer_list, name="get_customer_list"),
    path('send_points', views.send_points, name="send_points"),
    path('overall-business', views.all_businesses, name="overall-business"),
    path('reset-db', views.reset_db, name="reset-db"),
    path('all-listings', views.all_listings, name="all-listings"),
    path('whole-submit-member', views.whole_submit_member,
         name="whole-submit-member"),
    path('change-member-info', views.change_member_info, name="change-member-info"),
    path('create-notification', views.create_notification,
         name="create-notification"),
    path('selected_receiver', views.selected_receiver, name="selected_receiver"),
    path('send_general_notification', views.send_general_notification,
         name="send_general_notification")
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
