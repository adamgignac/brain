from .models import Workspace


def workspace_list(request):
    workspaces = {
        "public": Workspace.objects.filter(public=True)
    }
    if request.user.is_authenticated:
        workspaces['private'] = Workspace.objects.filter(public=False,
                                                         owner=request.user)
    return {
        "workspaces": workspaces
    }
