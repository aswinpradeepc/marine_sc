from django.contrib.gis.geos import Point
from rest_framework import serializers
from .models import PointData, Model
from office.models import Scheme


class SchemeNameValidationMixin:
    def validate_scheme_name(self, value):
        # Normalize the input name to match the cleaning logic in the model
        normalized_name = " ".join(value.split()).title().strip()

        # Check if a scheme with this normalized name already exists
        scheme, created = Scheme.objects.get_or_create(name=normalized_name)
        return scheme


class LocationSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id']
        read_only_fields = ['id']


class PointDataSerializer(BaseModelSerializer, SchemeNameValidationMixin):
    # Swagger Schema for location field
    location = LocationSerializer(many=False)
    added_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # section= serializers.SerializerMethodField(read_only=True)
    division_name = serializers.SerializerMethodField(read_only=True)
    scheme_name = serializers.CharField(max_length=100)

    # Override to_representation and to_internal_value as before

    class Meta(BaseModelSerializer.Meta):
        model = PointData
        fields = BaseModelSerializer.Meta.fields + ['location', 'division_name', 'location_name', 'scheme_type',
                                                    'resource_type', 'section', 'scheme_name']
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ['resource_type', 'section']

    @staticmethod
    def get_division_name(obj):
        return obj.division_name

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert latitude and longitude to desired format
        latitude = instance.location.x
        longitude = instance.location.y
        representation['location'] = {"y": latitude, "x": longitude}
        return representation

    @staticmethod
    def validate_location(value):
        if 'x' not in value or 'y' not in value:
            raise serializers.ValidationError("lat and long are required.")
        try:
            latitude = value['y']
            longitude = value['x']
        except ValueError:
            raise serializers.ValidationError("Invalid lat or long format.")
        return Point(latitude, longitude)

    def create(self, validated_data):
        # Get the requesting user from the context
        user = self.context['request'].user if 'request' in self.context else None
        validated_data['added_by'] = user
        if user:
            validated_data['section'] = user.section
        return super().create(validated_data)

    def save(self, **kwargs):
        super().save(**kwargs)
        self.instance.latitude, self.instance.longitude = self.instance.location.y, self.instance.location.x
        self.instance.save()
