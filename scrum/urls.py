from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns

from supdem.urls import router
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from supdem import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^api/messages$', views.MessageList.as_view()),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    url(r'^$', views.index, name='index'),
    url(r'^adduser$', views.adduser, name='adduser'),
    url(r'^image$', views.image, name='image'),
    url(r'^about/$', TemplateView.as_view(template_name='supdem/about.html'), name='about'),
    url(r'^help/$', TemplateView.as_view(template_name='supdem/help.html'),
        name='help'),
    url(r'^resetpassword/$', views.resetpassword, name='resetpassword'),
    url(r'^newpassword/$', views.newpassword, name='newpassword'),
    # must be low in the list otherwise it east the /login/ and /logout/ requests
)
