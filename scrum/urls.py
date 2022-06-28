from django.urls import include, re_path
from django.conf import settings
from django.conf.urls.static import static
from supdem import views


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^api/', include('supdem.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
