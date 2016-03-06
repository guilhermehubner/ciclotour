from ciclotour.core.views import home

from django.conf.urls import url, include

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^routes/', include('ciclotour.routes.urls', namespace='routes')),
]
