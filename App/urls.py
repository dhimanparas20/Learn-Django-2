from django.urls import path,include
from . import views
from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# from .routing import *

router = routers.DefaultRouter()
router.register(r'user',UserdetailViewset,basename="UserdetailViewset2")
router.register(r'stations', StationViewSet, basename='station')


urlpatterns = [
    path('',include(router.urls)),   # for above routers
    path('login/', views.login.as_view(), name="login"),
    path('view_details/', views.view_details.as_view(), name="view_details"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # to generate tokens only
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # to generate tokens only
    # path('api-auth/', include('rest_framework.urls')),   #if using another token verification
    # path('user/', UserdetailViewset2.as_view({'get': 'me'}), name='me'), #if dont wanna user routers then use this
]
# urlpatterns += websocket_urlpatterns
