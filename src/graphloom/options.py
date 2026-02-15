from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, field_serializer, field_validator

from .enums import (
    Alignment,
    AnnulusWedgeCriteria,
    BoxLayoutProvider_PackingMode,
    CenterEdgeLabelPlacementStrategy,
    ComponentOrderingStrategy,
    ConstraintCalculationStrategy,
    ContentAlignment,
    CrossingMinimizationStrategy,
    CuttingStrategy,
    CycleBreakingStrategy,
    Direction,
    DirectionCongruency,
    DiscoCompactionStrategy,
    EdgeCoords,
    EdgeLabelPlacement,
    EdgeLabelSideSelection,
    EdgeRouting,
    EdgeRoutingMode,
    EdgeRoutingStrategy,
    EdgeStraighteningStrategy,
    EdgeType,
    FixedAlignment,
    ForceModelStrategy,
    GraphCompactionStrategy,
    GreedySwitchType,
    GroupOrderStrategy,
    HierarchyHandling,
    HighLevelSortingCriterion,
    InteractiveReferencePoint,
    LayerConstraint,
    LayerUnzippingStrategy,
    LayeringStrategy,
    LongEdgeOrderingStrategy,
    LowLevelSortingCriterion,
    NeatoModel,
    NodeArrangementStrategy,
    NodeFlexibility,
    NodeLabelPlacement,
    NodePlacementStrategy,
    NodePromotionStrategy,
    OptimizationGoal,
    OrderWeighting,
    OrderingStrategy,
    OverlapMode,
    PackingStrategy,
    PortAlignment,
    PortConstraints,
    PortLabelPlacement,
    PortSide,
    PortSortingStrategy,
    RadialCompactionStrategy,
    RadialTranslationStrategy,
    RootSelection,
    SelfLoopDistributionStrategy,
    SelfLoopOrderingStrategy,
    ShapeCoords,
    SizeConstraint,
    SizeOptions,
    SortingStrategy,
    SpanningTreeCostFunction,
    SplineRoutingMode,
    SporeCompactionStrategy,
    StressMajorization_Dimension,
    StructureExtractionStrategy,
    TopdownNodeTypes,
    TraversalStrategy,
    TreeConstructionStrategy,
    TreeifyingOrder,
    ValidifyStrategy,
    WhiteSpaceEliminationStrategy,
    WhitespaceEliminationStrategy,
    WidthApproximationStrategy,
    WrappingStrategy,
)

NodePlacementInput = Union[str, List[NodeLabelPlacement]]

def _split_list_str(value: str) -> List[str]:
    s = value.strip()
    if s.startswith("#[") and s.endswith("]"):
        s = s[2:-1].strip()
    elif s.startswith("[") and s.endswith("]"):
        s = s[1:-1].strip()
    if not s:
        return []
    return [p.strip() for p in s.split(",") if p.strip()]

def _serialize_enum_list(value: object) -> object:
    if isinstance(value, list):
        parts = []
        for item in value:
            if hasattr(item, "value"):
                parts.append(str(item.value))
            else:
                parts.append(str(item))
        return "[" + ",".join(parts) + "]"
    return value

def _parse_enum_set(value: object, enum_cls: type[Enum], allow_single_str: bool = False) -> object:
    if value is None:
        return value
    if isinstance(value, enum_cls):
        return [value]
    if isinstance(value, list):
        return [enum_cls(v) if not isinstance(v, enum_cls) else v for v in value]
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return []
        has_brackets = (s.startswith("[") and s.endswith("]")) or (s.startswith("#[") and s.endswith("]"))
        if allow_single_str and not has_brackets and "," not in s:
            return s
        return [enum_cls(p) for p in _split_list_str(s)]
    return value

def _parse_str_list(value: object) -> object:
    if value is None:
        return value
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return []
        return _split_list_str(s)
    return value

def _parse_int_list(value: object) -> object:
    if value is None:
        return value
    if isinstance(value, list):
        return [int(v) for v in value]
    if isinstance(value, str):
        return [int(p) for p in _split_list_str(value)]
    return value

class _LayoutOptionsBase(BaseModel):
    model_config = {"extra": "forbid", "populate_by_name": True}

    @field_serializer("org_eclipse_elk_nodeLabels_placement", check_fields=False)
    def serialize_node_labels_placement(self, v: Optional[List[NodeLabelPlacement]], _info):
        if v is None:
            return None
        return _serialize_enum_list(v)

    @field_validator("org_eclipse_elk_nodeLabels_placement", mode="before", check_fields=False)
    @classmethod
    def parse_placement(cls, v: NodePlacementInput):
        return _parse_enum_set(v, NodeLabelPlacement)

    @field_serializer("org_eclipse_elk_portLabels_placement", check_fields=False)
    def serialize_port_labels_placement(self, v: Optional[List[PortLabelPlacement]], _info):
        if v is None:
            return None
        return _serialize_enum_list(v)

    @field_validator("org_eclipse_elk_portLabels_placement", mode="before", check_fields=False)
    @classmethod
    def parse_port_placement(cls, v: Union[str, List[PortLabelPlacement]]):
        return _parse_enum_set(v, PortLabelPlacement)

    @field_serializer("org_eclipse_elk_nodeSize_constraints", check_fields=False)
    def serialize_node_size_constraints(self, v: Optional[Union[str, List[SizeConstraint]]], _info):
        if v is None:
            return None
        return _serialize_enum_list(v)

    @field_validator("org_eclipse_elk_nodeSize_constraints", mode="before", check_fields=False)
    @classmethod
    def parse_node_size_constraints(cls, v: Union[str, List[SizeConstraint], SizeConstraint]):
        return _parse_enum_set(v, SizeConstraint, allow_single_str=True)

    @field_serializer("org_eclipse_elk_nodeSize_options", check_fields=False)
    def serialize_node_size_options(self, v: Optional[Union[str, List[SizeOptions]]], _info):
        if v is None:
            return None
        return _serialize_enum_list(v)

    @field_validator("org_eclipse_elk_nodeSize_options", mode="before", check_fields=False)
    @classmethod
    def parse_node_size_options(cls, v: Union[str, List[SizeOptions], SizeOptions]):
        return _parse_enum_set(v, SizeOptions, allow_single_str=True)

    @field_serializer("org_eclipse_elk_contentAlignment", check_fields=False)
    def serialize_content_alignment(self, v: Optional[List[ContentAlignment]], _info):
        if v is None:
            return None
        return _serialize_enum_list(v)

    @field_validator("org_eclipse_elk_contentAlignment", mode="before", check_fields=False)
    @classmethod
    def parse_content_alignment(cls, v: Union[str, List[ContentAlignment]]):
        return _parse_enum_set(v, ContentAlignment)

    @field_validator(
        "org_eclipse_elk_layered_considerModelOrder_groupModelOrder_cmEnforcedGroupOrders",
        "org_eclipse_elk_layered_wrapping_cutting_cuts",
        "org_eclipse_elk_layered_wrapping_validify_forbiddenIndices",
        mode="before",
        check_fields=False,
    )
    @classmethod
    def parse_int_lists(cls, v: Union[str, List[int]]):
        return _parse_int_list(v)


