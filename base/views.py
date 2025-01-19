from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework import permissions


class BaseWorkerViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', ]
    permission_classes = [permissions.IsAuthenticated]


class PointDataBaseViewSet(BaseWorkerViewSet):
    def get_queryset(self):
        return self.queryset.filter(added_by=self.request.user)


class WorkerBaseViewSet(PointDataBaseViewSet):
    pass


class PrivacyView(TemplateView):
    template_name = 'privacy.html'
