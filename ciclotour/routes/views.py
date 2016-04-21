from ciclotour.routes.forms import RouteForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render


@login_required(login_url=reverse_lazy('login'))
def create(request):
    return render(request, 'routes/routes_form.html', {'form': RouteForm()})


def detail(request, pk):
    return render(request, 'routes/routes_detail.html')
