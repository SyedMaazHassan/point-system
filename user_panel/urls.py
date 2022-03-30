from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "user_panel"
urlpatterns = [
    path('', views.index, name=""),
    path('createBusiness', views.create_business, name="createBusiness"),
    path('my-businesses', views.my_businesses, name="my-businesses"),
    path('business/<business_name>', views.particular_business, name="business"),
    path('addListing', views.add_listing_page, name="addListing"),

    path('purchase-history', views.purchase_history, name="purchase-history"),
    path('get_user', views.get_user, name="get_user"),
    path('add_new_transaction', views.add_new_transaction,
         name="add_new_transaction"),
    path('notifications', views.notifications, name="notifications"),
    path('dashboard', views.index, name="dashboard"),
    path('all-business', views.all_businesses, name="all-business")

]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
