from ciclotour.core.views import home
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^api/', include('ciclotour.api.urls', namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
