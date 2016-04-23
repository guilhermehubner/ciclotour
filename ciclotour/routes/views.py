from ciclotour.core.serializer import serializer
from ciclotour.routes.forms import RouteForm
from ciclotour.routes.models import Route
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404


@login_required(login_url=reverse_lazy('login'))
def create(request):
    return render(request, 'routes/routes_form.html', {'form': RouteForm()})


@login_required(login_url=reverse_lazy('login'))
def detail(request, pk):
    route = get_object_or_404(Route, pk=pk)
    waypoints = route.waypoint_set.all()

    context = {
        'route': route,
        'waypoints': serializer.serialize(waypoints)
    }

    return render(request, 'routes/routes_detail.html', context)
