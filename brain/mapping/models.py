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
    engine = models.CharField(default="dot", choices=[("dot", "Dot (flows bottom to top)"), ("neato", "Neato (radial)")], max_length=10)

    def save(self, *args, **kwargs):
        self.slug = f"{self.id}-{slugify(self.label)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse("workspace-detail", args=[self.slug])

    def graphviz_graph(self):
        graph = Digraph(comment=self.label, format="svg", name=self.label, engine=self.engine, graph_attr={"overlap": "false"})
        for item in self.items.all():
            graph.node(
                str(item.pk),
                item.label,
                shape=item.type.shape,
                style="filled",
                fillcolor=item.type.color,
                tooltip=item.notes,
                URL=item.get_absolute_url(),
            )
        for dependency in self.relationships.all():
            graph.edge(
                str(dependency.item1.pk),
                str(dependency.item2.pk),
                dir="back",
                tooltip=dependency.description,
                URL=dependency.get_absolute_url(),
            )
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
    item1 = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="depends_on")
    item2 = models.ForeignKey(
        "Item", on_delete=models.CASCADE, related_name="supports"
    )
    description = models.CharField(max_length=1024, blank=True, default="")

    def get_absolute_url(self):
        return reverse("update-dependency", args=[self.workspace.slug, self.pk])


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
        return reverse("item-detail", args=[self.workspace.slug, self.slug])

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
        graph = Digraph(name=self.label + " Dependencies", format="svg")
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
                tooltip=start.notes,
                fillcolor=start.type.color,
                URL=start.get_absolute_url(),
            )
            for neighbor in start.depends_on.all():
                graph.edge(
                    str(start.pk),
                    str(neighbor.item2.pk),
                    tooltip=neighbor.description,
                    dir="back",
                )
                dfs(neighbor.item2)

        dfs(self)
        return BeautifulSoup(graph.pipe(), "lxml").find("svg")

    def full_support_graph(self):
        graph = Digraph(name=self.label + " Supports", format="svg")
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
                tooltip=start.notes,
                fillcolor=start.type.color,
                URL=start.get_absolute_url(),
            )
            for neighbor in start.supports.all():
                graph.edge(
                    str(neighbor.item1.pk),
                    str(start.pk),
                    tooltip=neighbor.description,
                    dir="back",
                )
                dfs(neighbor.item1)

        dfs(self)
        return BeautifulSoup(graph.pipe(), "lxml").find("svg")
