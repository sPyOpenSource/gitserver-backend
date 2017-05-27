from django.conf.urls import url

from . import views

# This file is not used. The url patterns are moved to the main url definitions file
# because of https://docs.djangoproject.com/en/1.8/topics/i18n/translation/#language-prefix-in-url-patterns
#
#urlpatterns = [
#    url(r'^$', views.index, name='index'),
#    url(r'^(?:(?P<languagecode>[a-z]{2})/)?(?P<usertype>local|refugee)/(?P<centre>[a-z_]{3,})/$', views.list, name='list'),
#    url(r'^(?P<languagecode>[a-z]{2})/(?P<usertype>local|refugee)/(?P<centre>[a-z_]{3,})/item-(?P<itemid>[\d+])/$', views.item, name='item'),
#    url(r'^(?:(?P<languagecode>[a-z]{2})/)?(?:(?P<usertype>local|refugee)/)?(?:(?P<centre>[a-z_]{3,})/)?$', views.index, name='index'),
#]
