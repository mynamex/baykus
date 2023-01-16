from rest_framework import serializers

from apps.accounts.models import Apartments, Devices, Role


class ApartmentsSerializer(serializers.ModelSerializer):
    # data_created = serializers.DateField(format="%Y-%m-%d", read_only=True)
    data_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")


    class Meta:
        model = Apartments
        fields = ['id', 'name', "wifi_name", "wifi_pass",  'address', "is_active", 'data_created']

        order_by = (
            ('name',))


class DevicesSerializer(serializers.ModelSerializer):
    data_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Devices
        fields = ['id', "name", 'apartments', "is_active", "api_key", 'data_created']

        order_by = (
            ('name',))



class RoleSerializer(serializers.ModelSerializer):
    data_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Role
        fields = ['id', "name", "is_active", "key", 'data_created']

        order_by = (
            ('name',))
