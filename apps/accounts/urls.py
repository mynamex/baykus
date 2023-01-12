
from django.urls import path
from apps.accounts.views import Get_account_info, Get_first_setup, Get_account_user_verify

urlpatterns = [

    path('get_account_info/', Get_account_info.as_view(), name='get_account_info'),
    path('get_first_setup/', Get_first_setup.as_view(), name='get_first_setup'),
    path('get_account_user_verify/', Get_account_user_verify.as_view(),
         name='get_account_user_verify'),
]


