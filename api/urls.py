from django.urls import path
from .views import get_all_stock, get_all_users, get_all_oem, get_shop_orders, get_article, create_order, get_order_details, test_endpoint, add_user

urlpatterns = [
    # path('stock/', get_all_stock, name='get_all_stock'),
    # path('users/', get_all_users, name='get_all_users'),
    # path('oem/', get_all_oem, name='get_all_oem'),
    # path('shop-orders/', get_shop_orders, name='get_shop_orders'),
    path('get-article/', get_article, name='get_article'),
    path('create-order/', create_order, name='create_order'),
    path('order-details/', get_order_details, name='get_order_details'),
    path('test/', test_endpoint, name='test_endpoint'),
    path('add-user/', add_user, name='add_user'),
]