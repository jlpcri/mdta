from django.contrib import admin

from .models import Node, NodeType, Edge, EdgeType, Module


@admin.register(Node, NodeType, Edge, EdgeType, Module)
class GraphsAdmin(admin.ModelAdmin):
    pass
