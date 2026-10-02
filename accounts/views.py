from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import UserCreateForm, UserEditForm


def staff_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapper


@staff_required
def user_list(request):
    users = User.objects.order_by("username")
    return render(request, "accounts/list.html", {"users": users})


@staff_required
def user_create(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserCreateForm()
    return render(request, "accounts/form.html", {"form": form, "title": "Add user"})


@staff_required
def user_edit(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserEditForm(instance=user_obj)
    return render(request, "accounts/form.html", {"form": form, "title": "Edit user"})


@staff_required
@require_POST
def user_delete(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if user_obj != request.user:
        user_obj.delete()
    return redirect("user_list")

