from django.conf.urls import url
from ciclotour.routes.views import create, detail

urlpatterns = [
    url(r'^create/$', create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', detail, name='detail'),
]