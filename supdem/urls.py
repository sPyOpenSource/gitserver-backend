from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter(trailing_slash=False)
router.register(r'category', views.CategoryViewSet)
router.register(r'question', views.CategoryQuestionViewSet)
router.register(r'users', views.MyUserViewSet)
router.register(r'item', views.ItemViewSet)