class ParentLayoutOptions(_LayoutOptionsBase):
    org_eclipse_elk_graphviz_adaptPortPositions: Optional[bool] = Field(default=None, alias="org.eclipse.elk.graphviz.adaptPortPositions")
    org_eclipse_elk_layered_unnecessaryBendpoints: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.unnecessaryBendpoints")
    org_eclipse_elk_spacing_portsSurrounding: Optional[Any] = Field(default=None, alias="org.eclipse.elk.spacing.portsSurrounding")
    org_eclipse_elk_radial_rotation_computeAdditionalWedgeSpace: Optional[bool] = Field(default=None, alias="org.eclipse.elk.radial.rotation.computeAdditionalWedgeSpace")
    org_eclipse_elk_layered_wrapping_additionalEdgeSpacing: Optional[float] = Field(default=None, alias="org.eclipse.elk.layered.wrapping.additionalEdgeSpacing")
    org_eclipse_elk_alg_libavoid_anglePenalty: Optional[float] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.anglePenalty")
    org_eclipse_elk_animate: Optional[bool] = Field(default=None, alias="org.eclipse.elk.animate")
    org_eclipse_elk_animTimeFactor: Optional[int] = Field(default=None, alias="org.eclipse.elk.animTimeFactor")
    org_eclipse_elk_radial_wedgeCriteria: Optional[AnnulusWedgeCriteria] = Field(default=None, alias="org.eclipse.elk.radial.wedgeCriteria")
    org_eclipse_elk_aspectRatio: Optional[float] = Field(default=None, alias="org.eclipse.elk.aspectRatio")
    org_eclipse_elk_layered_nodePlacement_bk_edgeStraightening: Optional[EdgeStraighteningStrategy] = Field(default=None, alias="org.eclipse.elk.layered.nodePlacement.bk.edgeStraightening")
    org_eclipse_elk_layered_nodePlacement_bk_fixedAlignment: Optional[FixedAlignment] = Field(default=None, alias="org.eclipse.elk.layered.nodePlacement.bk.fixedAlignment")
    org_eclipse_elk_box_packingMode: Optional[BoxLayoutProvider_PackingMode] = Field(default=None, alias="org.eclipse.elk.box.packingMode")
    org_eclipse_elk_radial_centerOnRoot: Optional[bool] = Field(default=None, alias="org.eclipse.elk.radial.centerOnRoot")
    org_eclipse_elk_childAreaHeight: Optional[float] = Field(default=None, alias="org.eclipse.elk.childAreaHeight")
    org_eclipse_elk_childAreaWidth: Optional[float] = Field(default=None, alias="org.eclipse.elk.childAreaWidth")
    org_eclipse_elk_alg_libavoid_clusterCrossingPenalty: Optional[float] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.clusterCrossingPenalty")
    org_eclipse_elk_spacing_commentComment: Optional[float] = Field(default=None, alias="org.eclipse.elk.spacing.commentComment")
    org_eclipse_elk_spacing_commentNode: Optional[float] = Field(default=None, alias="org.eclipse.elk.spacing.commentNode")
    org_eclipse_elk_radial_compactor: Optional[RadialCompactionStrategy] = Field(default=None, alias="org.eclipse.elk.radial.compactor")
    org_eclipse_elk_rectpacking_packing_compaction_iterations: Optional[int] = Field(default=None, alias="org.eclipse.elk.rectpacking.packing.compaction.iterations")
    org_eclipse_elk_radial_compactionStepSize: Optional[int] = Field(default=None, alias="org.eclipse.elk.radial.compactionStepSize")
    org_eclipse_elk_compaction_compactionStrategy: Optional[SporeCompactionStrategy] = Field(default=None, alias="org.eclipse.elk.compaction.compactionStrategy")
    org_eclipse_elk_rectpacking_packing_strategy: Optional[PackingStrategy] = Field(default=None, alias="org.eclipse.elk.rectpacking.packing.strategy")
    org_eclipse_elk_spacing_componentComponent: Optional[float] = Field(default=None, alias="org.eclipse.elk.spacing.componentComponent")
    org_eclipse_elk_graphviz_concentrate: Optional[bool] = Field(default=None, alias="org.eclipse.elk.graphviz.concentrate")
    org_eclipse_elk_layered_compaction_connectedComponents: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.compaction.connectedComponents")
    org_eclipse_elk_disco_componentCompaction_strategy: Optional[DiscoCompactionStrategy] = Field(default=None, alias="org.eclipse.elk.disco.componentCompaction.strategy")
    org_eclipse_elk_disco_componentCompaction_componentLayoutAlgorithm: Optional[str] = Field(default=None, alias="org.eclipse.elk.disco.componentCompaction.componentLayoutAlgorithm")
    org_eclipse_elk_layered_considerModelOrder_strategy: Optional[OrderingStrategy] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.strategy")
    org_eclipse_elk_layered_considerModelOrder_components: Optional[ComponentOrderingStrategy] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.components")
    org_eclipse_elk_vertiflex_considerNodeModelOrder: Optional[bool] = Field(default=None, alias="org.eclipse.elk.vertiflex.considerNodeModelOrder")
    org_eclipse_elk_layered_considerModelOrder_portModelOrder: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.portModelOrder")
    org_eclipse_elk_contentAlignment: Optional[List[ContentAlignment]] = Field(default=None, alias="org.eclipse.elk.contentAlignment")
    org_eclipse_elk_layered_wrapping_correctionFactor: Optional[float] = Field(default=None, alias="org.eclipse.elk.layered.wrapping.correctionFactor")
    org_eclipse_elk_processingOrder_spanningTreeCostFunction: Optional[SpanningTreeCostFunction] = Field(default=None, alias="org.eclipse.elk.processingOrder.spanningTreeCostFunction")
    org_eclipse_elk_layered_considerModelOrder_crossingCounterNodeInfluence: Optional[float] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.crossingCounterNodeInfluence")
    org_eclipse_elk_layered_considerModelOrder_crossingCounterPortInfluence: Optional[float] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.crossingCounterPortInfluence")
    org_eclipse_elk_layered_considerModelOrder_groupModelOrder_cmEnforcedGroupOrders: Optional[List[int]] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.groupModelOrder.cmEnforcedGroupOrders")
    org_eclipse_elk_layered_considerModelOrder_groupModelOrder_cmGroupOrderStrategy: Optional[GroupOrderStrategy] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.groupModelOrder.cmGroupOrderStrategy")
    org_eclipse_elk_layered_crossingMinimization_strategy: Optional[CrossingMinimizationStrategy] = Field(default=None, alias="org.eclipse.elk.layered.crossingMinimization.strategy")
    org_eclipse_elk_alg_libavoid_crossingPenalty: Optional[float] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.crossingPenalty")
    org_eclipse_elk_layered_wrapping_cutting_strategy: Optional[CuttingStrategy] = Field(default=None, alias="org.eclipse.elk.layered.wrapping.cutting.strategy")
    org_eclipse_elk_layered_considerModelOrder_groupModelOrder_cbGroupOrderStrategy: Optional[GroupOrderStrategy] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.groupModelOrder.cbGroupOrderStrategy")
    org_eclipse_elk_layered_considerModelOrder_groupModelOrder_cbPreferredSourceId: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.groupModelOrder.cbPreferredSourceId")
    org_eclipse_elk_layered_considerModelOrder_groupModelOrder_cbPreferredTargetId: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.groupModelOrder.cbPreferredTargetId")
    org_eclipse_elk_layered_cycleBreaking_strategy: Optional[CycleBreakingStrategy] = Field(default=None, alias="org.eclipse.elk.layered.cycleBreaking.strategy")
    org_eclipse_elk_disco_debug_discoGraph: Optional[Any] = Field(default=None, alias="org.eclipse.elk.disco.debug.discoGraph")
    org_eclipse_elk_debugMode: Optional[bool] = Field(default=None, alias="org.eclipse.elk.debugMode")
    org_eclipse_elk_alg_libavoid_processTimeout: Optional[int] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.processTimeout")
    org_eclipse_elk_stress_desiredEdgeLength: Optional[float] = Field(default=None, alias="org.eclipse.elk.stress.desiredEdgeLength")
    org_eclipse_elk_direction: Optional[Direction] = Field(default=None, alias="org.eclipse.elk.direction")
    org_eclipse_elk_layered_directionCongruency: Optional[DirectionCongruency] = Field(default=None, alias="org.eclipse.elk.layered.directionCongruency")
    org_eclipse_elk_graphviz_neatoModel: Optional[NeatoModel] = Field(default=None, alias="org.eclipse.elk.graphviz.neatoModel")
    org_eclipse_elk_layered_wrapping_multiEdge_distancePenalty: Optional[float] = Field(default=None, alias="org.eclipse.elk.layered.wrapping.multiEdge.distancePenalty")
    org_eclipse_elk_force_repulsion: Optional[float] = Field(default=None, alias="org.eclipse.elk.force.repulsion")
    org_eclipse_elk_layered_edgeLabels_centerLabelPlacementStrategy: Optional[CenterEdgeLabelPlacementStrategy] = Field(default=None, alias="org.eclipse.elk.layered.edgeLabels.centerLabelPlacementStrategy")
    org_eclipse_elk_json_edgeCoords: Optional[EdgeCoords] = Field(default=None, alias="org.eclipse.elk.json.edgeCoords")
    org_eclipse_elk_layered_spacing_edgeEdgeBetweenLayers: Optional[float] = Field(default=None, alias="org.eclipse.elk.layered.spacing.edgeEdgeBetweenLayers")
    org_eclipse_elk_mrtree_edgeEndTextureLength: Optional[float] = Field(default=None, alias="org.eclipse.elk.mrtree.edgeEndTextureLength")
    org_eclipse_elk_layered_edgeLabels_sideSelection: Optional[EdgeLabelSideSelection] = Field(default=None, alias="org.eclipse.elk.layered.edgeLabels.sideSelection")
    org_eclipse_elk_spacing_edgeLabel: Optional[float] = Field(default=None, alias="org.eclipse.elk.spacing.edgeLabel")
    org_eclipse_elk_layered_spacing_edgeNodeBetweenLayers: Optional[float] = Field(default=None, alias="org.eclipse.elk.layered.spacing.edgeNodeBetweenLayers")
    org_eclipse_elk_spacing_edgeNode: Optional[float] = Field(default=None, alias="org.eclipse.elk.spacing.edgeNode")
    org_eclipse_elk_edgeRouting: Optional[EdgeRouting] = Field(default=None, alias="org.eclipse.elk.edgeRouting")
    org_eclipse_elk_mrtree_edgeRoutingMode: Optional[EdgeRoutingMode] = Field(default=None, alias="org.eclipse.elk.mrtree.edgeRoutingMode")
    org_eclipse_elk_spacing_edgeEdge: Optional[float] = Field(default=None, alias="org.eclipse.elk.spacing.edgeEdge")
    org_eclipse_elk_alg_libavoid_enableHyperedgesFromCommonSource: Optional[bool] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.enableHyperedgesFromCommonSource")
    org_eclipse_elk_graphviz_epsilon: Optional[float] = Field(default=None, alias="org.eclipse.elk.graphviz.epsilon")
    org_eclipse_elk_expandNodes: Optional[bool] = Field(default=None, alias="org.eclipse.elk.expandNodes")
    org_eclipse_elk_layered_nodePlacement_favorStraightEdges: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.nodePlacement.favorStraightEdges")
    org_eclipse_elk_layered_feedbackEdges: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.feedbackEdges")
    org_eclipse_elk_polyomino_fill: Optional[bool] = Field(default=None, alias="org.eclipse.elk.polyomino.fill")
    org_eclipse_elk_nodeSize_fixedGraphSize: Optional[bool] = Field(default=None, alias="org.eclipse.elk.nodeSize.fixedGraphSize")
    org_eclipse_elk_alg_libavoid_fixedSharedPathPenalty: Optional[float] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.fixedSharedPathPenalty")
    org_eclipse_elk_force_model: Optional[ForceModelStrategy] = Field(default=None, alias="org.eclipse.elk.force.model")
    org_eclipse_elk_layered_crossingMinimization_forceNodeModelOrder: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.crossingMinimization.forceNodeModelOrder")
    org_eclipse_elk_force_temperature: Optional[float] = Field(default=None, alias="org.eclipse.elk.force.temperature")
    org_eclipse_elk_layered_generatePositionAndLayerIds: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.generatePositionAndLayerIds")
    org_eclipse_elk_layered_wrapping_strategy: Optional[WrappingStrategy] = Field(default=None, alias="org.eclipse.elk.layered.wrapping.strategy")
    org_eclipse_elk_layered_crossingMinimization_greedySwitch_activationThreshold: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.crossingMinimization.greedySwitch.activationThreshold")
    org_eclipse_elk_layered_crossingMinimization_greedySwitch_type: Optional[GreedySwitchType] = Field(default=None, alias="org.eclipse.elk.layered.crossingMinimization.greedySwitch.type")
    org_eclipse_elk_layered_crossingMinimization_greedySwitchHierarchical_type: Optional[GreedySwitchType] = Field(default=None, alias="org.eclipse.elk.layered.crossingMinimization.greedySwitchHierarchical.type")
    org_eclipse_elk_layered_crossingMinimization_hierarchicalSweepiness: Optional[float] = Field(default=None, alias="org.eclipse.elk.layered.crossingMinimization.hierarchicalSweepiness")
    org_eclipse_elk_hierarchyHandling: Optional[HierarchyHandling] = Field(default=None, alias="org.eclipse.elk.hierarchyHandling")
    org_eclipse_elk_layered_highDegreeNodes_treeHeight: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.highDegreeNodes.treeHeight")
    org_eclipse_elk_layered_highDegreeNodes_threshold: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.highDegreeNodes.threshold")
    org_eclipse_elk_layered_highDegreeNodes_treatment: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.highDegreeNodes.treatment")
    org_eclipse_elk_spacing_labelPortHorizontal: Optional[float] = Field(default=None, alias="org.eclipse.elk.spacing.labelPortHorizontal")
    org_eclipse_elk_alg_libavoid_idealNudgingDistance: Optional[float] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.idealNudgingDistance")
    org_eclipse_elk_layered_wrapping_multiEdge_improveCuts: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.wrapping.multiEdge.improveCuts")
    org_eclipse_elk_alg_libavoid_improveHyperedgeRoutesMovingJunctions: Optional[bool] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.improveHyperedgeRoutesMovingJunctions")
    org_eclipse_elk_alg_libavoid_improveHyperedgeRoutesMovingAddingAndDeletingJunctions: Optional[bool] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.improveHyperedgeRoutesMovingAddingAndDeletingJunctions")
    org_eclipse_elk_layered_wrapping_multiEdge_improveWrappedEdges: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.wrapping.multiEdge.improveWrappedEdges")
    org_eclipse_elk_interactive: Optional[bool] = Field(default=None, alias="org.eclipse.elk.interactive")
    org_eclipse_elk_interactiveLayout: Optional[bool] = Field(default=None, alias="org.eclipse.elk.interactiveLayout")
    org_eclipse_elk_layered_interactiveReferencePoint: Optional[InteractiveReferencePoint] = Field(default=None, alias="org.eclipse.elk.layered.interactiveReferencePoint")
    org_eclipse_elk_stress_iterationLimit: Optional[int] = Field(default=None, alias="org.eclipse.elk.stress.iterationLimit")
    org_eclipse_elk_force_iterations: Optional[int] = Field(default=None, alias="org.eclipse.elk.force.iterations")
    org_eclipse_elk_graphviz_iterationsFactor: Optional[float] = Field(default=None, alias="org.eclipse.elk.graphviz.iterationsFactor")
    org_eclipse_elk_labelManager: Optional[Any] = Field(default=None, alias="org.eclipse.elk.labelManager")
    org_eclipse_elk_labels_labelManager: Optional[Any] = Field(default=None, alias="org.eclipse.elk.labels.labelManager")
    org_eclipse_elk_spacing_labelNode: Optional[float] = Field(default=None, alias="org.eclipse.elk.spacing.labelNode")
    org_eclipse_elk_spacing_labelLabel: Optional[float] = Field(default=None, alias="org.eclipse.elk.spacing.labelLabel")
    org_eclipse_elk_layered_layering_coffmanGraham_layerBound: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.layering.coffmanGraham.layerBound")
    org_eclipse_elk_vertiflex_layerDistance: Optional[float] = Field(default=None, alias="org.eclipse.elk.vertiflex.layerDistance")
    org_eclipse_elk_graphviz_layerSpacingFactor: Optional[float] = Field(default=None, alias="org.eclipse.elk.graphviz.layerSpacingFactor")
    org_eclipse_elk_layered_layerUnzipping_strategy: Optional[LayerUnzippingStrategy] = Field(default=None, alias="org.eclipse.elk.layered.layerUnzipping.strategy")
    org_eclipse_elk_algorithm: Optional[str] = Field(default=None, alias="org.eclipse.elk.algorithm")
    org_eclipse_elk_layoutAncestors: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layoutAncestors")
    org_eclipse_elk_stress_dimension: Optional[StressMajorization_Dimension] = Field(default=None, alias="org.eclipse.elk.stress.dimension")
    org_eclipse_elk_partitioning_partition: Optional[int] = Field(default=None, alias="org.eclipse.elk.partitioning.partition")
    org_eclipse_elk_partitioning_activate: Optional[bool] = Field(default=None, alias="org.eclipse.elk.partitioning.activate")
    org_eclipse_elk_layered_nodePlacement_linearSegments_deflectionDampening: Optional[float] = Field(default=None, alias="org.eclipse.elk.layered.nodePlacement.linearSegments.deflectionDampening")
    org_eclipse_elk_disco_debug_discoPolys: Optional[Any] = Field(default=None, alias="org.eclipse.elk.disco.debug.discoPolys")
    org_eclipse_elk_layered_considerModelOrder_longEdgeStrategy: Optional[LongEdgeOrderingStrategy] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.longEdgeStrategy")
    org_eclipse_elk_layered_wrapping_cutting_cuts: Optional[List[int]] = Field(default=None, alias="org.eclipse.elk.layered.wrapping.cutting.cuts")
    org_eclipse_elk_layered_layering_nodePromotion_maxIterations: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.layering.nodePromotion.maxIterations")
    org_eclipse_elk_graphviz_maxiter: Optional[int] = Field(default=None, alias="org.eclipse.elk.graphviz.maxiter")
    org_eclipse_elk_maxAnimTime: Optional[int] = Field(default=None, alias="org.eclipse.elk.maxAnimTime")
    org_eclipse_elk_layered_mergeEdges: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.mergeEdges")
    org_eclipse_elk_layered_mergeHierarchyEdges: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.mergeHierarchyEdges")
    org_eclipse_elk_minAnimTime: Optional[int] = Field(default=None, alias="org.eclipse.elk.minAnimTime")
    org_eclipse_elk_layered_wrapping_cutting_msd_freedom: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.wrapping.cutting.msd.freedom")
    org_eclipse_elk_topdownpacking_nodeArrangement_strategy: Optional[NodeArrangementStrategy] = Field(default=None, alias="org.eclipse.elk.topdownpacking.nodeArrangement.strategy")
    org_eclipse_elk_layered_nodePlacement_networkSimplex_nodeFlexibility_default: Optional[NodeFlexibility] = Field(default=None, alias="org.eclipse.elk.layered.nodePlacement.networkSimplex.nodeFlexibility.default")
    org_eclipse_elk_nodeLabels_padding: Optional[Any] = Field(default=None, alias="org.eclipse.elk.nodeLabels.padding")
    org_eclipse_elk_layered_layering_strategy: Optional[LayeringStrategy] = Field(default=None, alias="org.eclipse.elk.layered.layering.strategy")
    org_eclipse_elk_layered_spacing_nodeNodeBetweenLayers: Optional[float] = Field(default=None, alias="org.eclipse.elk.layered.spacing.nodeNodeBetweenLayers")
    org_eclipse_elk_layered_nodePlacement_strategy: Optional[NodePlacementStrategy] = Field(default=None, alias="org.eclipse.elk.layered.nodePlacement.strategy")
    org_eclipse_elk_layered_layering_nodePromotion_strategy: Optional[NodePromotionStrategy] = Field(default=None, alias="org.eclipse.elk.layered.layering.nodePromotion.strategy")
    org_eclipse_elk_spacing_nodeSelfLoop: Optional[float] = Field(default=None, alias="org.eclipse.elk.spacing.nodeSelfLoop")
    org_eclipse_elk_spacing_nodeNode: Optional[float] = Field(default=None, alias="org.eclipse.elk.spacing.nodeNode")
    org_eclipse_elk_alg_libavoid_nudgeOrthogonalSegmentsConnectedToShapes: Optional[bool] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.nudgeOrthogonalSegmentsConnectedToShapes")
    org_eclipse_elk_alg_libavoid_nudgeOrthogonalTouchingColinearSegments: Optional[bool] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.nudgeOrthogonalTouchingColinearSegments")
    org_eclipse_elk_alg_libavoid_nudgeSharedPathsWithCommonEndPoint: Optional[bool] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.nudgeSharedPathsWithCommonEndPoint")
    org_eclipse_elk_topdown_sizeCategories: Optional[int] = Field(default=None, alias="org.eclipse.elk.topdown.sizeCategories")
    org_eclipse_elk_omitNodeMicroLayout: Optional[bool] = Field(default=None, alias="org.eclipse.elk.omitNodeMicroLayout")
    org_eclipse_elk_rectpacking_widthApproximation_optimizationGoal: Optional[OptimizationGoal] = Field(default=None, alias="org.eclipse.elk.rectpacking.widthApproximation.optimizationGoal")
    org_eclipse_elk_rectpacking_orderBySize: Optional[bool] = Field(default=None, alias="org.eclipse.elk.rectpacking.orderBySize")
    org_eclipse_elk_compaction_orthogonal: Optional[bool] = Field(default=None, alias="org.eclipse.elk.compaction.orthogonal")
    org_eclipse_elk_radial_rotation_outgoingEdgeAngles: Optional[bool] = Field(default=None, alias="org.eclipse.elk.radial.rotation.outgoingEdgeAngles")
    org_eclipse_elk_graphviz_overlapMode: Optional[OverlapMode] = Field(default=None, alias="org.eclipse.elk.graphviz.overlapMode")
    org_eclipse_elk_padding: Optional[Any] = Field(default=None, alias="org.eclipse.elk.padding")
    org_eclipse_elk_alg_libavoid_penaliseOrthogonalSharedPathsAtConnEnds: Optional[bool] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.penaliseOrthogonalSharedPathsAtConnEnds")
    org_eclipse_elk_alg_libavoid_performUnifyingNudgingPreprocessingStep: Optional[bool] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.performUnifyingNudgingPreprocessingStep")
    org_eclipse_elk_polyomino_highLevelSort: Optional[HighLevelSortingCriterion] = Field(default=None, alias="org.eclipse.elk.polyomino.highLevelSort")
    org_eclipse_elk_polyomino_lowLevelSort: Optional[LowLevelSortingCriterion] = Field(default=None, alias="org.eclipse.elk.polyomino.lowLevelSort")
    org_eclipse_elk_polyomino_traversalStrategy: Optional[TraversalStrategy] = Field(default=None, alias="org.eclipse.elk.polyomino.traversalStrategy")
    org_eclipse_elk_alg_libavoid_portDirectionPenalty: Optional[float] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.portDirectionPenalty")
    org_eclipse_elk_layered_portSortingStrategy: Optional[PortSortingStrategy] = Field(default=None, alias="org.eclipse.elk.layered.portSortingStrategy")
    org_eclipse_elk_spacing_portPort: Optional[float] = Field(default=None, alias="org.eclipse.elk.spacing.portPort")
    org_eclipse_elk_mrtree_compaction: Optional[bool] = Field(default=None, alias="org.eclipse.elk.mrtree.compaction")
    org_eclipse_elk_layered_compaction_postCompaction_constraints: Optional[ConstraintCalculationStrategy] = Field(default=None, alias="org.eclipse.elk.layered.compaction.postCompaction.constraints")
    org_eclipse_elk_layered_compaction_postCompaction_strategy: Optional[GraphCompactionStrategy] = Field(default=None, alias="org.eclipse.elk.layered.compaction.postCompaction.strategy")
    org_eclipse_elk_progressBar: Optional[bool] = Field(default=None, alias="org.eclipse.elk.progressBar")
    org_eclipse_elk_radial_radius: Optional[float] = Field(default=None, alias="org.eclipse.elk.radial.radius")
    org_eclipse_elk_randomSeed: Optional[int] = Field(default=None, alias="org.eclipse.elk.randomSeed")
    org_eclipse_elk_resolvedAlgorithm: Optional[Any] = Field(default=None, alias="org.eclipse.elk.resolvedAlgorithm")
    org_eclipse_elk_alg_libavoid_reverseDirectionPenalty: Optional[float] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.reverseDirectionPenalty")
    org_eclipse_elk_processingOrder_preferredRoot: Optional[str] = Field(default=None, alias="org.eclipse.elk.processingOrder.preferredRoot")
    org_eclipse_elk_processingOrder_rootSelection: Optional[RootSelection] = Field(default=None, alias="org.eclipse.elk.processingOrder.rootSelection")
    org_eclipse_elk_radial_rotate: Optional[bool] = Field(default=None, alias="org.eclipse.elk.radial.rotate")
    org_eclipse_elk_rectpacking_packing_compaction_rowHeightReevaluation: Optional[bool] = Field(default=None, alias="org.eclipse.elk.rectpacking.packing.compaction.rowHeightReevaluation")
    org_eclipse_elk_mrtree_searchOrder: Optional[TreeifyingOrder] = Field(default=None, alias="org.eclipse.elk.mrtree.searchOrder")
    org_eclipse_elk_alg_libavoid_segmentPenalty: Optional[float] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.segmentPenalty")
    org_eclipse_elk_layered_crossingMinimization_semiInteractive: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.crossingMinimization.semiInteractive")
    org_eclipse_elk_separateConnectedComponents: Optional[bool] = Field(default=None, alias="org.eclipse.elk.separateConnectedComponents")
    org_eclipse_elk_alg_libavoid_shapeBufferDistance: Optional[float] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.shapeBufferDistance")
    org_eclipse_elk_json_shapeCoords: Optional[ShapeCoords] = Field(default=None, alias="org.eclipse.elk.json.shapeCoords")
    org_eclipse_elk_rectpacking_widthApproximation_lastPlaceShift: Optional[bool] = Field(default=None, alias="org.eclipse.elk.rectpacking.widthApproximation.lastPlaceShift")
    org_eclipse_elk_layered_edgeRouting_polyline_slopedEdgeZoneWidth: Optional[float] = Field(default=None, alias="org.eclipse.elk.layered.edgeRouting.polyline.slopedEdgeZoneWidth")
    org_eclipse_elk_layered_edgeRouting_splines_sloppy_layerSpacingFactor: Optional[float] = Field(default=None, alias="org.eclipse.elk.layered.edgeRouting.splines.sloppy.layerSpacingFactor")
    org_eclipse_elk_radial_sorter: Optional[SortingStrategy] = Field(default=None, alias="org.eclipse.elk.radial.sorter")
    org_eclipse_elk_layered_spacing_baseValue: Optional[float] = Field(default=None, alias="org.eclipse.elk.layered.spacing.baseValue")
    org_eclipse_elk_layered_edgeRouting_splines_mode: Optional[SplineRoutingMode] = Field(default=None, alias="org.eclipse.elk.layered.edgeRouting.splines.mode")
    org_eclipse_elk_stress_epsilon: Optional[float] = Field(default=None, alias="org.eclipse.elk.stress.epsilon")
    org_eclipse_elk_structure_structureExtractionStrategy: Optional[StructureExtractionStrategy] = Field(default=None, alias="org.eclipse.elk.structure.structureExtractionStrategy")
    org_eclipse_elk_radial_rotation_targetAngle: Optional[float] = Field(default=None, alias="org.eclipse.elk.radial.rotation.targetAngle")
    org_eclipse_elk_rectpacking_widthApproximation_targetWidth: Optional[float] = Field(default=None, alias="org.eclipse.elk.rectpacking.widthApproximation.targetWidth")
    org_eclipse_elk_layered_thoroughness: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.thoroughness")
    org_eclipse_elk_topdown_hierarchicalNodeAspectRatio: Optional[float] = Field(default=None, alias="org.eclipse.elk.topdown.hierarchicalNodeAspectRatio")
    org_eclipse_elk_topdown_hierarchicalNodeWidth: Optional[float] = Field(default=None, alias="org.eclipse.elk.topdown.hierarchicalNodeWidth")
    org_eclipse_elk_topdownLayout: Optional[bool] = Field(default=None, alias="org.eclipse.elk.topdownLayout")
    org_eclipse_elk_topdown_scaleCap: Optional[float] = Field(default=None, alias="org.eclipse.elk.topdown.scaleCap")
    org_eclipse_elk_topdown_scaleFactor: Optional[float] = Field(default=None, alias="org.eclipse.elk.topdown.scaleFactor")
    org_eclipse_elk_radial_optimizationCriteria: Optional[RadialTranslationStrategy] = Field(default=None, alias="org.eclipse.elk.radial.optimizationCriteria")
    org_eclipse_elk_processingOrder_treeConstruction: Optional[TreeConstructionStrategy] = Field(default=None, alias="org.eclipse.elk.processingOrder.treeConstruction")
    org_eclipse_elk_rectpacking_trybox: Optional[bool] = Field(default=None, alias="org.eclipse.elk.rectpacking.trybox")
    org_eclipse_elk_underlyingLayoutAlgorithm: Optional[str] = Field(default=None, alias="org.eclipse.elk.underlyingLayoutAlgorithm")
    org_eclipse_elk_layered_layering_minWidth_upperBoundOnWidth: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.layering.minWidth.upperBoundOnWidth")
    org_eclipse_elk_layered_layering_minWidth_upperLayerEstimationScalingFactor: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.layering.minWidth.upperLayerEstimationScalingFactor")
    org_eclipse_elk_overlapRemoval_maxIterations: Optional[int] = Field(default=None, alias="org.eclipse.elk.overlapRemoval.maxIterations")
    org_eclipse_elk_layered_wrapping_validify_forbiddenIndices: Optional[List[int]] = Field(default=None, alias="org.eclipse.elk.layered.wrapping.validify.forbiddenIndices")
    org_eclipse_elk_validateGraph: Optional[bool] = Field(default=None, alias="org.eclipse.elk.validateGraph")
    org_eclipse_elk_validateOptions: Optional[bool] = Field(default=None, alias="org.eclipse.elk.validateOptions")
    org_eclipse_elk_layered_wrapping_validify_strategy: Optional[ValidifyStrategy] = Field(default=None, alias="org.eclipse.elk.layered.wrapping.validify.strategy")
    org_eclipse_elk_spacing_labelPortVertical: Optional[float] = Field(default=None, alias="org.eclipse.elk.spacing.labelPortVertical")
    org_eclipse_elk_topdown_sizeCategoriesHierarchicalNodeWeight: Optional[int] = Field(default=None, alias="org.eclipse.elk.topdown.sizeCategoriesHierarchicalNodeWeight")
    org_eclipse_elk_mrtree_weighting: Optional[OrderWeighting] = Field(default=None, alias="org.eclipse.elk.mrtree.weighting")
    org_eclipse_elk_overlapRemoval_runScanline: Optional[bool] = Field(default=None, alias="org.eclipse.elk.overlapRemoval.runScanline")
    org_eclipse_elk_rectpacking_whiteSpaceElimination_strategy: Optional[WhiteSpaceEliminationStrategy] = Field(default=None, alias="org.eclipse.elk.rectpacking.whiteSpaceElimination.strategy")
    org_eclipse_elk_topdownpacking_whitespaceElimination_strategy: Optional[WhitespaceEliminationStrategy] = Field(default=None, alias="org.eclipse.elk.topdownpacking.whitespaceElimination.strategy")
    org_eclipse_elk_rectpacking_widthApproximation_strategy: Optional[WidthApproximationStrategy] = Field(default=None, alias="org.eclipse.elk.rectpacking.widthApproximation.strategy")
    org_eclipse_elk_zoomToFit: Optional[bool] = Field(default=None, alias="org.eclipse.elk.zoomToFit")

