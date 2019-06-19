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
    path('workspace/new/', CreateWorkspace.as_view(), name='create-workspace'),
    path('workspace/<int:pk>/', WorkspaceDetail.as_view(), name='workspace-detail'),
    path('workspace/<int:pk>/delete/', DeleteWorkspace.as_view(), name='delete-workspace'),
    path('workspace/<int:workspace>/add/', CreateItem.as_view(), name='add-item'),
    path('types/', ItemTypeList.as_view(), name='item-type-list'),
    path('types/add/', CreateItemType.as_view(), name='add-item-type'),
    path('types/<int:pk>/edit', UpdateItemType.as_view(), name='edit-item-type'),
    path('types/<int:pk>/delete', DeleteItemType.as_view(), name='delete-item-type'),
    path('item/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
    path('item/<int:pk>/edit', UpdateItem.as_view(), name='update-item'),
    path('item/<int:pk>/delete', DeleteItem.as_view(), name='delete-item'),
]