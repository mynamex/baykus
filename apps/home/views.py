# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from apps.accounts.models import Account
from apps.customauth.models import MyUser
from utils.decarator import cust_admin_only
from utils.query_debuger import query_debugger

my_decorators = [query_debugger, cust_admin_only, login_required(login_url='login')]


def is_true_or_false(val):
    if val == "false":
        return False
    elif val == "true":
        return True


def is_NONE(val):
    if val is None:
        return False
    else:
        return True


# @method_decorator(my_decorators, name='dispatch')
@query_debugger
@login_required(login_url='auth:login')
def home(request):
    user = MyUser.objects.select_related("account").get(username=request.user)
    context = {"segment": "home", "customer": Account.objects.get(id=user.account_id, license_status=True)}
    html_template = loader.get_template('cust_users/cust-index.html')
    return HttpResponse(html_template.render(context, request))

    # if user.is_person:
    #     # context = get_cust_customer_detail(request.user.pk)
    #
    #     context = {"segment": "home", "customer": Account.objects.get(id=user.account_id, license_status=True)}
    #     html_template = loader.get_template('cust_users/cust-index.html')
    #     return HttpResponse(html_template.render(context, request))
    #
    # elif not user.is_person:
    #     html_template = loader.get_template('home/page-no-official-user.html')
    #     return HttpResponse(html_template.render({"context": "siz bir ofis görevlisi değilsiniz !"}, request))


