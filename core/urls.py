from django.contrib import admin

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from apps.customauth.tokens import TokenObtainPairView
from django.urls import path, include  # add this
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path("", include("apps.authentication.urls")),  # Auth routes - login / register
    path("", include("apps.home.urls")),  # UI Kits Html files

    path('staff/', include('apps.staff.urls')),

]
