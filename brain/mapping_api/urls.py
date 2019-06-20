from rest_framework import routers
from mapping_api import views as api_views
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'workspaces', api_views.WorkspaceViewSet, basename="workspace")
router.register(r'items', api_views.ItemViewSet)

urlpatterns = [
    path('', include(router.urls))
]