"""brain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
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
    DeleteItemType
)
from django.contrib.auth.views import LoginView, LogoutView

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
    path('login/', LoginView.as_view(template_name="adminlte/login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
