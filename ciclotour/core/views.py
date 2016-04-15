from ciclotour.core.forms import LoginForm
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url


@login_required(login_url=reverse_lazy('login'))
def home(request):
    return render(request, 'index.html')


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(resolve_url('home'))

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            django_login(request, form.get_user())
            return HttpResponseRedirect(resolve_url('home'))

        return render(request, 'login.html', {'form': form})

    return render(request, 'login.html', {'form': LoginForm()})


@login_required(login_url=reverse_lazy('login'))
def logout(request):
    django_logout(request)
    return HttpResponseRedirect(resolve_url('login'))

