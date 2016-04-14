from ciclotour.core.views import home
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^routes/', include('ciclotour.routes.urls', namespace='routes')),
    url(r'^admin/', include(admin.site.urls)),
]
