# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

from bs4 import BeautifulSoup

from graphviz import Digraph
from .graphviz_attrs import SHAPES, COLORS


class Workspace(models.Model):
    label = models.CharField(max_length=1024)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = f"{self.id}-{slugify(self.label)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse("workspace-detail", args=[self.slug])

    def graphviz_graph(self):
        graph = Digraph(comment=self.label, format="svg")
        for item in self.items.all():
            graph.node(
                str(item.pk),
                item.label,
                shape=item.type.shape,
                style="filled",
                fillcolor=item.type.color,
                URL=item.get_absolute_url(),
            )
        for dependency in self.relationships.all():
            graph.edge(str(dependency.item1.pk), str(dependency.item2.pk), dir="back")
        return BeautifulSoup(graph.pipe(), "lxml").find("svg")


class ItemType(models.Model):
    label = models.CharField(max_length=1024)
    shape = models.CharField(max_length=15, choices=SHAPES)
    color = models.CharField(max_length=15, choices=COLORS, default="white")
    slug = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = f"{self.id}-{slugify(self.label)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label


class Dependency(models.Model):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="relationships"
    )
    item1 = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="supports")
    item2 = models.ForeignKey(
        "Item", on_delete=models.CASCADE, related_name="depends_on"
    )


class Item(models.Model):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="items"
    )
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    label = models.CharField(max_length=1024)
    notes = models.TextField(blank=True)
    slug = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = f"{self.id}-{slugify(self.label)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse("item-detail", args=[self.slug])

    @property
    def direct_supports(self):
        return Item.objects.filter(
            id__in=Dependency.objects.filter(item2=self).values_list("item1", flat=True)
        )

    @property
    def dependencies(self):
        return Item.objects.filter(
            id__in=Dependency.objects.filter(item1=self).values_list("item2", flat=True)
        )

    def full_dependency_graph(self):
        graph = Digraph(comment=self.label + " Dependencies", format="svg")
        visited = []

        def dfs(start):
            if start in visited:
                return
            visited.append(start)
            graph.node(
                str(start.pk),
                start.label,
                shape=start.type.shape,
                style="filled",
                fillcolor=start.type.color,
                URL=start.get_absolute_url(),
            )
            for neighbor in start.dependencies.all():
                graph.edge(str(start.pk), str(neighbor.pk), dir="back")
                dfs(neighbor)

        dfs(self)
        return BeautifulSoup(graph.pipe(), "lxml").find("svg")

    def full_support_graph(self):
        graph = Digraph(comment=self.label + " Supports", format="svg")
        visited = []

        def dfs(start):
            if start in visited:
                return
            visited.append(start)
            graph.node(
                str(start.pk),
                start.label,
                shape=start.type.shape,
                style="filled",
                fillcolor=start.type.color,
                URL=start.get_absolute_url(),
            )
            for neighbor in start.direct_supports.all():
                graph.edge(str(neighbor.pk), str(start.pk), dir="back")
                dfs(neighbor)

        dfs(self)
        return BeautifulSoup(graph.pipe(), "lxml").find("svg")
