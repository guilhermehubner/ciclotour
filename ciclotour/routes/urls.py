from django.conf.urls import url
from ciclotour.routes.views import create

urlpatterns = [
    url(r'^create/$', create, name="create"),
]