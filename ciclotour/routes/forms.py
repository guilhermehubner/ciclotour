from ciclotour.routes.models import Route
from django.forms import ModelForm


class RouteForm(ModelForm):
    class Meta:
        model = Route
        fields = ['title', 'origin', 'description', 'field']
