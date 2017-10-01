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
    url(r'^$', views.index, name='index'),
    url(r'^api/messages$', views.MessageList.as_view()),
    url(r'^api/demos$', views.demo, name='demo'),
    url(r'^api/image$', views.image, name='image'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    url(r'^adduser$', views.adduser, name='adduser'),
    url(r'^resetpassword/$', views.resetpassword, name='resetpassword'),
    # must be low in the list otherwise it east the /login/ and /logout/ requests
)