class NodeLayoutOptions(_LayoutOptionsBase):
    org_eclipse_elk_insideSelfLoops_activate: Optional[bool] = Field(default=None, alias="org.eclipse.elk.insideSelfLoops.activate")
    org_eclipse_elk_alignment: Optional[Alignment] = Field(default=None, alias="org.eclipse.elk.alignment")
    org_eclipse_elk_commentBox: Optional[bool] = Field(default=None, alias="org.eclipse.elk.commentBox")
    org_eclipse_elk_rectpacking_currentPosition: Optional[int] = Field(default=None, alias="org.eclipse.elk.rectpacking.currentPosition")
    org_eclipse_elk_rectpacking_desiredPosition: Optional[int] = Field(default=None, alias="org.eclipse.elk.rectpacking.desiredPosition")
    org_eclipse_elk_vertiflex_layoutStrategy: Optional[EdgeRoutingStrategy] = Field(default=None, alias="org.eclipse.elk.vertiflex.layoutStrategy")
    org_eclipse_elk_stress_fixed: Optional[bool] = Field(default=None, alias="org.eclipse.elk.stress.fixed")
    org_eclipse_elk_vertiflex_verticalConstraint: Optional[float] = Field(default=None, alias="org.eclipse.elk.vertiflex.verticalConstraint")
    org_eclipse_elk_layered_considerModelOrder_groupModelOrder_componentGroupId: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.groupModelOrder.componentGroupId")
    org_eclipse_elk_layered_considerModelOrder_groupModelOrder_crossingMinimizationId: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.groupModelOrder.crossingMinimizationId")
    org_eclipse_elk_layered_considerModelOrder_groupModelOrder_cycleBreakingId: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.groupModelOrder.cycleBreakingId")
    org_eclipse_elk_hierarchyHandling: Optional[HierarchyHandling] = Field(default=None, alias="org.eclipse.elk.hierarchyHandling")
    org_eclipse_elk_hypernode: Optional[bool] = Field(default=None, alias="org.eclipse.elk.hypernode")
    org_eclipse_elk_layered_crossingMinimization_inLayerPredOf: Optional[str] = Field(default=None, alias="org.eclipse.elk.layered.crossingMinimization.inLayerPredOf")
    org_eclipse_elk_layered_crossingMinimization_inLayerSuccOf: Optional[str] = Field(default=None, alias="org.eclipse.elk.layered.crossingMinimization.inLayerSuccOf")
    org_eclipse_elk_rectpacking_inNewRow: Optional[bool] = Field(default=None, alias="org.eclipse.elk.rectpacking.inNewRow")
    org_eclipse_elk_spacing_individual: Optional[Any] = Field(default=None, alias="org.eclipse.elk.spacing.individual")
    org_eclipse_elk_layered_layering_layerChoiceConstraint: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.layering.layerChoiceConstraint")
    org_eclipse_elk_layered_layering_layerConstraint: Optional[LayerConstraint] = Field(default=None, alias="org.eclipse.elk.layered.layering.layerConstraint")
    org_eclipse_elk_layered_layering_layerId: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.layering.layerId")
    org_eclipse_elk_partitioning_partition: Optional[int] = Field(default=None, alias="org.eclipse.elk.partitioning.partition")
    org_eclipse_elk_margins: Optional[Any] = Field(default=None, alias="org.eclipse.elk.margins")
    org_eclipse_elk_alg_libavoid_isCluster: Optional[bool] = Field(default=None, alias="org.eclipse.elk.alg.libavoid.isCluster")
    org_eclipse_elk_layered_layerUnzipping_minimizeEdgeLength: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.layerUnzipping.minimizeEdgeLength")
    org_eclipse_elk_noLayout: Optional[bool] = Field(default=None, alias="org.eclipse.elk.noLayout")
    org_eclipse_elk_layered_considerModelOrder_noModelOrder: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.noModelOrder")
    org_eclipse_elk_layered_nodePlacement_networkSimplex_nodeFlexibility: Optional[NodeFlexibility] = Field(default=None, alias="org.eclipse.elk.layered.nodePlacement.networkSimplex.nodeFlexibility")
    org_eclipse_elk_nodeLabels_placement: Optional[List[NodeLabelPlacement]] = Field(default=None, alias="org.eclipse.elk.nodeLabels.placement")
    org_eclipse_elk_nodeSize_constraints: Optional[Union[str, List[SizeConstraint]]] = Field(default=None, alias="org.eclipse.elk.nodeSize.constraints")
    org_eclipse_elk_nodeSize_minimum: Optional[Any] = Field(default=None, alias="org.eclipse.elk.nodeSize.minimum")
    org_eclipse_elk_nodeSize_options: Optional[Union[str, List[SizeOptions]]] = Field(default=None, alias="org.eclipse.elk.nodeSize.options")
    org_eclipse_elk_radial_orderId: Optional[int] = Field(default=None, alias="org.eclipse.elk.radial.orderId")
    org_eclipse_elk_padding: Optional[Any] = Field(default=None, alias="org.eclipse.elk.padding")
    org_eclipse_elk_portAlignment_default: Optional[PortAlignment] = Field(default=None, alias="org.eclipse.elk.portAlignment.default")
    org_eclipse_elk_portAlignment_east: Optional[PortAlignment] = Field(default=None, alias="org.eclipse.elk.portAlignment.east")
    org_eclipse_elk_portAlignment_north: Optional[PortAlignment] = Field(default=None, alias="org.eclipse.elk.portAlignment.north")
    org_eclipse_elk_portAlignment_south: Optional[PortAlignment] = Field(default=None, alias="org.eclipse.elk.portAlignment.south")
    org_eclipse_elk_portAlignment_west: Optional[PortAlignment] = Field(default=None, alias="org.eclipse.elk.portAlignment.west")
    org_eclipse_elk_portConstraints: Optional[PortConstraints] = Field(default=None, alias="org.eclipse.elk.portConstraints")
    org_eclipse_elk_portLabels_placement: Optional[List[PortLabelPlacement]] = Field(default=None, alias="org.eclipse.elk.portLabels.placement")
    org_eclipse_elk_portLabels_nextToPortIfPossible: Optional[bool] = Field(default=None, alias="org.eclipse.elk.portLabels.nextToPortIfPossible")
    org_eclipse_elk_spacing_portPort: Optional[float] = Field(default=None, alias="org.eclipse.elk.spacing.portPort")
    org_eclipse_elk_position: Optional[Any] = Field(default=None, alias="org.eclipse.elk.position")
    org_eclipse_elk_layered_crossingMinimization_positionChoiceConstraint: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.crossingMinimization.positionChoiceConstraint")
    org_eclipse_elk_mrtree_positionConstraint: Optional[int] = Field(default=None, alias="org.eclipse.elk.mrtree.positionConstraint")
    org_eclipse_elk_layered_crossingMinimization_positionId: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.crossingMinimization.positionId")
    org_eclipse_elk_priority: Optional[int] = Field(default=None, alias="org.eclipse.elk.priority")
    org_eclipse_elk_layered_layerUnzipping_resetOnLongEdges: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.layerUnzipping.resetOnLongEdges")
    org_eclipse_elk_scaleFactor: Optional[float] = Field(default=None, alias="org.eclipse.elk.scaleFactor")
    org_eclipse_elk_layered_edgeRouting_selfLoopDistribution: Optional[SelfLoopDistributionStrategy] = Field(default=None, alias="org.eclipse.elk.layered.edgeRouting.selfLoopDistribution")
    org_eclipse_elk_layered_edgeRouting_selfLoopOrdering: Optional[SelfLoopOrderingStrategy] = Field(default=None, alias="org.eclipse.elk.layered.edgeRouting.selfLoopOrdering")
    org_eclipse_elk_topdown_hierarchicalNodeAspectRatio: Optional[float] = Field(default=None, alias="org.eclipse.elk.topdown.hierarchicalNodeAspectRatio")
    org_eclipse_elk_topdown_hierarchicalNodeWidth: Optional[float] = Field(default=None, alias="org.eclipse.elk.topdown.hierarchicalNodeWidth")
    org_eclipse_elk_topdown_nodeType: Optional[TopdownNodeTypes] = Field(default=None, alias="org.eclipse.elk.topdown.nodeType")
    org_eclipse_elk_topdown_sizeApproximator: Optional[Any] = Field(default=None, alias="org.eclipse.elk.topdown.sizeApproximator")
    org_eclipse_elk_portLabels_treatAsGroup: Optional[bool] = Field(default=None, alias="org.eclipse.elk.portLabels.treatAsGroup")
    org_eclipse_elk_mrtree_treeLevel: Optional[int] = Field(default=None, alias="org.eclipse.elk.mrtree.treeLevel")
    org_eclipse_elk_layered_layerUnzipping_layerSplit: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.layerUnzipping.layerSplit")

