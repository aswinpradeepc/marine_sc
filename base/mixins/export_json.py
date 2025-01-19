from django.core.serializers import serialize
from django.http import HttpResponse


class ExportJsonMixin:
    def export_as_json(self, request, queryset):
        """
        Serialize queryset to JSON and return as a file.
        """
        data = serialize('json', queryset)

        response = HttpResponse(data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename={}_data.json'.format(self.model._meta.model_name)
        return response
