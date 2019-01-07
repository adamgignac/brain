# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from bs4 import BeautifulSoup

from graphviz import Digraph
from .graphviz_attrs import SHAPES, COLORS


class Workspace(models.Model):
    label = models.CharField(max_length=1024)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('workspace-detail', args=[self.pk])

    def graphviz_graph(self):
        graph = Digraph(comment=self.label, format="svg")
        for item in self.item_set.all():
            graph.node(str(item.pk), item.label,
                       shape=item.type.shape,
                       style="filled",
                       fillcolor=item.type.color,
                       URL=item.get_absolute_url())
            for dependency in item.dependencies.all():
                graph.edge(str(item.pk), str(dependency.pk), dir="back")
        return BeautifulSoup(graph.pipe(), "lxml").find("svg")


class ItemType(models.Model):
    label = models.CharField(max_length=1024)
    shape = models.CharField(max_length=15, choices=SHAPES)
    color = models.CharField(max_length=15, choices=COLORS, default='white')

    def __str__(self):
        return self.label


class Item(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    label = models.CharField(max_length=1024)
    dependencies = models.ManyToManyField("self", blank=True,
                                          symmetrical=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('item-detail', args=[self.pk])

    @property
    def direct_supports(self):
        return Item.objects.filter(dependencies=self.pk)

    def full_dependency_graph(self):
        graph = Digraph(comment=self.label + " Dependencies", format="svg")
        # Breadth-first search
        for item in self.dependencies.all():
            continue

    def full_support_graph(self):
        graph = Digraph(comment=self.label + " Supports", format="svg")
        # Breadth-first search
        for item in self.direct_supports.all():
            continue
