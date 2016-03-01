from ciclotour.core.views import home

from django.conf.urls import url

urlpatterns = [
    url(r'^$', home),
]
