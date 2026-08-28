from rest_framework import viewsets
from .models import EndpointDoc
from .serializers import EndpointDocSerializer


class EndpointDocViewSet(viewsets.ModelViewSet):
    queryset = EndpointDoc.objects.all()
    serializer_class = EndpointDocSerializer
