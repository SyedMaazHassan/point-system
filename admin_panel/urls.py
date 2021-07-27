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
    path('business', views.business, name="business"),
    path('get_customer_list', views.get_customer_list, name="get_customer_list"),
    path('send_points', views.send_points, name="send_points"),
    path('overall-business', views.all_businesses, name="overall-business")
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