class EdgeLayoutOptions(_LayoutOptionsBase):
    org_eclipse_elk_bendPoints: Optional[Any] = Field(default=None, alias="org.eclipse.elk.bendPoints")
    org_eclipse_elk_stress_desiredEdgeLength: Optional[float] = Field(default=None, alias="org.eclipse.elk.stress.desiredEdgeLength")
    org_eclipse_elk_layered_priority_direction: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.priority.direction")
    org_eclipse_elk_edge_thickness: Optional[float] = Field(default=None, alias="org.eclipse.elk.edge.thickness")
    org_eclipse_elk_edge_type: Optional[EdgeType] = Field(default=None, alias="org.eclipse.elk.edge.type")
    org_eclipse_elk_layered_considerModelOrder_groupModelOrder_componentGroupId: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.groupModelOrder.componentGroupId")
    org_eclipse_elk_layered_considerModelOrder_groupModelOrder_crossingMinimizationId: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.groupModelOrder.crossingMinimizationId")
    org_eclipse_elk_spacing_individual: Optional[Any] = Field(default=None, alias="org.eclipse.elk.spacing.individual")
    org_eclipse_elk_insideSelfLoops_yo: Optional[bool] = Field(default=None, alias="org.eclipse.elk.insideSelfLoops.yo")
    org_eclipse_elk_junctionPoints: Optional[Any] = Field(default=None, alias="org.eclipse.elk.junctionPoints")
    org_eclipse_elk_graphviz_labelAngle: Optional[float] = Field(default=None, alias="org.eclipse.elk.graphviz.labelAngle")
    org_eclipse_elk_graphviz_labelDistance: Optional[float] = Field(default=None, alias="org.eclipse.elk.graphviz.labelDistance")
    org_eclipse_elk_noLayout: Optional[bool] = Field(default=None, alias="org.eclipse.elk.noLayout")
    org_eclipse_elk_priority: Optional[int] = Field(default=None, alias="org.eclipse.elk.priority")
    org_eclipse_elk_force_repulsivePower: Optional[int] = Field(default=None, alias="org.eclipse.elk.force.repulsivePower")
    org_eclipse_elk_layered_priority_shortness: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.priority.shortness")
    org_eclipse_elk_layered_priority_straightness: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.priority.straightness")

