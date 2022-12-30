from django.urls import path
from base import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.ProductView.as_view(),name='index'),
    path('product-detail/<int:pk>/', views.Product_detail.as_view(), name='product-detail'),
    path('cart/',views.show_cart,name='showcart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/',views.mobile,name='mobiledata'),
    path('checkout/', views.checkout, name='checkout'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
