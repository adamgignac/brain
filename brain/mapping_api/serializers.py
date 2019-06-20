from mapping.models import Item, Workspace
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    dependencies = serializers.StringRelatedField(many=True)
    type = serializers.StringRelatedField()

    class Meta:
        model = Item
        fields = ("type", "label", "dependencies", "notes", "workspace", "slug")


class WorkspaceSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Workspace
        fields = ("label", "owner", "public", "items", "slug")