class PortLayoutOptions(_LayoutOptionsBase):
    org_eclipse_elk_layered_allowNonFlowPortsToSwitchSides: Optional[bool] = Field(default=None, alias="org.eclipse.elk.layered.allowNonFlowPortsToSwitchSides")
    org_eclipse_elk_layered_considerModelOrder_groupModelOrder_componentGroupId: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.groupModelOrder.componentGroupId")
    org_eclipse_elk_layered_considerModelOrder_groupModelOrder_crossingMinimizationId: Optional[int] = Field(default=None, alias="org.eclipse.elk.layered.considerModelOrder.groupModelOrder.crossingMinimizationId")
    org_eclipse_elk_spacing_individual: Optional[Any] = Field(default=None, alias="org.eclipse.elk.spacing.individual")
    org_eclipse_elk_noLayout: Optional[bool] = Field(default=None, alias="org.eclipse.elk.noLayout")
    org_eclipse_elk_port_anchor: Optional[Any] = Field(default=None, alias="org.eclipse.elk.port.anchor")
    org_eclipse_elk_port_borderOffset: Optional[float] = Field(default=None, alias="org.eclipse.elk.port.borderOffset")
    org_eclipse_elk_port_index: Optional[int] = Field(default=None, alias="org.eclipse.elk.port.index")
    org_eclipse_elk_port_side: Optional[PortSide] = Field(default=None, alias="org.eclipse.elk.port.side")
    org_eclipse_elk_position: Optional[Any] = Field(default=None, alias="org.eclipse.elk.position")

