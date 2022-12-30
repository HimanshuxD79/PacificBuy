from django.urls import path 
from pacificAuth import views
urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.handlelogin,name='handlelogin'),
    path('logout/',views.handlelogout,name ='logout'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('request-reset-password/',views.RequestResetPassword.as_view(),name='request_reset_password'),
    path('set-new-password/<uidb64>/<token>',views.SetNewPassword.as_view(),name='set_new_password'),

]
