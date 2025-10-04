from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Device  # si tienes modelo Device

@login_required
def dashboard(request):
    return render(request, "dispositivos/dashboard.html")


@login_required
def devices_list(request):
    org = request.user.userprofile.organization
    qs = Device.objects.filter(organization=org).select_related("category", "zone")
    return render(request, "dispositivos/list.html", {"devices": qs})
