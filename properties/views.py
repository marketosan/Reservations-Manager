from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    if request.user.is_staff:
        return render(request, "properties/admin_home.html")
    return render(request, "properties/guest_home.html")

