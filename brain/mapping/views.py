# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Workspace, Item, ItemType, Dependency


class WorkspaceList(ListView):
    def get_queryset(self):
        spaces = Workspace.objects.filter(public=True)
        if self.request.user.is_authenticated:
            spaces |= Workspace.objects.filter(owner=self.request.user)
        return spaces


class WorkspaceDetail(DetailView):
    model = Workspace


class CreateWorkspace(LoginRequiredMixin, CreateView):
    model = Workspace
    fields = ["label", "public", "engine"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())


class ItemTypeList(ListView):
    model = ItemType


class CreateItemType(LoginRequiredMixin, CreateView):
    model = ItemType
    fields = ["label", "shape", "color"]
    success_url = reverse_lazy("item-type-list")


class UpdateItemType(LoginRequiredMixin, UpdateView):
    model = ItemType
    fields = ["label", "shape", "color"]
    success_url = reverse_lazy("item-type-list")


class DeleteItemType(LoginRequiredMixin, DeleteView):
    model = ItemType
    success_url = reverse_lazy("item-type-list")


class DeleteWorkspace(LoginRequiredMixin, DeleteView):
    model = Workspace
    success_url = reverse_lazy("workspace-list")


class ItemDetail(DetailView):
    model = Item


class CreateItem(LoginRequiredMixin, CreateView):
    model = Item
    fields = ["type", "label", "notes"]

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["workspace"] = self.kwargs["workspace"]
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.workspace = Workspace.objects.get(slug=self.kwargs["workspace"])
        obj.save()
        return HttpResponseRedirect(obj.workspace.get_absolute_url())


class UpdateItem(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ["label", "notes"]

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["workspace"] = self.kwargs["workspace"]
        return ctx


class DeleteItem(LoginRequiredMixin, DeleteView):
    model = Item

    def get_success_url(self):
        return self.object.workspace.get_absolute_url()


class DependencyEditorMixin:
    model = Dependency
    fields = ["item1", "item2", "description"]

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["workspace"] = self.kwargs["workspace"]
        return ctx

    def get_workspace(self):
        return Workspace.objects.get(slug=self.kwargs["workspace"])

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        workspace = self.get_workspace()
        items = Item.objects.filter(workspace=workspace)
        form.fields["item1"].queryset = items
        form.fields["item1"].label = "Item"
        form.fields["item2"].queryset = items
        form.fields["item2"].label = "Depends On"
        return form

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.workspace = self.get_workspace()
        obj.save()
        return HttpResponseRedirect(obj.workspace.get_absolute_url())


class CreateDependency(DependencyEditorMixin, LoginRequiredMixin, CreateView):
    pass


class UpdateDependency(DependencyEditorMixin, LoginRequiredMixin, UpdateView):
    pass


class DeleteDependency(LoginRequiredMixin, DeleteView):
    model = Dependency

    def get_success_url(self):
        return reverse_lazy("workspace-detail", args=[self.kwargs["workspace"]])
