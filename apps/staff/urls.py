from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path

from apps.staff.views import (customer,
                              editCustomerInfo, createCustomer,
                              ShowCampus, showApartments, StaffCampusView,
                              customerUsers, CustUsersView, DevicesView)

app_name = "staff_me"

urlpatterns = [

    path('create_customer/', createCustomer, name="create_customer"),
    path('edit_customer_info/<str:pk_test>/', editCustomerInfo, name="edit_customer_info"),
    path('customer/<str:pk_customer>/', customer, name="customer"),

    # show
    path('customer_users/<str:pk_customer>/', customerUsers, name="customer_users"),

    path('show_campus/<str:pk_customer>/', ShowCampus, name="show_campus"),


    path('show_apartments/<str:pk_customer>/', showApartments, name="show_apartments"),


    path('cust_users_view/', CustUsersView.as_view(), name="cust_users_view"),

    path('devices_view/', DevicesView.as_view(), name="devices_view"),


    path('staff_campus_view/', StaffCampusView.as_view(), name="staff_campus_view"),


]
