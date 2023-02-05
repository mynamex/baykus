import random

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db import transaction

from apps.accounts.models import Account, Gates, Blocks
from apps.customauth.models import MyUser
from apps.users.models import Apartments

User = get_user_model()


class Command(BaseCommand):
    help = "Creates customer or regular user"

    # def add_arguments(self, parser):
    #     parser.add_argument("total", type=int, help="How many users will be created")
    list_rakam = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    list_rakam_salesman_id = [0, 1, 2, 3, 4]

    def handle(self, *args, **kwargs):

        test_add_path = r"C:\Users\zen_win\Documents\call_center_backend\backend\helper\test_add_temp"

        filepath_names = test_add_path + "/temp_names.txt"
        filepath_last_names = test_add_path + "/temp_lastnames.txt"

        a_last_name = []
        a_name = []
        salesman_id = 1

        with open(filepath_last_names, encoding="utf8") as row:
            for line in row:
                a_last_name.append(str(line).strip())

        a_salesman_names = ["hakan", "sezgin", "fatih", "osman", "gündüz"]

        a_gate_names = ["ana", "ön", "arka", "üst", "doğu", "batı", "kuzey", "güney"]

        try:
            User.objects.get(pk=2)
        except User.DoesNotExist:
            for j, i in enumerate(a_salesman_names):
                User.objects.create_salesmanuser(username=str(i),
                                                 # name=str(i + " pazarlama"),
                                                 password="lola12345")

        with open(filepath_names, encoding="utf8") as row:
            for line in row:
                a_name.append(str(line).strip())

        try:
            for j, i in enumerate(a_name):
                if j > 10:
                    break
                site_name = str(i).strip() + " sitesi"

                try:
                    Account.objects.get(site_name=site_name)
                    continue
                except Account.DoesNotExist:
                    pass

                with transaction.atomic():

                    if j % 10 == 0:
                        if salesman_id < 6:
                            salesman_id += 1

                    # new_tax = tax+j
                    ac = Account.objects.create(
                        site_name=site_name,
                        tax_number=self.get_random_tax_no(),
                        site_phone1=self.get_random_phone(),
                        site_address=site_name + "falan mah falan sok falan no 22",
                        related_person_name=site_name + " bey",
                        salesman_id=salesman_id)

                    ac_pk = ac.pk

                    for k in range(0, 5):
                        user_or_staff = "user"
                        is_staff = False
                        if k > 3:
                            is_staff = True
                            user_or_staff = "staff"
                        user = MyUser.objects.create(username="{}{}{}".format(str(i).strip(), user_or_staff, k),
                                                     account_id=ac_pk,
                                                     is_person=is_staff,
                                                     name="{} falan".format(site_name),
                                                     )

                        user.set_password("lola12345")
                        user.save()

                    for gate in a_gate_names:
                        Gates.objects.create(account_id=ac_pk,
                                             gate_name="{} kapı {}".format(gate, ac_pk),
                                             module_type_id=random.choice([1, 2]))

                    for block in range(0, 5):
                        bl = Blocks.objects.create(account=ac,
                                                   name="{}.b {}.ac".format(block, ac.pk))

                        for daire in range(0, 20):
                            Apartments.objects.create(account=ac,
                                                      block=bl,
                                                      name="{}.d {}.b {}.ac".format(daire, block, ac.pk))

                    self.stdout.write(self.style.SUCCESS(f"{i.__str__()} created"))
        except Exception as err:
            print(err)

    def get_random_tax_no(self):
        tax = "{}{}{}{}{}{}{}{}{}{}{}".format(random.choice(range(2, 6)),
                                              random.choice(self.list_rakam),
                                              random.choice(self.list_rakam),
                                              random.choice(self.list_rakam),
                                              random.choice(self.list_rakam),
                                              random.choice(self.list_rakam),
                                              random.choice(self.list_rakam),
                                              random.choice(self.list_rakam),
                                              random.choice(self.list_rakam),
                                              random.choice(self.list_rakam),
                                              random.choice(self.list_rakam))

        return tax

    def get_random_phone(self):
        tel = "053{}{}{}{}{}{}{}{}".format(random.choice(range(2, 6)),
                                           random.choice(self.list_rakam),
                                           random.choice(self.list_rakam),
                                           random.choice(self.list_rakam),
                                           random.choice(self.list_rakam),
                                           random.choice(self.list_rakam),
                                           random.choice(self.list_rakam),
                                           random.choice(self.list_rakam))

        return tel

    # self.stdout.write(self.style.ERROR("lorem ipsum dolor."))
    #     self.stdout.write(self.style.NOTICE("lorem ipsum dolor."))
    #     self.stdout.write(self.style.SUCCESS("lorem ipsum dolor."))
    #     self.stdout.write(self.style.WARNING("lorem ipsum dolor."))
    #     self.stdout.write(self.style.SQL_FIELD("lorem ipsum dolor."))
    #     self.stdout.write(self.style.SQL_COLTYPE("lorem ipsum dolor."))
    #     self.stdout.write(self.style.SQL_KEYWORD("lorem ipsum dolor."))
    #     self.stdout.write(self.style.SQL_TABLE("lorem ipsum dolor."))
    #     self.stdout.write(self.style.HTTP_INFO("lorem ipsum dolor."))
    #     self.stdout.write(self.style.HTTP_SUCCESS("lorem ipsum dolor."))
    #     self.stdout.write(self.style.HTTP_NOT_MODIFIED("lorem ipsum dolor."))
    #     self.stdout.write(self.style.HTTP_REDIRECT("lorem ipsum dolor."))
    #     self.stdout.write(self.style.HTTP_NOT_FOUND("lorem ipsum dolor."))
    #     self.stdout.write(self.style.HTTP_BAD_REQUEST("lorem ipsum dolor."))
    #     self.stdout.write(self.style.HTTP_SERVER_ERROR("lorem ipsum dolor."))
    #     self.stdout.write(self.style.MIGRATE_HEADING("lorem ipsum dolor."))
    #     self.stdout.write(self.style.MIGRATE_LABEL("lorem ipsum dolor."))
