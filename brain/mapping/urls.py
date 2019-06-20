from django.urls import path, include

from mapping.views import (
    WorkspaceList,
    WorkspaceDetail,
    CreateWorkspace,
    DeleteWorkspace,

    CreateItem,
    UpdateItem,
    DeleteItem,
    ItemDetail,
    ItemTypeList,
    CreateItemType,
    UpdateItemType,
    DeleteItemType
)

urlpatterns = [
    path('', WorkspaceList.as_view(), name='workspace-list'),
    path('workspaces/new/', CreateWorkspace.as_view(), name='create-workspace'),
    path('workspaces/<slug>/', WorkspaceDetail.as_view(), name='workspace-detail'),
    path('workspaces/<slug>/delete/', DeleteWorkspace.as_view(), name='delete-workspace'),
    path('workspaces/<slug>/add/', CreateItem.as_view(), name='add-item'),
    path('types/', ItemTypeList.as_view(), name='item-type-list'),
    path('types/add/', CreateItemType.as_view(), name='add-item-type'),
    path('types/<slug>/edit', UpdateItemType.as_view(), name='edit-item-type'),
    path('types/<slug>/delete', DeleteItemType.as_view(), name='delete-item-type'),
    path('items/<slug>/', ItemDetail.as_view(), name='item-detail'),
    path('items/<slug>/edit', UpdateItem.as_view(), name='update-item'),
    path('items/<slug>/delete', DeleteItem.as_view(), name='delete-item'),
]