from django.shortcuts import render


def create(request):
    return render(request, 'routes/routes_form.html')
