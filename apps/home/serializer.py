from rest_framework import serializers

from apps.accounts.models import Apartments,   Devices


class ApartmentsSerializer(serializers.ModelSerializer):
    # data_created = serializers.DateField(format="%Y-%m-%d", read_only=True)
    data_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    device_last_online_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Apartments
        fields = ['id', 'name', "api_key", "wifi_name", "wifi_pass",  'address', "is_active", 'data_created',"device_last_online_date"]

        order_by = (
            ('name',))


class ApartmentsSerializerCustomer(serializers.ModelSerializer):
    # data_created = serializers.DateField(format="%Y-%m-%d", read_only=True)

    device_last_online_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Apartments
        fields = ['id', 'name', 'address', 'device_last_online_date']

        order_by = (
            ('name',))


class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = ['pk',
                  "key",
                  "name",
                  "device_type",
                  "name",
                  "status",
                  "is_active",
                  "label",
                  ]



