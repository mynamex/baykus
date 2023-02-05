
from rest_framework import serializers


from apps.customauth.models import MyUser



class UserSerializer(serializers.ModelSerializer):
    password = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MyUser
        fields = ('id', 'name', 'username', 'is_active', "password")



    def get_password(self, obj):
        return "********"  # str(obj.module_type)






# class BlockDaireFilterIsActiveS(serializers.ModelSerializer):
#     customer = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = Daire
#         fields = ['id', 'daire_name', 'customer', 'daire_status', "is_active"]
#
#         order_by = (
#             ('daire_name',))
#
#     def get_blocks(self, obj):
#         return obj.module_type.pk  # str(obj.module_type)















