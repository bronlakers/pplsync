from functools import wraps
from django.http import HttpResponseForbidden

def in_group(user, group_name: str) -> bool:
    return user.is_authenticated and user.groups.filter(name=group_name).exists()

def any_group(user, group_names) -> bool:
    return user.is_authenticated and user.groups.filter(name__in=group_names).exists()

def group_required(*group_names):
    """Restrict access to users in any of the provided groups, or superusers."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if request.user.is_superuser or any_group(request.user, group_names):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have access to this page.")
        return _wrapped
    return decorator
