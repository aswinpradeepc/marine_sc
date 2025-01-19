from functools import wraps

from django.shortcuts import redirect

from .models import Payment


def payment_completed_test(user):
    return Payment.objects.filter(user=user, status='success').exists()


def payment_completed(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/maricon/login/')
        elif not payment_completed_test(request.user):
            # Redirect to a page indicating payment completion is required
            return redirect('/payment/')
        return view_func(request, *args, **kwargs)

    return _wrapped_view
