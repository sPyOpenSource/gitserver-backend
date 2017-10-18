from . import views
from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'users', views.MyUserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^additem$', views.additem, name='item'),
    url(r'^adduser$', views.adduser, name='adduser'),
    url(r'^csrf_token$', views.csrf_token, name='csrf'),
    url(r'^messages$', views.MessageList.as_view()),
    url(r'^resetpassword$', views.resetpassword, name='resetpassword'),
    url(r'^token-auth$', obtain_jwt_token)
]
