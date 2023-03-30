from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = {}
            if request.user.groups.exists():
                group = set(map(lambda x: x.name, request.user.groups.all()))

            if group.isdisjoint(set(allowed_roles)):
                return redirect("home")
            else:
                return view_func(request, *args, **kwargs)

        return wrapper_func

    return decorator


def staff_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = {}
        if request.user.groups.exists():
            group = set(map(lambda x: x.name, request.user.groups.all()))

        if "staff" in group:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("home")

    return wrapper_func
