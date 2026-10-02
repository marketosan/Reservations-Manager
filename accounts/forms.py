from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def _apply_daisyui_widgets(form):
    for field in form.fields.values():
        if isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs.setdefault("class", "checkbox")
        else:
            field.widget.attrs.setdefault("class", "input w-full")


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "is_staff", "is_active")
        labels = {"is_staff": "Admin User"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_daisyui_widgets(self)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "is_staff", "is_active")
        labels = {"is_staff": "Admin User"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_daisyui_widgets(self)
