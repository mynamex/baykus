# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path


from .views import home, createApart, aparts, ApartmentsView, DevicesView, RoleView, Apis

# app_name = "home"

urlpatterns = [
    # The home page
    path('', home, name='home'),
    path('create_apart/', createApart, name="create_apart"),
    path('aparts/<str:pk_apart>/', aparts, name="aparts"),

    path('apartments_view/', ApartmentsView.as_view(), name="apartments_view"),

    path('devices_view/', DevicesView.as_view(), name="devices_view"),

    path('role_view/', RoleView.as_view(), name="role_view"),

    path('apis/', Apis, name="apis"),


]
