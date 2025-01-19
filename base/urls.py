"""
organisation/urls.py
"""

from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path("privacy/", views.PrivacyView.as_view(), name="privacy"),
]
