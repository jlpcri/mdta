from django.contrib import admin

from .models import Node, NodeType, Edge, EdgeType


@admin.register(Node, NodeType, Edge, EdgeType)
class GraphsAdmin(admin.ModelAdmin):
    pass
