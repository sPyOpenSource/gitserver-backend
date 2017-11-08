from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from supdem import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/', include('supdem.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
