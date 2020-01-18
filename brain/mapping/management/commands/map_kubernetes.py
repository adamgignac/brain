from django.core.management.base import BaseCommand, CommandError
from mapping.models import Workspace, ItemType, Item, Dependency
import requests


class Kubernetes:
    def __init__(self, api):
        self.api = api

    def list_namespaces(self):
        r = requests.get(f"{self.api}/api/v1/namespace")
        response = r.json()
        return [namespace["objectMeta"] for namespace in response["namespaces"]]

    def deployments_in_namespace(self, namespace):
        r = requests.get(f"{self.api}/api/v1/deployment/{namespace}")
        response = r.json()
        return [deployment["objectMeta"] for deployment in response["deployments"]]


class Command(BaseCommand):
    help = "Scans Kubernetes and maps all namespaces and deployments"

    def add_arguments(self, parser):
        parser.add_argument(
            "kubernetes",
            action="store",
            type=str,
            help="Base URL for Kubernetes API host",
        )

    def get_workspace(self):
        print("Available workspaces:")
        workspaces = Workspace.objects.all()
        for i, w in enumerate(workspaces):
            print(f"[{i}]: {w.label}")

        while True:
            target_workspace_id = input("Select workspace: ")
            try:
                return workspaces[int(target_workspace_id)]
            except (IndexError, ValueError):
                print("Please select a valid workspace from the list.")

    def get_item_types(self):
        if not ItemType.objects.filter(label="Kubernetes Namespace").exists():
            namespace_type = ItemType(
                label="Kubernetes Namespace", color="gray", shape="box"
            )
            namespace_type.save()
            print("Created Kubernetes Namespace item type")
        else:
            namespace_type = ItemType.objects.get(label="Kubernetes Namespace")
            print("Found existing Kubernetes Namespace item type")

        if not ItemType.objects.filter(label="Kubernetes Deployment").exists():
            deployment_type = ItemType(
                label="Kubernetes Deployment", color="white", shape="box"
            )
            deployment_type.save()
            print("Created Kubernetes Deployment item type")
        else:
            deployment_type = ItemType.objects.get(label="Kubernetes Deployment")
            print("Found existing Kubernetes Deployment item type")
        return namespace_type, deployment_type

    def handle(self, *args, **options):
        workspace = self.get_workspace()
        NAMESPACE, DEPLOYMENT = self.get_item_types()
        print(f"Scanning {options['kubernetes']} into {workspace.label}...")
        k8s = Kubernetes(options["kubernetes"])
        print("Found the following namespaces:")
        for namespace in k8s.list_namespaces():
            print(namespace["name"])
            ns, _ = Item.objects.get_or_create(
                label=namespace["name"], type=NAMESPACE, workspace=workspace
            )
            for deployment in k8s.deployments_in_namespace(namespace["name"]):
                print("-", deployment["name"])
                dep, _ = Item.objects.get_or_create(
                    label=f"{namespace['name']}:{deployment['name']}",
                    type=DEPLOYMENT,
                    workspace=workspace,
                )
                _ = Dependency.objects.get_or_create(
                    item1=dep, item2=ns, workspace=workspace
                )
