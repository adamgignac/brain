from django.urls import path

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
    DeleteItemType,
    CreateDependency,
    UpdateDependency,
    DeleteDependency,
)

urlpatterns = [
    path("", WorkspaceList.as_view(), name="workspace-list"),
    path("types/", ItemTypeList.as_view(), name="item-type-list"),
    path("types/add/", CreateItemType.as_view(), name="add-item-type"),
    path("types/<slug>/edit", UpdateItemType.as_view(), name="edit-item-type"),
    path("types/<slug>/delete", DeleteItemType.as_view(), name="delete-item-type"),
    path("workspaces/new/", CreateWorkspace.as_view(), name="create-workspace"),
    path("workspaces/<slug>/", WorkspaceDetail.as_view(), name="workspace-detail"),
    path(
        "workspaces/<slug>/delete/", DeleteWorkspace.as_view(), name="delete-workspace"
    ),
    path("workspaces/<workspace>/items/add/", CreateItem.as_view(), name="add-item"),
    path(
        "workspaces/<workspace>/items/<slug>/", ItemDetail.as_view(), name="item-detail"
    ),
    path(
        "workspaces/<workspace>/items/<slug>/edit",
        UpdateItem.as_view(),
        name="update-item",
    ),
    path(
        "workspaces/<workspace>/items/<slug>/delete",
        DeleteItem.as_view(),
        name="delete-item",
    ),
    path(
        "workspaces/<workspace>/dependencies/add/",
        CreateDependency.as_view(),
        name="add-dependency",
    ),
    path(
        "workspaces/<workspace>/dependencies/<int:pk>/",
        UpdateDependency.as_view(),
        name="update-dependency",
    ),
    path(
        "workspaces/<workspace>/dependencies/<int:pk>/delete/",
        DeleteDependency.as_view(),
        name="delete-dependency",
    ),
]
