# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView
)
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Workspace, Item, ItemType


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
    fields = ['label', 'public']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())


class ItemTypeList(ListView):
    model = ItemType


class CreateItemType(LoginRequiredMixin, CreateView):
    model = ItemType
    fields = ['label', 'shape', 'color']
    success_url = reverse_lazy('item-type-list')


class UpdateItemType(LoginRequiredMixin, UpdateView):
    model = ItemType
    fields = ['label', 'shape', 'color']
    success_url = reverse_lazy('item-type-list')


class DeleteItemType(LoginRequiredMixin, DeleteView):
    model = ItemType
    success_url = reverse_lazy('item-type-list')


class DeleteWorkspace(LoginRequiredMixin, DeleteView):
    model = Workspace
    success_url = reverse_lazy('workspace-list')


class ItemDetail(DetailView):
    model = Item


class CreateItem(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['type', 'label', 'notes']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.workspace = Workspace.objects.get(slug=self.kwargs['workspace'])
        obj.save()
        return HttpResponseRedirect(obj.workspace.get_absolute_url())


class UpdateItem(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['label', 'notes']


class DeleteItem(LoginRequiredMixin, DeleteView):
    model = Item

    def get_success_url(self):
        return self.object.workspace.get_absolute_url()
