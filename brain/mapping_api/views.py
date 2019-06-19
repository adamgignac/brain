from mapping.models import Item, Workspace
from .serializers import ItemSerializer, WorkspaceSerializer
from rest_framework import viewsets


class WorkspaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceSerializer
    queryset = Workspace.objects.filter(public=True)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
