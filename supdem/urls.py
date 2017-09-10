from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter(trailing_slash=False)
router.register(r'categories', views.CategoryViewSet)
router.register(r'users', views.MyUserViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'groups', views.GroupViewSet)
