from rest_framework import viewsets
from .models import Activity
from .serializers import ActivitySerializer
from .filters import ActivityFilter


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filterset_class = ActivityFilter