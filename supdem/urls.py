from . import views
from django.conf.urls import url, include
from rest_framework import routers


# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter(trailing_slash = False)
router.register(r'items', views.ItemViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
