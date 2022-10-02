from django.contrib import messages
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def admin_only(view_func):
    def wrapper_func_admin(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'user':
            return redirect('home')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_func_admin


def user_only(view_func):
    def wrapper_func_user(request, *args, **kwargs):

        if request.user.is_superuser:
            return redirect('admin-page')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func_user
