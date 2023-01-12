# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# # from django.utils import six
#
#

#
#
# class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return (
#             six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
#
#         )
#
# account_activation_token = AccountActivationTokenGenerator()

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.views import TokenViewBase

from apps.customauth.models import MyUser


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_uid = decoded_payload['user_id']
        # add filter query
        # data.update({'custom_field': 'custom_data'})

        user = MyUser.objects.prefetch_related("account").get(pk=user_uid)

        data.update({'user_info': {
            "full_name": user.name,
            "site_name": user.account.site_name,
        }})

        return data



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        license_status = self.user.account.license_status

        if license_status:
            return {
                "account_info": {
                    'success': 'true',
                    'site_name': self.user.account.site_name,
                    'is_staff': self.user.is_person,
                    "security_id":self.user.pk,
                    'account_user_name': self.user.name,
                    'license_status':license_status,
                    'desc': "login success",
                },
                **attrs,
            }
        else:
            return {
                "account_info": {
                    'success': 'true',
                    'site_name': self.user.account.site_name,
                    'is_staff': self.user.is_person,
                    'account_user_name': self.user.name,
                    'license_status': license_status,
                    'desc': "Lisans süresi dolmuş, lütfen bu programın yetkililerine"
                },
                **attrs,
            }


class TokenObtainPairView(TokenViewBase):
    """
        Return JWT tokens (access and refresh) for specific user based on username and password.
    """
    serializer_class = MyTokenObtainPairSerializer


class TokenRefreshView(TokenViewBase):
    """
        Renew tokens (access and refresh) with new expire time based on specific user's access token.
    """
    serializer_class = CustomTokenRefreshSerializer