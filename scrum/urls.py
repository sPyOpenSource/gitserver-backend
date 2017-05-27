from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns

from rest_framework.authtoken.views import obtain_auth_token

from board.urls import router
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from supdem import views

urlpatterns = [
    url(r'^api/token/', obtain_auth_token, name='api-token'),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    url(r'^$', views.index, name='index'),
    url(r'^(?P<usertype>local|refugee)/$', views.index, name='index'),
    url(r'^about/$', TemplateView.as_view(template_name='supdem/about.html'), name='about'),
    url(r'^how_it_works/$', TemplateView.as_view(template_name='supdem/how_it_works.html'),
        name='how_it_works'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^resetpassword/$', views.resetpassword, name='resetpassword'),
    url(r'^newpassword/$', views.newpassword, name='newpassword'),
    url(r'^mypage/$', views.mypage, name='mypage'),
    url(r'^(?P<usertype>local|refugee)/(?P<centreslug>[a-z_]{5,})/$',
        views.list_view, name='list'),
    url(r'^(?P<usertype>local|refugee)/(?P<centreslug>[a-z_]{5,})/additem/$',
        views.additem, name='additem'),
    url(r'^(?P<usertype>local|refugee)/(?P<centreslug>[a-z_]{5,})/item-(?P<itemid>\d+)/$',
        views.item, name='item'),
    url(r'^(?P<usertype>local|refugee)/(?P<centreslug>[a-z_]{5,})/item-(?P<itemid>\d+)/extend/$',
        views.extenditem, name='extenditem'),
    url(r'^(?P<usertype>local|refugee)/(?P<centreslug>[a-z_]{5,})/item-(?P<itemid>\d+)/adddialogue/$',
        views.adddialogue, name='adddialogue'),
    url(r'^(?P<usertype>local|refugee)/(?P<centreslug>[a-z_]{5,})/item-(?P<itemid>\d+)/delete/$',
        views.deleteitem, name='deleteitem'),
    url(r'^(?P<usertype>local|refugee)/(?P<centreslug>[a-z_]{5,})/dialogue-(?P<dialogueid>\d+)/delete/$',
        views.deletedialogue, name='deletedialogue'),
    # must be low in the list otherwise it east the /login/ and /logout/ requests
    url(r'^(?P<centreslug>[a-z_]{5,})/$', views.index, name='index'),
)
