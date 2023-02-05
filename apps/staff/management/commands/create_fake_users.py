from django.core.management import BaseCommand
from django.db import transaction, IntegrityError
from django.utils.formats import localize
import datetime
import random

from random import randrange
from datetime import timedelta
from django.contrib.auth import get_user_model
User = get_user_model()



class Command(BaseCommand):
    help = "Creates customer or regular user"
    list_rakam = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    universty_list = [
        ["itü", "makina"],
        ["itü", "kimya"],
        ["itü", "inşaat"],
        ["marmara", "makina"],
        ["marmara", "makina"],
        ["marmara", "kimya"],
        ["marmara", "inşaat"],
    ]

    genderSelect=["1","2"]

    reltype = ["1", "2", "3", "4", "5"]


    # def add_arguments(self, parser):
    #     parser.add_argument("total", type=int, help="How many users will be created")

    def handle(self, *args, **kwargs):

        test_add_path = r"/home/zen/PycharmProjects/PROGISYAPP/backend/helper/test_add_temp"

        filepath_names = test_add_path + "/temp_names.txt"
        filepath_last_names = test_add_path + "/temp_lastnames.txt"

        a_last_name = []

        with open(filepath_last_names, encoding="utf8") as row:
            for line in row:
                a_last_name.append(str(line).strip())

        with open(filepath_names, encoding="utf8") as row:
            cnt = 0
            for j, i in enumerate(row):
                # if j < 100:
                #     continue
                name = str(i).strip()

                with transaction.atomic():
                    try:
                        user_contact = UserContact.objects.create(
                            phone1=self.get_random_phone(),
                            address="adres falan mahalle sokak",
                            city_id=7,
                            county_id=1811)

                        rand = random.choice(range(1, self.universty_list.__len__()))
                        education = UserEducation.objects.create(
                            education=3,
                            schoolName=self.universty_list[rand][0],
                            schoolSection=self.universty_list[rand][1])

                        placeOfBirth = Cities.objects.get(pk=random.choice(range(1, 81)))

                        new_profile = UserProfile.objects.create(
                            tc_no=self.get_random_tc(),
                            first_name=name,
                            last_name=random.choice(a_last_name),
                            genderSelect=random.choice(self.genderSelect),
                            maritalSelect=random.choice(self.genderSelect),
                            placeOfBirth=placeOfBirth,
                            contact=user_contact,
                            education=education,
                            birthday="2022-01-06")

                        UserRelatives.objects.create(
                            user_profile=new_profile,
                            relative_type=random.choice(self.reltype),
                            relative_name=random.choice(a_last_name),
                            relative_phone=self.get_random_phone()
                        )

                        account = Account.objects.get(pk=random.choice(range(1, 10)))


                        roleat = 12

                        roleat_end = 21
                        if j % 50 == 0:
                            roleat = 4
                            roleat_end = 12

                        role = Roles.objects.get(pk=random.choice(range(roleat, roleat_end)))

                        new_user = User.objects.create_user(email="{}{}{}.gma.com".format(name,j, random.choice(range(1, 10000))),
                                                            uap=UAP.objects.create(request_date=datetime.date.today()),
                                                            user_profile=new_profile,
                                                            password="tempPassw",
                                                            role=role,
                                                            account=account)

                        new_user.save()


                        if j % 50 ==0:
                            self.stdout.write(self.style.HTTP_INFO(f"{str(i).strip().__str__()} yönetici"))
                        else:
                            self.stdout.write(self.style.SUCCESS(f"{str(i).strip().__str__()} created"))
                    except IntegrityError as e:
                        self.stdout.write(self.style.WARNING(f"{str(e).strip().__str__()} created"))

            d_user = User.objects.filter(is_email_verified=False)

            for j, i in enumerate(d_user):

                if j % 10 == 0:
                    self.stdout.write(self.style.NOTICE(f"{str(i).strip().__str__()} onaylanmayana at"))
                    continue

                i.is_working = True
                i.is_active = True
                i.is_email_verified = True

                i.uap.starting_work_date = datetime.datetime.now()
                i.uap.save()

                i.save()
                self.stdout.write(self.style.MIGRATE_HEADING(f"{str(i).strip().__str__()} onaylandı"))


    def get_random_phone(self):
        tel = "053{}{}{}{}{}{}{}{}".format(random.choice(range(2, 6)),
                                           random.choice(self.list_rakam),
                                           random.choice(self.list_rakam),
                                           random.choice(self.list_rakam),
                                           random.choice(self.list_rakam),
                                           random.choice(self.list_rakam),
                                           random.choice(self.list_rakam),
                                           random.choice(self.list_rakam))

        co = UserContact.objects.filter(phone1=tel)
        if co:
            self.get_random_phone()

        return tel

    def get_random_tc(self):
        tc = "{}{}{}{}{}{}{}{}{}{}{}".format(
                random.choice(self.list_rakam),
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

        co = UserProfile.objects.filter(tc_no=tc)
        if co:
            self.get_random_phone()

        return tc

        # d1 = datetime.strptime('1/1/2019 1:30 PM', '%m/%d/%Y %I:%M %p')
        # # d2 = datetime.strptime('2/17/2021 2:30 PM', '%m/%d/%Y %I:%M %p')
        #
        # d2 = datetime.now()
        #
        # for i in a_name_last_name:
        #     r_date = random_date(d1, d2)
        # a_dates.append(r_date)
        # a_dates.sort()
        #

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
