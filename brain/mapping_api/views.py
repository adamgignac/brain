from mapping.models import Item, Workspace
from .serializers import ItemSerializer, WorkspaceSerializer
from rest_framework import viewsets


class WorkspaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        spaces = Workspace.objects.filter(public=True)
        if self.request.user.is_authenticated:
            spaces |= Workspace.objects.filter(owner=self.request.user)
        return spaces


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
