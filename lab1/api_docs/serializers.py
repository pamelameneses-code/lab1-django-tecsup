from rest_framework import serializers
from .models import EndpointDoc


class EndpointDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndpointDoc
        fields = '__all__'
