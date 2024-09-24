from functools import wraps
from django.shortcuts import redirect

from django.urls import reverse


def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the session key exists
        if 'teacher_name' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            # If the session key doesn't exist, redirect to a login or error page
            return redirect(reverse('student:landing'))  # Change 'login' to your redirect URL
     
    return _wrapped_view
