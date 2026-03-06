"""Top-level canvas model representing a complete ELK graph.

The :class:`Canvas` is the root container that holds all top-level nodes
(children), edges, and the global layout options passed to the ELK layout
engine.  It is the final output produced by :func:`graphloom.builder.build_canvas`.
"""

from typing import List
from pydantic import BaseModel, Field, field_validator

from .edge import Edge
from .enums import Direction, EdgeRouting, EdgeRoutingMode, LayeringStrategy
from .node import Node
from .options import LayoutOptions

class Canvas(BaseModel):
    """Root ELK graph container.

    Attributes:
        id: Unique identifier for the canvas, defaults to ``"canvas"``.
        layoutOptions: Global ELK layout options applied at the root level.
        children: Top-level nodes contained in the graph.  Each child
            must have a unique ``id``.
        edges: Top-level edges connecting the children.  Each edge must
            have a unique ``id``.
    """

    model_config = {"populate_by_name": True}

    id: str = "canvas"
    layoutOptions: LayoutOptions
    children: List[Node]
    edges: List[Edge] = Field(default_factory=list)

    @field_validator("children")
    @classmethod
    def children_ids_unique(cls, v: List[Node]) -> List[Node]:
        """Validate that all child node ids are unique.

        Args:
            v: List of top-level :class:`~graphloom.node.Node` instances.

        Returns:
            The unmodified list when validation passes.

        Raises:
            ValueError: If two or more children share the same ``id``.
        """
        ids = [c.id for c in v]
        if len(ids) != len(set(ids)):
            raise ValueError("children id values must be unique")
        return v

    @field_validator("edges")
    @classmethod
    def edge_ids_unique(cls, v: List[Edge]) -> List[Edge]:
        """Validate that all top-level edge ids are unique.

        Args:
            v: List of top-level :class:`~graphloom.edge.Edge` instances.

        Returns:
            The unmodified list when validation passes.

        Raises:
            ValueError: If two or more edges share the same ``id``.
        """
        ids = [e.id for e in v]
        if len(ids) != len(set(ids)):
            raise ValueError("edge id values must be unique")
        return v
