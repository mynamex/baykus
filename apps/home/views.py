# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import datetime
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.accounts.models import Account, Apartments
from apps.customauth.models import MyUser
from apps.home.form import CreateApartments
from apps.home.serializer import ApartmentsSerializer, DevicesSerializer, ApartmentsSerializerCustomer
from django.db import IntegrityError, transaction

from utils.query_debuger import query_debugger

my_decorators = [query_debugger, login_required(login_url='login')]


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
    if user.is_salesman:
        accounts = Account.objects.all()
        date_now = datetime.datetime.now()
        context = {
            "segment": "index",
            "date_now": date_now,
            'customers': accounts,
            'customers_count': len(accounts)}

        html_template = loader.get_template('staff/staff-index.html')
        return HttpResponse(html_template.render(context, request))

    elif user:
        # context = get_cust_customer_detail(request.user.pk)

        context = {"segment": "home", "customer": Account.objects.get(id=user.account_id, license_status=True)}
        html_template = loader.get_template('cust_users/cust-index.html')
        return HttpResponse(html_template.render(context, request))

    elif not user.is_person:
        html_template = loader.get_template('home/page-no-official-user.html')
        return HttpResponse(html_template.render({"context": "siz bir ofis görevlisi değilsiniz !"}, request))


@query_debugger
@login_required(login_url='auth:login')
def aparts(request, pk_customer):
    account = Account.objects.get(pk=request.POST.get('account_id'))
    apartments = Apartments.objects.get(account=account)
    context = {
        'account': account,
        "apartments": apartments
    }
    return render(request, 'staff/customer_temp/customer.html', context)


@query_debugger
@login_required(login_url='auth:login')
def getApartments(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:

        if request.method == 'GET':
            user = MyUser.objects.select_related("account").get(username=request.user.username)

            apartments = list(
                Apartments.objects.filter(account=user.account, is_active=True).order_by(
                    'name').values("id", "name"))
            return JsonResponse({"success": True, 'apartments': apartments})
        if request.method == 'POST':
            data = json.load(request)
            todo = data.get('payload')
            # Todo.objects.create(task=todo['task'], completed=todo['completed'])
            return JsonResponse({'status': 'Todo added!'})

        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


@login_required(login_url='auth:login')
def custWatch(request):
    user = MyUser.objects.select_related("account").get(pk=request.user.pk)
    context = {}
    apartment = Apartments.objects.filter(account=user.account, is_active=True)

    context["customer"] = Account.objects.get(pk=user.account_id)
    context["segment"] = "watch"
    context["d_apartments"] = ApartmentsSerializerCustomer(apartment, many=True).data
    context["first_id"] = apartment[0].pk
    context["go_ask_date"] = apartment[0].go_ask_date

    context["d_devices"] = DevicesSerializer(apartment[0].devices.all().filter(is_active=True).order_by('device_type','name'), many=True).data
    return render(request, 'cust_users/watch/cust-watch.html', context)


@method_decorator(my_decorators, name='dispatch')
class WatchCampus(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apartment = None
        self.success = True
        self.data = {"desc": ""}
        self.user = None

    def get(self, request):

        try:
            apartment = Apartments.objects.get(account=request.GET.get("account_id", None),
                                               pk=request.GET.get("ap_id", None))

            self.data["d_data"] = DevicesSerializer(apartment.devices.all().order_by('device_type', 'name'), many=True).data

        except Apartments.DoesNotExist:
            self.data["desc"] = "Yerleşke Bulunamadı"
            self.success = False

        except Exception as err:
            self.data["desc"] = str(err)
            self.success = False

        return JsonResponse({"success": self.success, "data": self.data})

    def post(self, request):

        try:
            with transaction.atomic():
                apartment = Apartments.objects.get(pk=request.POST.get("ap_id", None), is_active=True)
                self.data["go_ask_date"] = apartment.go_ask_date

                if request.POST.get("in_go") == "go_get":
                    self.data["d_data"] = DevicesSerializer(apartment.devices.all().filter(is_active=True).order_by('device_type', 'name'), many=True).data

                elif request.POST.get("in_go") == "go_order":
                    device = apartment.devices.get(pk=self.request.POST.get("device_id", ""))
                    if device.status:
                        device.status = False
                        self.data["desc"] = "{} kapatıldı".format(device.name)
                    else:
                        device.status = True
                        self.data["desc"] = "{} açıldı".format(device.name)
                    device.save()

                    self.data["d_data"] = DevicesSerializer(apartment.devices.all().filter(is_active=True).order_by('device_type', 'name'),  many=True).data

                elif request.POST.get("in_go") == "update":
                    ap = apartment.device.get(pk=request.POST.get("dev_id", None))

                    ap.name = eD(self.request.POST.get("name", ""))
                    ap.key = self.request.POST.get("key", "")
                    ap.device_type = self.request.POST.get("device_type", "")
                    ap.status = is_true_or_false(request.POST.get("status", None))
                    ap.is_active = is_true_or_false(request.POST.get("is_active", None))
                    ap.save()
                    apartment.save()
                    self.data["desc"] = "cihaz güncellendi"

                elif request.POST.get("in_go") == "create":

                    self.data["desc"] = "Yeni bir cihaz yaratıldı"
                    self.data["new_devices_id"] = None


        except IntegrityError as e:
            if str(e).__contains__("UNIQUE"):
                if str(e).__contains__("accounts_device.key"):
                    self.data["desc"] = "Bu key kullanılıyor"
                elif str(e).__contains__("accounts_device.name"):
                    self.data["desc"] = "Bu cihaz adı kullanılıyor"
                else:
                    self.data["desc"] = "Zaten var" + str(e)
            else:
                self.data["desc"] = str(e)

            self.success = False

        except Exception as err:
            self.data["desc"] = str(err)
            self.success = False

        return JsonResponse({"success": self.success, "data": self.data})


def eD(val):
    return str(val).strip().lower()


@csrf_exempt
def Apis(request):
    print("----------", request.headers["Api-Key"])
    print("----------", request.headers["Data"])

    return JsonResponse(
        {"result": False, "karagoz": "134t"}, safe=False)