class LabelLayoutOptions(_LayoutOptionsBase):
    org_eclipse_elk_layered_edgeLabels_centerLabelPlacementStrategy: Optional[CenterEdgeLabelPlacementStrategy] = Field(default=None, alias="org.eclipse.elk.layered.edgeLabels.centerLabelPlacementStrategy")
    org_eclipse_elk_edgeLabels_placement: Optional[EdgeLabelPlacement] = Field(default=None, alias="org.eclipse.elk.edgeLabels.placement")
    org_eclipse_elk_font_name: Optional[str] = Field(default=None, alias="org.eclipse.elk.font.name")
    org_eclipse_elk_font_size: Optional[int] = Field(default=None, alias="org.eclipse.elk.font.size")
    org_eclipse_elk_spacing_individual: Optional[Any] = Field(default=None, alias="org.eclipse.elk.spacing.individual")
    org_eclipse_elk_edgeLabels_inline: Optional[bool] = Field(default=None, alias="org.eclipse.elk.edgeLabels.inline")
    org_eclipse_elk_labelManager: Optional[Any] = Field(default=None, alias="org.eclipse.elk.labelManager")
    org_eclipse_elk_labels_labelManager: Optional[Any] = Field(default=None, alias="org.eclipse.elk.labels.labelManager")
    org_eclipse_elk_noLayout: Optional[bool] = Field(default=None, alias="org.eclipse.elk.noLayout")
    org_eclipse_elk_nodeLabels_placement: Optional[List[NodeLabelPlacement]] = Field(default=None, alias="org.eclipse.elk.nodeLabels.placement")
    org_eclipse_elk_position: Optional[Any] = Field(default=None, alias="org.eclipse.elk.position")
    org_eclipse_elk_softwrappingFuzziness: Optional[float] = Field(default=None, alias="org.eclipse.elk.softwrappingFuzziness")


class LayoutOptions(ParentLayoutOptions):
    org_eclipse_elk_portConstraints: Optional[PortConstraints] = Field(
        default=None,
        alias="org.eclipse.elk.portConstraints",
    )
    model_config = {"extra": "allow", "populate_by_name": True}
