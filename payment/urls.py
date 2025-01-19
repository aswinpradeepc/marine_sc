from django.urls import path

from .views import *

urlpatterns = [
    path('', PaymentView.as_view(), name='payment'),
    path('verify/', payment_verification, name='verify'),
]
    